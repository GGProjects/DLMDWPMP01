#!/usr/bin/env python
# coding: utf-8

"""
# =============================================================================
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
# =============================================================================
"""

from pathlib import Path
import subprocess
from functionfinder.config import out_data

def create_empty_sqlitedb(dbname):
    dbpath = out_data + dbname
    if Path.is_file(Path(dbpath)):
        Path.unlink(Path(dbpath))
    Path(dbpath).touch()


def csv2sql_directly(existing_db, csv_toadd, tablename):
    db_name = Path(str(out_data + existing_db)).resolve()
    csv_file = Path(csv_toadd).resolve()
    result = subprocess.run(['sqlite3',
                             str(db_name),
                             '-cmd',
                             '.mode csv',
                             '.import ' + str(csv_file).replace('\\', '\\\\')
                             + ' ' + str(tablename)],
                            capture_output=True)


def csv2sql_pandas(existing_db, csv_toadd, tablename):
    import pandas as pd
    import sqlite3
    conn = sqlite3.connect(str(out_data + existing_db))
    pd.read_csv(csv_toadd).to_sql(tablename, conn,
                                  if_exists='replace', index=False)
    conn.close()


def min_error(train_set, ideal_df):
    import pandas as pd
    from .config import error_calculation

    last_val = "not_set"
    for i in ideal_df.axes[1][1:]:
        tmp_val = error_calculation(trainvalue=pd.to_numeric(train_set),
                                    idealvalue=pd.to_numeric(ideal_df[i]))
# =============================================================================
#         sum((pd.to_numeric(train_set) -
#                        pd.to_numeric(ideal_df[i]))**2)
# =============================================================================
        # print(i + ": " + str(tmp_val))
        if last_val == "not_set":
            last_val = tmp_val
            selected = i
        elif tmp_val > last_val:
            pass
        elif tmp_val == last_val:
            selected = selected + ", " + i
        else:
            last_val = tmp_val
            selected = i
    return(selected, last_val)


def calculate_best_ideal(test_value, match_against, index,
                         idealdata, function):

    from .config import factor
    import pandas as pd

    result = pd.DataFrame()

    for i in match_against.keys():
        ideal_col = match_against[i][0]
        ideal_deviation = match_against[i][1]
        max_deviation = ideal_deviation*factor

        extract = idealdata.loc[idealdata["x"] == float(test_value[0]),
                                ideal_col]
        ideal_value = float(extract.values)
        deviation = abs(ideal_value - float(test_value[1]))
        too_much = deviation > max_deviation

        row = {"DeltaY": deviation,
               "Idealfunktion": ideal_col,
               'Off_limit': too_much}

        result = pd.concat([result,
                            pd.DataFrame(row, index=[index])])

    if function == "raw":
        pass
    else:
        result = result[result["DeltaY"]
                        == function(result["DeltaY"])]

    return(result)
