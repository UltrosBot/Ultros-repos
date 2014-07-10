__author__ = 'Gareth'

import os

from twisted.internet import reactor
import yaml

# import control.system.servers as servers
import control.system.ssl as ssl

from control.utils.log import getLogger
from control.system.singleton import Singleton

CONF_DIR = "control/config/"
DATA_DIR = "control/data/"
LOGS_DIR = "control/logs/"


class Manager(object):
    __metaclass__ = Singleton

    config = {}

    def __init__(self):
        self.logger = getLogger("Manager")

        try:
            self.logger.info("Ensuring directories exist..")
            self.create_dirs()
        except:
            self.logger.exception("Error while creating directories")
            return

        self.logger.info("Loading configuration..")
        if not self.load_config():
            self.logger.error("Unable to find control/config/config.yml")
            return

        try:
            self.logger.info("Ensuring SSL cert exists..")
            self.create_ssl()
        except:
            self.logger.exception("Error while creating SSL cert")
            return

        reactor.run()

    def create_dirs(self):
        paths = [CONF_DIR, DATA_DIR,
                 DATA_DIR + "ssl"]

        for path in paths:
            if not os.path.exists(path):
                self.logger.trace("Creating directory: %s" % path)
                os.mkdir(path)

    def load_config(self):
        if not os.path.exists(CONF_DIR + "config.yml"):
            return False

        self.config = yaml.load(open(CONF_DIR + "config.yml", "r"))

        return True

    def create_ssl(self):
        if not os.path.exists(DATA_DIR + "ssl/ssl.crt"):
            self.logger.trace("No SSL cert found; generating..")
            self.logger.info("Generating SSL cert. This may take a while.")
            ssl.create_self_signed_cert(
                DATA_DIR + "ssl",
                self.config.get("ssl", {})
            )
            self.logger.info("Done!")
        elif not os.path.exists(DATA_DIR + "ssl/ssl.key"):
            self.logger.trace("No private key found; generating..")
            self.logger.info("Generating SSL cert. This may take a while.")
            ssl.create_self_signed_cert(
                DATA_DIR + "ssl",
                self.config.get("ssl", {})
            )
            self.logger.info("Done!")
        else:
            self.logger.info("SSL cert and key found.")
