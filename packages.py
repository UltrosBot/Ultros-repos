__author__ = 'Gareth'

import os

if not os.path.exists("packages/logs"):
    os.mkdir("packages/logs")

from packages.utils import log
# from packages.system.manager import Manager

log.set_level()
log.open_log("output.log")

try:
    # Manager()
    pass
finally:
    log.close_log("output.log")