import sys
import os

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

from ghosttrackerpro.core import *
from ghosttrackerpro.core import LOGS_DIR, HEADERS, TIMEOUT, COMMON_PORTS, PLATFORMS
