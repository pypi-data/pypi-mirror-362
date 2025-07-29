import argparse
import asyncio
import logging
import socket
from pathlib import Path
from threading import Event, Thread

import uvicorn

from lite_dist2.config import TableConfigProvider
from lite_dist2.curriculum_models.curriculum import CurriculumProvider
from lite_dist2.table_node_api.api import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        logger.warning("Cannot reach DNS Server. It may show localhost IP.")
        return socket.gethostbyname(socket.gethostname())


async def _periodic_save() -> None:
    interval = TableConfigProvider.get().curriculum_save_interval_seconds
    while True:
        await asyncio.sleep(interval)
        logger.info("Performing periodic save of curriculum data")
        await CurriculumProvider.save_async()


def _run_periodic_save() -> None:
    asyncio.run(_periodic_save())


async def _periodic_timeout_check() -> None:
    interval = TableConfigProvider.get().timeout_check_interval_seconds
    while True:
        await asyncio.sleep(interval)
        logger.info("Performing periodic timeout check of trials")
        await CurriculumProvider.check_timeout()


def _run_periodic_timeout_check() -> None:
    asyncio.run(_periodic_timeout_check())


def start() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to table node config file.", type=str, default=None)
    args = parser.parse_args()
    table_config_path = None if args.config is None else Path(args.config)

    logger.info("Table Node IP: %s", _get_local_ip())
    table_config = TableConfigProvider.get(table_config_path)

    # save thread
    save_thread = Thread(target=_run_periodic_save, daemon=True)
    save_thread.start()

    # timeout check thread
    timeout_thread = Thread(target=_run_periodic_timeout_check, daemon=True)
    timeout_thread.start()

    port = table_config.port
    uvicorn.run(app, host="0.0.0.0", port=port)  # noqa: S104


class StoppableThread(Thread):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self) -> None:
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()


def start_in_thread() -> StoppableThread:
    table_thread = StoppableThread(target=start, daemon=True)
    table_thread.start()
    return table_thread


if __name__ == "__main__":
    start()
