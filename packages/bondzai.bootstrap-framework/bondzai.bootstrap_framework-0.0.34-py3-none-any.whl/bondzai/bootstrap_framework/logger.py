import logging
import time
import sys


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger()
logging.Formatter.converter = time.localtime
logger.setLevel(logging.INFO)
