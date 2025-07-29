import binascii
import hashlib
import time
from pathlib import Path

from lite_dist2.config import TableConfig, TableConfigProvider, WorkerConfig
from lite_dist2.curriculum_models.study_portables import StudyRegistry
from lite_dist2.study_strategies import StudyStrategyModel
from lite_dist2.study_strategies.base_study_strategy import StudyStrategyParam
from lite_dist2.suggest_strategies import SuggestStrategyModel
from lite_dist2.suggest_strategies.base_suggest_strategy import SuggestStrategyParam
from lite_dist2.table_node_api.start_table_api import start_in_thread
from lite_dist2.table_node_api.table_param import StudyRegisterParam
from lite_dist2.type_definitions import RawParamType, RawResultType
from lite_dist2.value_models.aligned_space_registry import LineSegmentRegistry, ParameterAlignedSpaceRegistry
from lite_dist2.value_models.point import ScalarValue
from lite_dist2.worker_node.table_node_client import TableNodeClient
from lite_dist2.worker_node.trial_runner import AutoMPTrialRunner
from lite_dist2.worker_node.worker import Worker


def set_table_config() -> None:
    config = TableConfig(
        port=8000,
        curriculum_path=Path(__file__).parent / "example_curriculum.json",
        curriculum_save_interval_seconds=10,
    )
    TableConfigProvider.set(config)


def register_study(table_ip: str, table_port: int) -> None:
    _resolution = 10
    _half_size = 2.0

    study_register_param = StudyRegisterParam(
        study=StudyRegistry(
            name="preimage",
            required_capacity=set(),
            study_strategy=StudyStrategyModel(
                type="find_exact",
                study_strategy_param=StudyStrategyParam(
                    target_value=ScalarValue(
                        type="scalar",
                        value_type="int",
                        value="0x49f68a5c8493ec2c0bf489821c21fc3b",
                    ),
                ),
            ),
            suggest_strategy=SuggestStrategyModel(
                type="sequential",
                suggest_strategy_param=SuggestStrategyParam(strict_aligned=True),
            ),
            result_type="scalar",
            result_value_type="int",
            const_param=None,
            parameter_space=ParameterAlignedSpaceRegistry(
                type="aligned",
                axes=[
                    LineSegmentRegistry(
                        name="x",
                        type="int",
                        size=None,
                        step="0x1",
                        start="0x0",
                    ),
                ],
            ),
        ),
    )
    client = TableNodeClient(table_ip, table_port)
    client.register_study(study_register_param)


class MD5Preimage(AutoMPTrialRunner):
    def func(self, parameters: RawParamType, *_: object, **__: object) -> RawResultType:
        preimage = int(parameters[0])
        hex_digest = hashlib.md5(self.to_bytes(preimage)).hexdigest()  # noqa: S324
        return self.from_hex(hex_digest)

    @staticmethod
    def to_bytes(val: int) -> bytes:
        hex_str = hex(val)[2:]
        if len(hex_str) % 2 == 1:
            hex_str = "0" + hex_str
        return binascii.unhexlify(hex_str)

    @staticmethod
    def from_hex(hex_str: str) -> int:
        return int("0x" + hex_str, base=16)


def run_worker(table_ip: str, table_port: int) -> None:
    worker_config = WorkerConfig(
        name="w_01",
        process_num=2,
        max_size=2000,
        wait_seconds_on_no_trial=5,
        table_node_request_timeout_seconds=60,
    )
    worker = Worker(
        trial_runner=MD5Preimage(),
        ip=table_ip,
        port=table_port,
        config=worker_config,
    )
    worker.start(stop_at_no_trial=True)


if __name__ == "__main__":
    # 1. Set table config for example
    #    Execution node type in normal use: Table
    #    NOTE: For normal use, change the `table_config.json` file in the root directory.
    set_table_config()

    # 2. Start table node in other thread
    #    Execution node type in normal use: Table
    #    NOTE: In most cases, use `start()` (or `uv run start`) instead of `start_in_thread()`
    #          since table nodes and worker nodes are separated.
    table_thread = start_in_thread()
    time.sleep(1)  # wait for activate

    # 3. Register study to table node
    #    Execution node type in normal use: Management
    #    NOTE: If the management node is also a worker node or a table node,
    #          `TableNodeClient.register_study` is available.
    #          Otherwise, studies can be registered using the curl command.
    register_study(table_ip="127.0.0.1", table_port=8000)

    # 4. run worker node
    #    Execution node type in normal use: Worker
    #    NOTE: In this example, the entire process should be completed within 10 seconds.
    #          10 seconds later, example_curriculum.json should be saved in the same directory as this file.
    #          The saving interval can be changed from the `TableConfig.curriculum_save_interval_seconds`.
    run_worker(table_ip="127.0.0.1", table_port=8000)

    # 5. Stop table node
    #    Execution node type in normal use: Table
    #    NOTE: Used to explicitly terminate a table node.
    #          In this example, however, the node is running on a daemon thread,
    #          so there is no need to terminate it explicitly.
    # table_thread.stop()
    # table_thread.join()
