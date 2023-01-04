# !/usr/bin/env python
# coding: utf-8
"""Docstring for module config.py.

This script contains definitions of configurable elements for the
functionfinder package and should be adjusted to your own needs before running
the program.

It provides variables to configure
    output paths,
    the name of the database,
    logging configuration,
    required files (checked at setup),
    a dictionary to match datafiles to specified keys,
    the functiondefinition for the errorcalculation of train and ideal data,
    the factor to modify the calculated error when evaluating test data.

Methods
-------
error_calculation(trainvalue, idealvalue)
    Calculate error rate between to given pandas-series objects of same length.
"""

from math import sqrt

# =============================================================================
# Config output paths
# =============================================================================
out_figures = "output/figures/"
out_data = "output/data/"

# =============================================================================
# Set DB name
# =============================================================================
dbname = "DLMDWPMP01.db"

# =============================================================================
#  Log_Config
# =============================================================================
loglevel = "DEBUG"
setuploglevel = "DEBUG"
logpath = "output/logs"
logfile_prefix = "ffrunnerlog_"
setup_prefix = "setuplog_"

# =============================================================================
# Required files
# =============================================================================
datafiles = {"ideal": "data/ideal.csv",
             "test": "data/test.csv",
             "train": "data/train.csv"}

progfiles = ["functionfinder/ffrunner.py",
             "functionfinder/config.py",
             "functionfinder/datafunctions.py",
             "functionfinder/classes.py",
             "functionfinder/setuplog.py",
             "functionfinder/log.py",
             "tests/test_unit.py"]


# =============================================================================
# Calculations
# =============================================================================
def error_calculation(trainvalue, idealvalue):
    r"""Calculate an error-value between two pandas Series.

    The method is called by datafunctions.min_error method
    and can modified to test different calculation algorithms.

    Parameters
    ----------
    trainvalue : pandas Series
        Specific Y-Data column of a trainingdata DataFrame.
        (has to have the same length as idealvalue!)
    idealvalue : pandas Series
        Specific Y-Data column of a idealdata DataFrame.
        (has to have the same length as idealvalue!)

    Returns
    -------
    calcerror : float
        Calculated error value of the provided two pandas Series

    Notes
    -----
    By default the provided algorithm is the summed squared error (SSE)
    of the provided pandas Series.

    .. math:: \sum_{i=1}^{n}(TrainingData_{i} - IdealFunction_{i})^2
    """
    calcerror = sum((trainvalue - idealvalue)**2)
    return(calcerror)


# Factor for test data evaluation w/ regards to calculated
# error of training data
factor = sqrt(2)
