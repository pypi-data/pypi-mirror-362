import logging
import os


def setup_logging():
    logging.basicConfig(
        level=os.environ.get("OPEN_MINDED_LOG_LEVEL") or logging.ERROR,
        format="%(asctime)s: [%(levelname)s] %(name)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
