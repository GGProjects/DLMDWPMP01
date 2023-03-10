#!/usr/bin/env python
# coding: utf-8
"""Definition of logging parameters.

This script defines the basic logging configuration for the main program.
User configurable variables are read from 'config' module.
"""


import logging
import time
from .config import loglevel, logpath, logfile_prefix

logfile = logpath + "/" + logfile_prefix + time.strftime("%y%m%d_%H%M")


levels = {"DEBUG": logging.DEBUG,
          "INFO": logging.INFO,
          "WARN": logging.WARN,
          "ERROR": logging.ERROR,
          "CRITICAL": logging.CRITICAL}


logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def setlogging():
    """Set predefined parameters for logging."""
    logging.basicConfig(filename=logfile, filemode="w",
                        format=logformat,
                        level=levels[loglevel])

