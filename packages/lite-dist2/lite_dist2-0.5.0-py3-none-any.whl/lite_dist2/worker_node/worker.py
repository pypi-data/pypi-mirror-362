from __future__ import annotations

import logging
import time
import uuid
from typing import TYPE_CHECKING, Annotated

from lite_dist2.expections import LD2TableNodeServerError
from lite_dist2.worker_node.table_node_client import TableNodeClient

if TYPE_CHECKING:
    from multiprocessing.pool import Pool

    from lite_dist2.config import WorkerConfig
    from lite_dist2.worker_node.trial_runner import BaseTrialRunner


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Worker:
    def __init__(
        self,
        trial_runner: Annotated[BaseTrialRunner, "Runner for executing trials"],
        ip: Annotated[str, "IP address of the table node server"],
        port: Annotated[int | str, "Port number  of the table node server"],
        config: Annotated[WorkerConfig, "Configuration of  the worker node"],
        pool: Annotated[
            Pool | None,
            "Process pool for parallel execution. Ignored except `SemiAutoMPTrialRunner`.",
        ] = None,
    ) -> None:
        self.trial_runner = trial_runner
        self.client = TableNodeClient(ip, port)
        self.pool = pool
        self.config = config
        self.id = str(uuid.uuid1())

    def start(self, stop_at_no_trial: bool = False, *args: object, **kwargs: object) -> None:
        if not self.client.ping():
            msg = "Table node server not responding"
            raise LD2TableNodeServerError(msg)

        while True:
            has_next = self._step(*args, **kwargs)
            if (not has_next) and stop_at_no_trial:
                logger.info("No trial. Stop worker after saving.")
                self.client.save()
                return
            if not has_next:
                logger.info("No trial. Waiting %d seconds...", self.config.wait_seconds_on_no_trial)
                time.sleep(self.config.wait_seconds_on_no_trial)

    def _step(self, *args: object, **kwargs: object) -> bool:
        trial = self.client.reserve_trial(
            self.id,
            self.config.name,
            self.config.max_size,
            self.config.retaining_capacity,
            self.config.table_node_request_timeout_seconds,
        )
        if trial is None:
            return False

        kwargs |= trial.const_param.to_dict() if trial.const_param is not None else {}
        done_trial = self.trial_runner.run(trial, self.config, self.pool, *args, **kwargs)
        self.client.register_trial(done_trial, self.config.table_node_request_timeout_seconds)
        return True
