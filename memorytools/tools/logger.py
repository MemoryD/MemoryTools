# -*- coding: utf-8 -*-

import logging
import logging.handlers
from sys import stdout
from pathlib import Path


class Logger(object):
    def __init__(self, log_level=logging.INFO, log_file=None):
        """
            指定日志级别，以及是否将日志存入到指定的文件中
        """
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] - %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        ch = logging.StreamHandler(stdout)
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=30)
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger


logger = Logger(log_file=Path("log/memorytools.log")).get_logger()

if __name__ == '__main__':
    # logger = Logger().get_logger()
    logger.debug("debug msg")
    logger.info('info msg')
    logger.warning('warn msg')
    logger.error('error msg')
    logger.critical('critical msg')
