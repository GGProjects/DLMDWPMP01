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

import unittest
from pathlib import Path
from functionfinder.datafunctions import create_empty_sqlitedb
from functionfinder.datafunctions import csv2sql_directly, csv2sql_pandas
import pandas as pd
from functionfinder.config import out_data


# =============================================================================
# SQLite Testset
# =============================================================================


class test_sqlite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        

        Parameters
        ----------
        cls : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        cls.db = str('testdb')
        cls.testcsv = str(out_data + "testdata.csv")
        my_dic = {"Name": ['Bernd', 'Silke', 'Claudia'],
                  "Alter": [54, 36, 23],
                  "Lieblingszahl": [25, 7, 43]}
        my_df = pd.DataFrame(my_dic,
                             index=['1001', '1002', '1003'])
        my_df.to_csv(cls.testcsv, encoding="utf-8")
        cls.testtable = str("testtable")

    def setUp(self):
        """
        

        Returns
        -------
        None.

        """
        pass

    def test_creation(self):
        """
        

        Returns
        -------
        None.

        """
        create_empty_sqlitedb(self.db)
        self.assertTrue(Path.is_file(Path(out_data + self.db)),
                        "no database was created")

    @unittest.expectedFailure
    def test_table_from_csv(self):
        """
        

        Returns
        -------
        None.

        """
        import sqlite3
        import pandas as pd
        csv2sql_directly(self.db, self.testcsv, self.testtable)
        con = sqlite3.connect(out_data + self.db)
        df = pd.read_sql_query("SELECT * from " + self.testtable, con)
        con.close()
        self.assertIsInstance(df, pd.DataFrame,
                              "Could not reimport table from direct DB-entry")

    def test_table_from_pandas(self):
        """
        

        Returns
        -------
        None.

        """
        import sqlite3
        import pandas as pd
        csv2sql_pandas(self.db, self.testcsv, self.testtable)
        con = sqlite3.connect(out_data + self.db)
        df = pd.read_sql_query("SELECT * from " + self.testtable, con)
        con.close()
        self.assertIsInstance(df, pd.DataFrame,
                              "Could not reimport table from Pandas-DB-entry")

    def tearDown(self):
        """
        

        Returns
        -------
        None.

        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        

        Parameters
        ----------
        cls : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        try:
            Path.unlink(Path(out_data + cls.db))
            Path.unlink(Path(cls.testcsv))
        except PermissionError:
            pass


# =============================================================================
# DataFunctions Testset
# =============================================================================

# add structure tests (spaltenanzahl, gleiche zeilenlänge ideal und train)

# =============================================================================
# class test_df(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         pass
# 
#     def setUp(self):
#         # self.plotname = "unittest_plot.png"
#         pass
# 
# =============================================================================
# =============================================================================
#     def test_plot_frame(self):
#         plotname = "output/figures/unittest_plot.pdf"
#         x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#         y = {"y1": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
#              "y2": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]}
#         plot_frame("X", "Y", "Testplot", x, y, filename=plotname)
#         
#         # generate plot w/ example data
#         
#         #ax.plot(x, y, label="line plot example", linewidth=2)
#         # Save plot
#         plt.savefig(fname=Path(plotname))
#         
#         # Assert existance of plot
#         self.assertTrue(Path.is_file(Path(self.plotname)),
#                         "no plot was created")
# =============================================================================
# =============================================================================
#     def test_table_from_pandas(self):
#         import sqlite3
#         import pandas as pd
#         csv2sql_pandas(self.db, self.testcsv, self.testtable)
#         con = sqlite3.connect(self.db)
#         df = pd.read_sql_query("SELECT * from " + self.testtable, con)
#         self.assertIsInstance(df, pd.DataFrame,
#                               "Could not reimport table from Pandas-DB-entry"
# =============================================================================
# =============================================================================
#     def tearDown(self):
#         # Path.unlink(Path(self.plotname))
#         pass
# 
#     @classmethod
#     def tearDownClass(cls):
#         pass
# =============================================================================
