import json
import math

from art.utils.deploy_model import (
    LoRADeploymentJob,
    LoRADeploymentProvider,
    deploy_model,
)
from art.utils.old_benchmarking.calculate_step_metrics import calculate_step_std_dev
from art.utils.output_dirs import (
    get_default_art_path,
    get_model_dir,
    get_trajectories_split_dir,
)
from art.utils.trajectory_logging import serialize_trajectory_groups
from mp_actors import move_to_child_process
import numpy as np
import os
import polars as pl
import subprocess
import torch
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from tqdm import auto as tqdm
from typing import AsyncIterator, cast
import wandb
from wandb.sdk.wandb_run import Run
import weave
from weave.trace.weave_client import WeaveClient

from .. import dev
from ..backend import Backend
from ..model import Model, TrainableModel
from .service import ModelService
from ..trajectories import Trajectory, TrajectoryGroup
from ..types import Message, TrainConfig
from ..utils import format_message, get_model_step
from .pack import (
    packed_tensors_from_tokenized_results,
    packed_tensors_to_dir,
    PackedTensors,
    plot_packed_tensors,
)
from .tokenize import tokenize_trajectory_groups
from .checkpoints import (
    delete_checkpoints,
)
from art.utils.s3 import (
    pull_model_from_s3,
    push_model_to_s3,
    ExcludableOption,
)


class LocalBackend(Backend):
    def __init__(self, *, in_process: bool = False, path: str | None = None) -> None:
        """
        Initializes a local, directory-based Backend interface at the given path.

        Note:
            The local Backend uses Weights & Biases for training monitoring.
            If you don't have a W&B account, you can create one at https://wandb.ai.

        Args:
            in_process: Whether to run the local service in-process.
            path: The path to the local directory. Defaults to "{repo_root}/.art".
        """
        self._in_process = in_process
        self._path = path or get_default_art_path()
        os.makedirs(self._path, exist_ok=True)

        # Other initialization
        self._services: dict[str, ModelService] = {}
        self._tokenizers: dict[str, "PreTrainedTokenizerBase"] = {}
        self._wandb_runs: dict[str, Run] = {}
        self._weave_clients: dict[str, WeaveClient] = {}

    def __enter__(self):
        return self

    def __exit__(self, *excinfo):
        self.close()

    def close(self):
        """
        If running vLLM in a separate process, this will kill that process and close the communication threads.
        """
        for _, service in self._services.items():
            close_method = getattr(service, "close", None)
            if callable(close_method):
                close_method()

    async def register(
        self,
        model: Model,
    ) -> None:
        """
        Registers a model with the local Backend for logging and/or training.

        Args:
            model: An art.Model instance.
        """
        output_dir = get_model_dir(model=model, art_path=self._path)
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/model.json", "w") as f:
            json.dump(model.model_dump(), f)

        # Initialize wandb and weave early if this is a trainable model
        if isinstance(model, TrainableModel) and "WANDB_API_KEY" in os.environ:
            _ = self._get_wandb_run(model)

    async def _get_service(self, model: TrainableModel) -> ModelService:
        from ..torchtune.service import TorchtuneService
        from ..unsloth.service import UnslothService
        from ..unsloth.decoupled_service import DecoupledUnslothService

        if model.name not in self._services:
            config = dev.get_model_config(
                base_model=model.base_model,
                output_dir=get_model_dir(model=model, art_path=self._path),
                config=model._internal_config,
            )
            if config.get("torchtune_args") is not None:
                service_class = TorchtuneService
            elif config.get("_decouple_vllm_and_unsloth", False):
                service_class = DecoupledUnslothService
            else:
                service_class = UnslothService
            self._services[model.name] = service_class(
                model_name=model.name,
                base_model=model.base_model,
                config=config,
                output_dir=get_model_dir(model=model, art_path=self._path),
            )
            if not self._in_process:
                # Kill all "model-service" processes to free up GPU memory
                subprocess.run(["pkill", "-9", "model-service"])
                if isinstance(
                    self._services[model.name],
                    (UnslothService, DecoupledUnslothService),
                ):
                    # To enable sleep mode, import peft before unsloth
                    # Unsloth will issue warnings, but everything appears to be okay
                    if config.get("engine_args", {}).get("enable_sleep_mode", False):
                        os.environ["IMPORT_PEFT"] = "1"
                    # When moving the service to a child process, import unsloth
                    # early to maximize optimizations
                    os.environ["IMPORT_UNSLOTH"] = "1"
                self._services[model.name] = move_to_child_process(
                    self._services[model.name],
                    process_name="model-service",
                )
        return self._services[model.name]

    def _get_packed_tensors(
        self,
        model: TrainableModel,
        trajectory_groups: list[TrajectoryGroup],
        allow_training_without_logprobs: bool,
        plot_tensors: bool,
    ) -> PackedTensors | None:
        if model.base_model not in self._tokenizers:
            self._tokenizers[model.base_model] = AutoTokenizer.from_pretrained(
                model.base_model
            )
        tokenizer = self._tokenizers[model.base_model]
        tokenized_results = list(
            tokenize_trajectory_groups(
                tokenizer,
                trajectory_groups,
                allow_training_without_logprobs,
            )
        )
        if not tokenized_results:
            return None
        max_tokens = max(len(result.tokens) for result in tokenized_results)
        # Round up max_tokens to the nearest multiple of 2048
        sequence_length = math.ceil(max_tokens / 2048) * 2048
        # Cap sequence length at the model's max sequence length
        sequence_length = min(
            sequence_length,
            (model._internal_config or dev.InternalModelConfig())
            .get("init_args", {})
            .get("max_seq_length", 32_768),
        )
        packed_tensors = packed_tensors_from_tokenized_results(
            tokenized_results,
            sequence_length,
            pad_token_id=tokenizer.eos_token_id,  # type: ignore
        )
        if (
            not allow_training_without_logprobs
            and np.isnan(packed_tensors["logprobs"]).all()
        ):
            print(
                "There are no assistant logprobs to train on. Did you forget to include at least one Choice in Trajectory.messages_and_choices?"
            )
            return None
        if plot_tensors:
            plot_packed_tensors(
                packed_tensors, get_model_dir(model=model, art_path=self._path)
            )
        else:
            print(
                f"Packed {len(tokenized_results)} trajectories into {packed_tensors['tokens'].shape[0]} sequences of length {packed_tensors['tokens'].shape[1]}"
            )
        return packed_tensors

    async def _get_step(self, model: TrainableModel) -> int:
        return self.__get_step(model)

    def __get_step(self, model: TrainableModel) -> int:
        return get_model_step(model, self._path)

    async def _delete_checkpoints(
        self,
        model: TrainableModel,
        benchmark: str,
        benchmark_smoothing: float,
    ) -> None:
        output_dir = get_model_dir(model=model, art_path=self._path)
        # Keep the latest step
        steps_to_keep = [get_model_step(model, self._path)]
        try:
            best_step = (
                pl.read_ndjson(f"{output_dir}/history.jsonl")
                .drop_nulls(subset=[benchmark])
                .group_by("step")
                .mean()
                .with_columns(pl.col(benchmark).ewm_mean(alpha=benchmark_smoothing))
                .sort(benchmark)
                .select(pl.col("step").last())
                .item()
            )
            steps_to_keep.append(best_step)
        except FileNotFoundError:
            pass
        except pl.exceptions.ColumnNotFoundError:
            print(f'No "{benchmark}" metric found in history')
        delete_checkpoints(output_dir, steps_to_keep)

    async def _prepare_backend_for_training(
        self,
        model: TrainableModel,
        config: dev.OpenAIServerConfig | None = None,
    ) -> tuple[str, str]:
        service = await self._get_service(model)
        await service.start_openai_server(config=config)
        server_args = (config or {}).get("server_args", {})

        base_url = f"http://{server_args.get('host', '0.0.0.0')}:{server_args.get('port', 8000)}/v1"
        api_key = server_args.get("api_key", None) or "default"

        return base_url, api_key

    async def _log(
        self,
        model: Model,
        trajectory_groups: list[TrajectoryGroup],
        split: str = "val",
    ) -> None:
        # Save logs for trajectory groups
        parent_dir = get_trajectories_split_dir(
            get_model_dir(model=model, art_path=self._path), split
        )
        os.makedirs(parent_dir, exist_ok=True)

        # Get the file name for the current iteration, or default to 0 for non-trainable models
        iteration = self.__get_step(model) if isinstance(model, TrainableModel) else 0
        file_name = f"{iteration:04d}.jsonl"

        # Write the logs to the file
        with open(f"{parent_dir}/{file_name}", "w") as f:
            f.write(serialize_trajectory_groups(trajectory_groups))

        # Collect all metrics (including reward) across all trajectories
        all_metrics: dict[str, list[float]] = {"reward": [], "exception_rate": []}

        for group in trajectory_groups:
            for trajectory in group:
                if isinstance(trajectory, BaseException):
                    all_metrics["exception_rate"].append(1)
                    continue
                else:
                    all_metrics["exception_rate"].append(0)
                # Add reward metric
                all_metrics["reward"].append(trajectory.reward)

                # Collect other custom metrics
                for metric, value in trajectory.metrics.items():
                    if metric not in all_metrics:
                        all_metrics[metric] = []
                    all_metrics[metric].append(float(value))

        # Calculate averages for all metrics
        averages = {}
        for metric, values in all_metrics.items():
            if len(values) > 0:
                averages[metric] = sum(values) / len(values)

        # Calculate average standard deviation of rewards within groups
        averages["reward_std_dev"] = calculate_step_std_dev(trajectory_groups)

        self._log_metrics(model, averages, split)

    def _trajectory_log(self, trajectory: Trajectory) -> str:
        """Format a trajectory into a readable log string."""
        header = f"reward: {trajectory.reward} {' '.join(f'{k}: {v}' for k, v in trajectory.metrics.items())}\n\n"
        formatted_messages = []
        for message_or_choice in trajectory.messages_and_choices:
            if isinstance(message_or_choice, dict):
                message = message_or_choice
            else:
                message = cast(Message, message_or_choice.message.model_dump())
            formatted_messages.append(format_message(message))
        return header + "\n".join(formatted_messages)

    async def _train_model(
        self,
        model: TrainableModel,
        trajectory_groups: list[TrajectoryGroup],
        config: TrainConfig,
        dev_config: dev.TrainConfig,
        verbose: bool = False,
    ) -> AsyncIterator[dict[str, float]]:
        step = await self._get_step(model)
        if verbose:
            print("Starting _train_model")
        service = await self._get_service(model)
        if verbose:
            print("Logging training data to disk...")
        await self._log(model, trajectory_groups, "train")
        if verbose:
            print("Packing tensors...")
        packed_tensors = self._get_packed_tensors(
            model,
            trajectory_groups,
            allow_training_without_logprobs=dev_config.get(
                "allow_training_without_logprobs", False
            ),
            plot_tensors=dev_config.get("plot_tensors", False),
        )
        if packed_tensors is None:
            print(
                "Skipping tuning as there is no suitable data. "
                "This can happen when all the trajectories in the same group "
                "have the same reward and thus no advantage to train on."
            )
            return
        disk_packed_tensors = packed_tensors_to_dir(
            packed_tensors, f"{get_model_dir(model=model, art_path=self._path)}/tensors"
        )
        results: list[dict[str, float]] = []
        estimated_gradient_steps = disk_packed_tensors["num_sequences"]
        if torchtune_args := (model._internal_config or dev.InternalModelConfig()).get(
            "torchtune_args"
        ):
            tp = torchtune_args.get("tensor_parallel_dim", 1)
            cp = torchtune_args.get("context_parallel_dim", 1)
            world_size = torch.cuda.device_count()
            dp = world_size // (tp * cp)
            estimated_gradient_steps = math.ceil(estimated_gradient_steps / dp)
        pbar = tqdm.tqdm(total=estimated_gradient_steps, desc="train")
        async for result in service.train(
            disk_packed_tensors, config, dev_config, verbose
        ):
            num_gradient_steps = int(
                result.pop("num_gradient_steps", estimated_gradient_steps)
            )
            assert num_gradient_steps == estimated_gradient_steps, (
                f"num_gradient_steps {num_gradient_steps} != estimated_gradient_steps {estimated_gradient_steps}"
            )
            results.append(result)
            yield {**result, "num_gradient_steps": num_gradient_steps}
            pbar.update(1)
            pbar.set_postfix(result)
        pbar.close()
        if verbose:
            print("Logging metrics...")
        data = {
            k: sum(d.get(k, 0) for d in results) / sum(1 for d in results if k in d)
            for k in {k for d in results for k in d}
        }
        self._log_metrics(model, data, "train", step=step)
        if verbose:
            print("_train_model complete")

    def _log_metrics(
        self,
        model: Model,
        metrics: dict[str, float],
        split: str,
        step: int | None = None,
    ) -> None:
        metrics = {f"{split}/{metric}": value for metric, value in metrics.items()}
        step = (
            step
            if step is not None
            else (self.__get_step(model) if isinstance(model, TrainableModel) else 0)
        )

        # If we have a W&B run, log the data there
        if run := self._get_wandb_run(model):
            # Mark the step metric itself as hidden so W&B doesn't create an automatic chart for it
            wandb.define_metric("training_step", hidden=True)

            # Enabling the following line will cause W&B to use the training_step metric as the x-axis for all metrics
            # wandb.define_metric(f"{split}/*", step_metric="training_step")
            run.log({"training_step": step, **metrics}, step=step)

    def _get_wandb_run(self, model: Model) -> Run | None:
        if "WANDB_API_KEY" not in os.environ:
            return None
        if (
            model.name not in self._wandb_runs
            or self._wandb_runs[model.name]._is_finished
        ):
            run = wandb.init(
                project=model.project,
                name=model.name,
                id=model.name,
                resume="allow",
                settings=wandb.Settings(
                    x_stats_open_metrics_endpoints={
                        "vllm": "http://localhost:8000/metrics",
                    },
                    x_stats_open_metrics_filters=(
                        "vllm.vllm:num_requests_waiting",
                        "vllm.vllm:num_requests_running",
                    ),
                ),
            )
            self._wandb_runs[model.name] = run
            os.environ["WEAVE_PRINT_CALL_LINK"] = os.getenv(
                "WEAVE_PRINT_CALL_LINK", "False"
            )
            os.environ["WEAVE_LOG_LEVEL"] = os.getenv("WEAVE_LOG_LEVEL", "CRITICAL")
            self._weave_clients[model.name] = weave.init(model.project)
        return self._wandb_runs[model.name]

    # ------------------------------------------------------------------
    # Experimental support for S3
    # ------------------------------------------------------------------

    async def _experimental_pull_from_s3(
        self,
        model: Model,
        step: int | None = None,
        s3_bucket: str | None = None,
        prefix: str | None = None,
        verbose: bool = False,
        delete: bool = False,
        exclude: list[ExcludableOption] | None = None,
    ) -> None:
        """Download the model directory from S3 into local Backend storage. Right now this can be used to pull trajectory logs for processing or model checkpoints.
        Args:
            model: The model to pull from S3.
            step: A specific step to pull from S3. If None, all steps will be pulled.
            s3_bucket: The S3 bucket to pull from. If None, the default bucket will be used.
            prefix: The prefix to pull from S3. If None, the model name will be used.
            verbose: Whether to print verbose output.
            delete: Whether to delete the local model directory.
            exclude: List of directories to exclude from sync. Valid options: "checkpoints", "logs", "trajectories".
        """

        await pull_model_from_s3(
            model_name=model.name,
            project=model.project,
            step=step,
            s3_bucket=s3_bucket,
            prefix=prefix,
            verbose=verbose,
            delete=delete,
            art_path=self._path,
            exclude=exclude,
        )

    async def _experimental_push_to_s3(
        self,
        model: Model,
        s3_bucket: str | None = None,
        prefix: str | None = None,
        verbose: bool = False,
        delete: bool = False,
    ) -> None:
        """Upload the model directory from local storage to S3."""
        await push_model_to_s3(
            model_name=model.name,
            project=model.project,
            s3_bucket=s3_bucket,
            prefix=prefix,
            verbose=verbose,
            delete=delete,
            art_path=self._path,
        )

    async def _experimental_deploy(
        self,
        deploy_to: LoRADeploymentProvider,
        model: "TrainableModel",
        step: int | None = None,
        s3_bucket: str | None = None,
        prefix: str | None = None,
        verbose: bool = False,
        pull_s3: bool = True,
        wait_for_completion: bool = True,
    ) -> LoRADeploymentJob:
        """
        Deploy the model's latest checkpoint to a hosted inference endpoint.

        Together is currently the only supported provider. See link for supported base models:
        https://docs.together.ai/docs/lora-inference#supported-base-models
        """
        return await deploy_model(
            deploy_to=deploy_to,
            model=model,
            step=step,
            s3_bucket=s3_bucket,
            prefix=prefix,
            verbose=verbose,
            pull_s3=pull_s3,
            wait_for_completion=wait_for_completion,
            art_path=self._path,
        )
