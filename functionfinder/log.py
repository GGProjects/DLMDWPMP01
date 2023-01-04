#!/usr/bin/env python
# coding: utf-8



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

# specify logging-config
logging.basicConfig(filename=logfile, filemode="w",
                    format=logformat,
                    level=levels[loglevel])
