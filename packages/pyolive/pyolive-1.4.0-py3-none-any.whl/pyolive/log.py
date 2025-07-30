import os
import sys
import socket
import queue
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime
from typing import Optional
from .config import Config


def get_log_level(level_str: str) -> int:
    if level_str == 'info':
        level = logging.INFO
    elif level_str == 'warn':
        level = logging.WARNING
    elif level_str == 'error':
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return level


class AgentLog:
    def __init__(self, agent: str):
        self.agent: str = agent
        self.log_queue: queue.Queue = queue.Queue()
        self.listener: Optional[logging.handlers.QueueListener] = None
        self.logger: Optional[logging.Logger] = None
        self.home: Optional[str] = os.getenv('ATHENA_HOME')
        self._init_logger()

    def _init_logger(self) -> None:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        config = Config('athena-agent.yaml')
        level: int = get_log_level(config.get_value('log/level'))
        count: int = self._get_log_count(config.get_value('log/rotate'))
        size: int = self._get_log_bytes(config.get_value('log/size'))
        name: str = self._get_log_name()

        file_handler = RotatingFileHandler(filename=name, maxBytes=size, backupCount=count)
        file_handler.setFormatter(formatter)

        self.listener = logging.handlers.QueueListener(self.log_queue, file_handler)
        self.listener.start()

        queue_handler = logging.handlers.QueueHandler(self.log_queue)

        self.logger = logging.getLogger(self.agent)
        self.logger.setLevel(level)
        self.logger.addHandler(queue_handler)
        self.logger.propagate = False

    def get_logger(self) -> logging.Logger:
        return self.logger

    def close(self) -> None:
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _get_log_count(self, rotate_str: str) -> int:
        return int(rotate_str)

    def _get_log_bytes(self, size_str: str) -> int:
        i = size_str.find('kb')
        if i > 0:
            return int(size_str[:i]) * 1024
        i = size_str.find('mb')
        if i > 0:
            return int(size_str[:i]) * 1024 * 1024
        i = size_str.find('gb')
        if i > 0:
            return int(size_str[:i]) * 1024 * 1024 * 1024
        return 0

    def _get_log_name(self) -> str:
        path = os.path.join(self.home, 'logs', 'agent')
        os.makedirs(path, exist_ok=True)
        file = self.agent + '@' + socket.gethostname() + '.log'
        return os.path.join(path, file)


class AppLog:
    def __init__(self, app: str, devel: bool = False):
        self.app: str = app
        self.devel: bool = devel
        self.home: Optional[str] = os.getenv('ATHENA_HOME')
        self.logger: logging.Logger = self._get_or_create_logger()

    def _get_or_create_logger(self) -> logging.Logger:
        formatter = logging.Formatter('%(asctime)s %(levelname)s #(%(thread)s) %(message)s')

        if not self.devel:
            logger = logging.getLogger(self.app)
            if not logger.handlers:
                config = Config('athena-app.yaml')
                level: int = get_log_level(config.get_value('log/level'))
                date_fmt: str = config.get_value('log/path').strip('{}')
                path: str = os.path.join(self.home, 'logs', 'app')
                file: str = self.app + '@' + socket.gethostname() + '.log'

                file_handler = CustomTimedRotatingFileHandler(path, file, date_fmt)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                logger.setLevel(level)
                logger.propagate = False
        else:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
        self,
        base_dir: str,
        filename: str,
        date_format: str,
        when: str = 'midnight',
        interval: int = 1,
        backupCount: int = 0
    ):
        self.base_dir: str = base_dir
        self.date_format: str = date_format
        self.filename: str = filename
        self.update_log_dir()
        log_filename: str = os.path.join(self.log_dir, filename)
        super().__init__(log_filename, when=when, interval=interval, backupCount=backupCount)

    def update_log_dir(self) -> None:
        current_time: str = datetime.now().strftime(self.date_format)
        self.log_dir: str = os.path.join(self.base_dir, current_time)
        os.makedirs(self.log_dir, exist_ok=True)

    def doRollover(self) -> None:
        self.update_log_dir()
        self.baseFilename = os.path.join(self.log_dir, self.filename)
        super().doRollover()