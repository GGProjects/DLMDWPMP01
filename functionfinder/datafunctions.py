#!/usr/bin/env python
# coding: utf-8
"""Functions used for data handling.

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
import sys
from .config import out_data, error_calculation, factor
from .log import logging
from .exceptions import TypeError


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
    # Conduct instance check of variable input
    paramdict = {"dbname": (dbname, str)}
    checktypes("create_empty_sqlitedb", paramdict)

    # Conduct actual task
    dbpath = out_data + dbname  # create path
    if Path.is_file(Path(dbpath)):  # check if path allready exists
        Path.unlink(Path(dbpath))  # in case: delete file
    Path(dbpath).touch()  # create empty db file


def csv2sql_directly(existing_db, csv_toadd, tablename):
    """Import csv files into existing SQLite database using subprocess.

    Direct import using subprocess enhances importing large csv files.

    Parameters
    ----------
    existing_db : string
        Name of existing SQLite database. Location/Directory is handled by
        parameter set in config.py.
    csv_toadd : string
        Location and name of csv-file to import.
    tablename : string
        Name of table in SQLite database in which to write the data.
    """
    # Conduct instance check of variable input
    paramdict = {"dbname": (existing_db, str),
                 "csv_toadd": (csv_toadd, str),
                 "tablename": (tablename, str)}
    checktypes("csv2sql_directly", paramdict)

    # Execute actual task
    db_name = Path(str(out_data + existing_db)).resolve()
    csv_file = Path(csv_toadd).resolve()
    subprocess.run(['sqlite3',
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
    existing_db : string
        Name of existing SQLite database. Location/Directory is handled by
        parameter set in config.py.
    csv_toadd : string
        Location and name of csv-file to import.
    tablename : string
        Name of table in SQLite database in which to write the data.
    """
    # Conduct instance check of variable input
    paramdict = {"dbname": (existing_db, str),
                 "csv_toadd": (csv_toadd, str),
                 "tablename": (tablename, str)}
    checktypes("csv2sql_pandas", paramdict)

    # Execute actual task
    conn = sqlite3.connect(str(out_data + existing_db))
    pd.read_csv(csv_toadd).to_sql(tablename, conn,
                                  if_exists='replace', index=False)
    conn.close()


def min_error(train_set, ideal_df):
    """Select column of a pandas DataFrame with minimal error to a Series.

    Parameters
    ----------
    train_set : pandas Series
        Column of training dataset, that should be matched against DataFrame
        of ideal functions.
    ideal_df : pandas DataFrame
        DataFrame of ideal functions.

    Returns
    -------
    selected, last_val : tupel
    selected : string
        Column name of matched ideal function for this train_set.
    last_val : float
        Deviation between train_set and matched ideal function according to
        the error_calculation method.
    """
    # Conduct instance check of variable input
    paramdict = {"train_set": (train_set, pd.core.series.Series),
                 "csv_toadd": (ideal_df, pd.core.frame.DataFrame)}
    checktypes("min_error", paramdict)

    # Execute actual task
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
                         idealdata, function=min):
    """Select ideal function with minimal deviation to given point.

    Parameters
    ----------
    test_value : list
        Current row of test.csv file containing two values (x and y).
    match_against : dictionary
        Matches of training data to selected ideal functions including
        calculated deviation.
    index : float
        Read from x-value of test_value parameter. Used to index resulting
        DataFrame.
    idealdata : pandas.DataFrame
        Ideal functions from ideal dataset. Used to find function with closest
        y-value at indexed position (x-value)
    function : method, optional
        Desired method to filter resulting deviation values.
        The default is min (the observation with the lowest deviation will be
        returned). When passing 'raw' all rows of the resulting DataFrame will
        be returned (used to write all DataFrame lines to logfile for
        evaluating certain values).

    Returns
    -------
    result : pandas.DataFrame
    Containing the deviation (DeltaY), number of matched ideal function
    (Idealfunktion) and a boolean whether the deviation exceeded the given
    limit, filtered by passed 'function' method upon call.
    """
    # check if passed params are of correct type
    paramdict = {"test_value": (test_value, list),
                 "match_against": (match_against, dict),
                 "index": (index, float),
                 "idealdata": (idealdata, pd.core.frame.DataFrame)}
    checktypes("calculate_best_ideal", paramdict)

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


def checktypes(functionname, typedict):
    """Check if types of data passed to a function upon call meet requirements.

    Parameters
    ----------
    functionname : string
        Name of calling function, needed in case of error-logging.
    typedict : dictionary
        Required parameters of functions and according datatypes. Format has
        to be {object-name as string: (object-name, object-type)}

    Returns
    -------
    Raise Error on failure and quit program.
    """
    try:
        markdeletion = list()  # create empty list to mark dict deletions

        # iterate through dict and mark correct instances for deletion
        for i in typedict.keys():
            if isinstance(typedict[i][0], typedict[i][1]):
                markdeletion = markdeletion + [i]

        # iterate through marked deletions and delete from passed dict
        for j in markdeletion:
            del(typedict[j])

        if len(typedict) > 0:  # check if any incorrect entries remain in dict
            raise TypeError

    except TypeError:
        text = ("Method " + functionname + ": " +
                "Parameters " + str(list(typedict.keys())) + " NOT of right " +
                "data type!")
        logging.critical(text)
        sys.exit(text)
