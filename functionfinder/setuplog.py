#!/usr/bin/env python
# coding: utf-8
"""Definition of logging parameters for the installation process.

This script defines the basic logging configuration for the setup process of
this program. User configurable variables are read from 'config' module.
"""

import logging
import time
from .config import setuploglevel, logpath, setup_prefix

logfile = logpath + "/" + setup_prefix + time.strftime("%y%m%d_%H%M")


levels = {"DEBUG": logging.DEBUG,
          "INFO": logging.INFO,
          "WARN": logging.WARN,
          "ERROR": logging.ERROR,
          "CRITICAL": logging.CRITICAL}


logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def set_setuplogging():
    """Set predefined parameters for logging setup process."""
    logging.basicConfig(filename=logfile, filemode="w",
                        format=logformat,
                        level=levels[setuploglevel])
