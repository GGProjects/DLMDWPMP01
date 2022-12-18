#!/usr/bin/env python
# coding: utf-8

"""
# =========================================================================
# Created on Fri Nov 18 08:45:16 2022
# in Python version: python: 3.9.13 (main, Aug 25 2022, 23:51:50)
#
# AUTHOR: Georg Grunsky (georg.grunsky@iu-study.org)
#
# MODULE: DLMDWPM01
#
# DESCRIPTION: This is the main programm for mentioned MODULE.
#
# PURPOSE:
#   Evaluate ideal functions for a set of training data (1) and assign
#   values of a test-dataset to those ideal functions (2)
#
# DETAILS:
#    Used criteria for evaluation:
#     (1) to match training data and ideal functions:
#         minimum MeanSquaredError (MSE)
#     (2) to match ideal functions and test data:
#         precalculated MSE (1) * SquareRoot(2)
#
# =========================================================================
"""

import sys
from setuptools import setup, find_packages
from unittest import TestLoader, TestResult
from pathlib import Path

try:
    from functionfinder.log import logging
    from functionfinder.config import datafiles, progfiles
except ImportError:
    print("Initially required modules not found.")
    sys.exit("Please ensure complete download of this package")

# Log DocString and start of setup
logging.info(__doc__)
logging.info("Starting setup of functionfinder:")


# Define function to check required files
def check_required_files(files):
    """
    Check for specifically required files to run program.

    Arguments_
        Input is a string, a list or a dictonary with filepaths to check.
        In case of a dictionary, the filepaths have to be stored in the
        values.
        The filepath in the given argument hast to be relative
        to the current working directory.
    """
    if isinstance(files, dict):
        files = list(files.values())

        missing = list()

        for i in files:
            if not Path.is_file(Path(i)):
                print("Fehlende Datei: " + i)
                missing.append(i)

        if not len(missing) == 0:
            # Write Log
            logging.critical("Missing File(s): %s", missing)
            # Stop execution
            sys.exit("Missing files! Please consult logfile.")
    else:
        logging.info("All required files available")


# Define function to run unit-tests
def run_tests():
    """
    Run UnitTests specified in tests-directory.

    This is done to ensure functionality of this package before installation.
    Test from tests-directory will be loaded as a test suite and run
    before execution of setup-method.

    """
    test_loader = TestLoader()
    test_result = TestResult()
    test_directory = str('tests')

    test_suite = test_loader.discover(test_directory, pattern='test_*.py')
    test_suite.run(result=test_result)
    test_result.unexpectedSuccesses

    if test_result.wasSuccessful():
        logging.info("UnitTests successful")
        logging.debug(test_result)
        if "test_table_from_csv" in str(test_result.unexpectedSuccesses):
            logging.info("Direct import from csv to SQLite is possible.\n",
                         "Host seems to be able to handle",
                         "large csv files easily.")
    else:
        logging.info("UnitTests not successful.\n",
                     "Failed: ", test_result.failures,
                     "Errors: ", test_result.errors)
        #sys.exit("UnitTests not successful")


# Check required files
check_required_files(datafiles)
check_required_files(progfiles)

# Execute UnitTests
run_tests()

# Setup package
setup(
    name='functionfinder',
    version='1.0.0',
    description='Solve task in DLMDWPMP01 python course of www.iu.de ',
    author='Georg Grunsky',
    author_email='georg.grunsky@iu-study.org',
    packages=find_packages(include=['functionfinder']),
    # install_requires=['pandas==0.23.3','numpy>=1.14.5'],
    extras_require={'plotting': ['matplotlib>=2.2.0', 'jupyter']},
    entry_points={
        'console_scripts': ['ff = functionfinder.ffrunner:main']
    }  # ,
    # package_data={'exampleproject': ['data/schema.json']}
)

logging.info("Setup of functionfinder successfull")
