import logging
import os
import random
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

"""Description
Defined the logger

Date: 2026-4-21
Created by oldmerman
"""

def setup_root_logger(env: str, log_dir: str = None):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    if env == "production":
        if log_dir is None:
            log_dir = "logs"

        os.makedirs(log_dir, exist_ok=True)

        random_num = f"{random.randint(10000000, 99999999)}"
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{date_str}_{random_num}.log"
        filepath = os.path.join(log_dir, filename)

        file_handler = RotatingFileHandler(
            filepath,
            maxBytes=1024 * 1024,
            backupCount=10,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        class InfoErrorFilter(logging.Filter):
            def filter(self, record):
                return record.levelno in (logging.INFO, logging.ERROR)

        file_handler.addFilter(InfoErrorFilter())

        root_logger.addHandler(file_handler)
        root_logger.setLevel(logging.INFO)

    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)
        root_logger.setLevel(logging.INFO)


def get_logger(name: str, log_dir: str = None) -> logging.Logger:
    env = os.getenv("ENVIRONMENT", "development").lower()

    if not logging.getLogger().handlers:
        setup_root_logger(env, log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if env == "development" else logging.INFO)

    return logger
