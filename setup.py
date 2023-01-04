#!/usr/bin/env python
# coding: utf-8
"""Docstring for package-setup.

This script installs the functionfinder package and can be called using
'pip install -e .' from within the package root directory.
The main effort of this package is to gain basic python programming skills
and therefore solve a simple classification task. This package is designed to
fulfill the given task and complete the IU Python Module 'DLMDWPMP01'.

Methods
-------
check_required_files(files)
    Check for specifically required files to run program.
run_tests()
    Run UnitTests specified in tests-directory.
"""
# =============================================================================
# Import modules
# =============================================================================
import sys
from setuptools import setup, find_packages
from unittest import TestLoader, TestResult
from pathlib import Path

# =============================================================================
# Try importing own modules, if availaible
# =============================================================================
try:
    from functionfinder.setuplog import logging
    from functionfinder.config import datafiles, progfiles
except ImportError:
    print("Initially required modules not found.")
    sys.exit("Please ensure complete download of this package")

# =============================================================================
# Define logger for setup process and start logging
# =============================================================================
logger = logging.getLogger('ff-setup')

# Log DocString and start of setup process
logger.info(__doc__)
logger.info("Starting setup of functionfinder")

# =============================================================================
# Define additional functions
# =============================================================================


def check_required_files(files):
    """Check for specifically required files to run program.

    Parameters
    ----------
    files : string, list or dictionary
        This parameter contains filepaths to check for existance.
        In case of a dictionary, the filepaths have to be stored in the
        values.
        The filepath in the given argument has to be relative
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
            logger.critical("Missing File(s): %s", missing)
            # Stop execution
            sys.exit("Missing files! Please consult logfile.")
    else:
        logger.info("All required files available")


def run_tests():
    """Run UnitTests specified in tests-directory.

    This is done to ensure functionality of this package before installation.
    Tests from tests-directory will be loaded as a test suite and run
    before execution of setup-method.

    """
    logger.info("Start UnitTests")
    test_loader = TestLoader()
    test_result = TestResult()
    test_directory = str('tests')

    test_suite = test_loader.discover(test_directory, pattern='test_*.py')
    test_suite.run(result=test_result)

    # Evaluators
    success = len(test_result.failures) == 0 & len(test_result.errors) == 0
    csv_to_sql = "test_table_from_csv" in str(test_result.unexpectedSuccesses)
    print(csv_to_sql)

    if csv_to_sql:
        logtext = ("Direct import from csv to SQLite is possible. " +
                   "Host seems to be able to handle" +
                   "large csv files easily.")
        logger.info(logtext)
        print(logtext)

    if success:
        logger.info("UnitTests successful")
        print("UnitTests successful")
        logger.debug(test_result)

    else:
        logger.critical("UnitTests not successful.")
        logger.critical("Failed: %s", test_result.failures)
        logger.critical("Errors: %s", test_result.errors)
        sys.exit("UnitTests not successful")


# =============================================================================
# Check required files
# =============================================================================
logtext = "Check for required files"
logger.info(logtext)
print(logtext)
check_required_files(datafiles)
check_required_files(progfiles)

# =============================================================================
# Setup package
# =============================================================================
logtext = "Start installing required packages"
logger.info(logtext)
print(logtext)

setup(
    name='functionfinder',
    version='1.0.0',
    description='Solve task in DLMDWPMP01 python course of www.iu.de ',
    author='Georg Grunsky',
    author_email='georg.grunsky@iu-study.org',
    packages=find_packages(include=['functionfinder']),
    install_requires=['matplotlib==3.6.2',
                      'pandas==1.5.2',
                      'seaborn==0.12.1',
                      'setuptools==65.5.0'],
    entry_points={
        'console_scripts': ['ff = functionfinder.ffrunner:task']
    }
)

# =============================================================================
# Execute UnitTests
# =============================================================================
logtext = "Execute UnitTexts"
logger.info(logtext)
print(logtext)
run_tests()

# =============================================================================
# Finish setup
# =============================================================================
logger.info("Setup of functionfinder successfull")
print("Setup successfully finished")
print("Please check setup-log in folder logs for further details.")
print("You can now run \"ff\" to start programm!")
