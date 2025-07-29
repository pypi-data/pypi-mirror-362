from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .version import __version__

import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")