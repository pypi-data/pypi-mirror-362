import sys
from logging import StreamHandler, getLogger

from dbnl.config import CONFIG

dbnl_logger = getLogger("dbnl.print")
dbnl_logger.setLevel(CONFIG.dbnl_log_level)
dbnl_logger.addHandler(StreamHandler(stream=sys.stdout))
