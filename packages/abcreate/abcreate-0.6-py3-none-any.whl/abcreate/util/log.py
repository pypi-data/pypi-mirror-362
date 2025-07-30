# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
import logging
import os


class ExitOnCriticalHandler(logging.StreamHandler):
    def emit(self, record):
        if record.levelno == logging.CRITICAL:
            raise SystemExit(1)


class CollectStatisticsHandler(logging.StreamHandler):
    message_counter: dict[int, int] = dict()

    def __init__(self):
        super().__init__()
        self.messages = dict()
        for level in (
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ):
            self.messages[level] = 0

    def emit(self, record):
        try:
            self.messages[record.levelno] += 1
        except KeyError:
            self.messages[record.levelno] = 1

    @property
    def errors(self) -> int:
        return self.messages[logging.ERROR]

    @property
    def warnings(self) -> int:
        return self.messages[logging.WARNING]


class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function_at_module = f"{self.name}:{self.funcName}"


logstats = CollectStatisticsHandler()


def setup_logging(logfile: Path) -> None:
    level = os.environ.get("ABCREATE_LOGLEVEL", "INFO").upper()

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(level)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)-23s | %(name)-14s | %(funcName)-20s | %(levelname)-8s | %(message)s"
        )
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(
        logging.Formatter(
            "%(asctime)-23s [%(function_at_module)-18s] %(levelname)s: %(message)s"
        )
    )
    logging.setLogRecordFactory(CustomLogRecord)
    logging.basicConfig(
        level=level,
        handlers=[
            file_handler,
            stream_handler,
            logstats,
            ExitOnCriticalHandler(),
        ],
    )
