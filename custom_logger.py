import logging
from ext import data_path


# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s: [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(data_path.joinpath("script.log"))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)