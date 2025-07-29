from __future__ import annotations

import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableConfig(BaseModel):
    port: int = Field(
        default=8000,
        description="The port number to use table node",
        ge=0,
        le=65535,
    )
    trial_timeout_seconds: int = Field(
        default=600,
        description="Timeout seconds before a trial is reserved and registered",
        ge=1,
    )
    timeout_check_interval_seconds: int = Field(
        default=60,
        description="Interval of time to check timeout trials",
        ge=1,
    )
    curriculum_path: Path = Field(
        default=Path.cwd() / "curriculum.json",
        description="Path to the curriculum json file",
    )
    trial_file_dir: Path = Field(
        default=Path.cwd() / "trials",
        description="Path to the trial files",
    )
    curriculum_save_interval_seconds: int = Field(
        default=600,
        description="Interval of time to save curriculum json file",
        ge=1,
    )

    @staticmethod
    def load_from_file(path: Path | None) -> TableConfig:
        if path is None:
            path = Path.cwd() / "table_config.json"
        if not path.exists():
            logger.info("TableConfig not found, creating it now")
            default_config = TableConfig()
            with path.open(mode="w") as f:
                json.dump(default_config.model_dump(mode="json"), f, indent=4)
        with path.open() as f:
            return TableConfig.model_validate(json.load(f))


class WorkerConfig(BaseModel):
    name: str | None = Field(
        default=None,
        description="Name of the worker node",
    )
    process_num: int | None = Field(
        default=None,
        description="The number of processes on using `AutoMPTrialRunner`. If `None`, use `os.cpu_count()`.",
    )
    chunk_size: int = Field(
        default=1,
        description="The size of the chunks to be passed to each process.",
    )
    max_size: int = Field(
        default=1,
        description="The maximum size of a trial.",
    )
    disable_function_progress_bar: bool = Field(
        default=False,
        description="Whether to disable progress bar.",
    )
    retaining_capacity: set[str] = Field(
        default_factory=set,
        description="Set of capabilities that the worker node has.",
    )
    wait_seconds_on_no_trial: int = Field(
        default=5,
        description="Waiting time when there was no trial allocated by the table node.",
        ge=1,
    )
    table_node_request_timeout_seconds: int = Field(
        default=30,
        description="Timeout for requests to table nodes.",
        ge=1,
    )


class TableConfigProvider:
    _TABLE: TableConfig | None = None

    @classmethod
    def set(cls, config: TableConfig) -> None:
        cls._TABLE = config

    @classmethod
    def get(cls, table_config_path: Path | None = None) -> TableConfig:
        if cls._TABLE is None:
            cls._TABLE = TableConfig.load_from_file(table_config_path)
        return cls._TABLE
