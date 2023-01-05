#!/usr/bin/env python
# coding: utf-8
"""Docstring for test_unit.py.

This script contains sets of UnitTests to check the functionality of the
functionfinder package and is called during the setup process by setup.py.

Notes
-----
Tests of the calculation functions have not been written, due to the fact that
calculation functions are, by the author, meant to be open for modification and
therefore cannot be tested with specific values.

TestSets
--------
test_sqlite
    Test data functions with regards to SQLite operations.
test_df
    Test basic data properties such as the structure of provided data files.

Methods
-------
check_struct(structdata)
    Check structure of a passed DataFrame to certain needs. Used in test_df
    TestSet.
"""

import unittest
from pathlib import Path
import pandas as pd
import sqlite3

from functionfinder.datafunctions import create_empty_sqlitedb
from functionfinder.datafunctions import csv2sql_directly, csv2sql_pandas
from functionfinder.config import out_data, datafiles


def check_struct(structdata):
    """Check structure of passed DataFrame to certain needs.

    Check if column of name 'x' exists and if the number of columns is at
    least two.

    Parameters
    ----------
    structdata : pandas.DataFrame
        DataFrame to check for above criteria.

    Returns
    -------
    checkresult : bool
        If True, all checks were passed.
    """
    checklength = len(structdata.axes[1]) >= 2  # check column number
    check_x_exists = "x" in structdata.axes[1]  # check if "x" exists
    checkresult = checklength & check_x_exists  # combine above checks
    return(checkresult)


# =============================================================================
# SQLite Testset
# =============================================================================


class test_sqlite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Execute before running tests of this class."""
        cls.db = str('testdb')  # db name to test functionality
        cls.testtable = str("testtable")  # db table name to test functionality

        # create example csv to test db operations
        cls.testcsv = str(out_data + "testdata.csv")
        my_dic = {"Name": ['Bernd', 'Silke', 'Claudia'],
                  "Alter": [54, 36, 23],
                  "Lieblingszahl": [25, 7, 43]}
        my_df = pd.DataFrame(my_dic,
                             index=['1001', '1002', '1003'])
        my_df.to_csv(cls.testcsv, encoding="utf-8")

    def setUp(self):
        """Execute everytime before running a test of this class."""
        pass

    def test_creation(self):
        """Test creation of empty sqlite database."""
        create_empty_sqlitedb(self.db)
        self.assertTrue(Path.is_file(Path(out_data + self.db)),
                        "no database was created")

    @unittest.expectedFailure
    def test_table_from_csv(self):
        """Test import of csv files to SQLite using subprocess.

        Test csv2sql_directly function inside the module datafunctions.py.
        This Test is expected to fail, therefore a @expectedFailure decorator
        was placed. In case of success, a log-file entry gets printed during
        the setup process. Success would suggest, that the system is able to
        handle extremely large csv files, due to the possibility to directly
        write those files to the SQLite database.
        """
        csv2sql_directly(self.db, self.testcsv, self.testtable)

        # Test success by reimporting written dataset using pandas and checking
        # the existance by asserting the right instance.
        con = sqlite3.connect(out_data + self.db)
        sqldata = pd.read_sql_query("SELECT * from " + self.testtable, con)
        con.close()
        print(type(sqldata))
        self.assertIsInstance(sqldata, pd.DataFrame,
                              "Could not reimport table from direct DB-entry")

    def test_table_from_pandas(self):
        """Test import of csv files to SQLite using pandas.

        Test csv2sql_pandas function of module datafunction.py
        """
        csv2sql_pandas(self.db, self.testcsv, self.testtable)

        # Test success by reimporting written dataset using pandas and checking
        # the existance by asserting the right instance.
        con = sqlite3.connect(out_data + self.db)
        df = pd.read_sql_query("SELECT * from " + self.testtable, con)
        con.close()
        self.assertIsInstance(df, pd.DataFrame,
                              "Could not reimport table from Pandas-DB-entry")

    def tearDown(self):
        """Execute everytime after running a test of this class."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Execute after running  all tests of this class.

        Try deleting created files during testing process. Pass if deletion is
        not possible. The existance of test-files can be accepted an has no
        negative effect on the result of the main program.
        """
        try:
            Path.unlink(Path(out_data + cls.db))  # delete test database
            Path.unlink(Path(cls.testcsv))  # delete test csv file
        except PermissionError:
            pass


# =============================================================================
# DataFunctions Testset
# =============================================================================


class test_df(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Execute before running tests of this class."""
        cls.testdf = pd.read_csv(datafiles['test'])
        cls.traindf = pd.read_csv(datafiles['train'])
        cls.idealdf = pd.read_csv(datafiles['ideal'])

    def setUp(self):
        """Execute everytime before running a test of this class."""
        pass

    def test_teststruct(self):
        """Test structure of test dataset."""
        testcheck = check_struct(self.testdf)
        self.assertTrue(testcheck,
                        "Test dataset has wrong structure.")

    def test_trainstruct(self):
        """Test structure of train dataset."""
        traincheck = check_struct(self.traindf)
        self.assertTrue(traincheck,
                        "Train dataset has wrong structure.")

    def test_idealstruct(self):
        """Test structure of ideal dataset."""
        idealcheck = check_struct(self.idealdf)
        self.assertTrue(idealcheck,
                        "Ideal dataset has wrong structure.")

    def test_trainideal_length(self):
        """Test if train dataset and ideal dataset are of same length.

        Same length is needed to execute error calculation by conducting a math
        operation to two pandas.Series objects.
        """
        lengthcheck = len(self.traindf) == len(self.idealdf)
        self.assertTrue(lengthcheck,
                        "Train and ideal datasets are not of the same length.")

    def tearDown(self):
        """Execute everytime after running a test of this class."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Execute after running all tests of this class."""
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
