# !/usr/bin/env python
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
# DESCRIPTION: This File contains general configuration settings, adjustable
#              by the user.
#
# =============================================================================
"""

from math import sqrt

#### Config output paths
out_figures = "output/figures/"
out_data = "output/data/"
ve = "venv/"

#### Set DB name
dbname = "DLMDWPMP01.db"

#### Log_Config
loglevel = "DEBUG"
setuploglevel = "DEBUG"
logpath = "output/logs"
logfile_prefix = "ffrunnerlog_"
setup_prefix = "setuplog_"

#### Required files
datafiles = {"ideal": "data/ideal.csv",
             "test": "data/test.csv",
             "train": "data/train.csv"}

progfiles = ["functionfinder/envfunctions.py",
             "functionfinder/datafunctions.py",
             "functionfinder/classes.py",
             "functionfinder/exceptionhandling.py",
             "functionfinder/log.py",
             "tests/test_unittest.py"]

#### Calculations


# Function to calculate error of training and ideal functions
def error_calculation(trainvalue, idealvalue):
    calcerror = sum((trainvalue - idealvalue)**2)
    return(calcerror)


# Factor for test data evaluation
factor = sqrt(2)
