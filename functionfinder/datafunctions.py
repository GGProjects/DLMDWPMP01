#!/usr/bin/env python
# coding: utf-8
"""Docstring for module datafunctions.py.

This script contains definitions for data related functions of the
functionfinder package.

Methods
-------
create_empty_sqlitedb(dbname)
    Create empty SQLite Database.
csv2sql_directly(existing_db, csv_toadd, tablename)
    Import csv files into existing SQLite database using subprocess.
csv2sql_pandas(existing_db, csv_toadd, tablename)
    Import csv files into existing SQLite database using pandas.
min_error(train_set, ideal_df)
    Select column of a pandas DataFrame with minimal error to a Series.
calculate_best_ideal(test_value, match_against, index, idealdata, function)
    Select ideal function with minimal deviation to given point.
"""

from pathlib import Path
import subprocess
import pandas as pd
import sqlite3
from .config import out_data, error_calculation, factor

def create_empty_sqlitedb(dbname):
    """Create empty SQLite Database.

    Name and location are specified by handed parameter and data output folder
    in config.py. Existing databases in same location of the same name are
    deleted before creation.

    Parameters
    ----------
    dbname : string
        Name of database to create.
    """
    dbpath = out_data + dbname
    if Path.is_file(Path(dbpath)):
        Path.unlink(Path(dbpath))
    Path(dbpath).touch()


def csv2sql_directly(existing_db, csv_toadd, tablename):
    """Import csv files into existing SQLite database using subprocess.

    Direct import using subprocess enhances importing large csv files.

    Parameters
    ----------
    existing_db : TYPE
        DESCRIPTION.
    csv_toadd : TYPE
        DESCRIPTION.
    tablename : TYPE
        DESCRIPTION.
    """
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
    """Import csv files into existing SQLite database using pandas.

    No direct import. csv files are first read into a pandas dataframe and
    then fed into an existing SQLite database.

    Parameters
    ----------
    existing_db : TYPE
        DESCRIPTION.
    csv_toadd : TYPE
        DESCRIPTION.
    tablename : TYPE
        DESCRIPTION.
    """
    conn = sqlite3.connect(str(out_data + existing_db))
    pd.read_csv(csv_toadd).to_sql(tablename, conn,
                                  if_exists='replace', index=False)
    conn.close()


def min_error(train_set, ideal_df):
    """Select column of a pandas DataFrame with minimal error to a Series.
    

    Parameters
    ----------
    train_set : pandas Series
        DESCRIPTION.
    ideal_df : pandas DataFrame
        DESCRIPTION.

    Returns
    -------
    None.

    """
    last_val = "not_set"
    for i in ideal_df.axes[1][1:]:
        tmp_val = error_calculation(trainvalue=pd.to_numeric(train_set),
                                    idealvalue=pd.to_numeric(ideal_df[i]))
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
    """Select ideal function with minimal deviation to given point.
    

    Parameters
    ----------
    test_value : TYPE
        DESCRIPTION.
    match_against : TYPE
        DESCRIPTION.
    index : TYPE
        DESCRIPTION.
    idealdata : TYPE
        DESCRIPTION.
    function : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
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
