#!/usr/bin/env python
# coding: utf-8

# TODO: Modify docstring

"""
# =============================================================================
# Created on Fri Nov 18 08:45:16 2022
# in Python version: python: 3.9.13 (main, Aug 25 2022, 23:51:50)
#
# AUTHOR: Georg Grunsky (georg.grunsky@iu-study.org)
#
# MODULE: DLMDWPM01
#
# DESCRIPTION: This File contains the logging configuration settings.
#
# =============================================================================
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

# specify logging-config
logging.basicConfig(filename=logfile, filemode="w",
                    format=logformat,
                    level=levels[setuploglevel])
