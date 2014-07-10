__author__ = 'Gareth'

import os

if not os.path.exists("control/logs"):
    os.mkdir("control/logs")

from control.utils import log
from control.system.manager import Manager

log.set_level()
log.open_log("output.log")

try:
    Manager()
finally:
    log.close_log("output.log")