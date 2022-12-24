#!/usr/bin/env python
# coding: utf-8
"""
Run the main calculations to solve given task.

PURPOSE:
Evaluate ideal functions for a set of training data (1) and assign
values of a test-dataset to those ideal functions (2)
DETAILS:
  Used criteria for evaluation:
  (1) to match training data and ideal functions:
      minimum MeanSquaredError (MSE)
  (2) to match ideal functions and test data:
  precalculated MSE (1) * SquareRoot(2)

  Created on Fri Nov 18 08:45:16 2022
  in Python version: python: 3.9.13 (main, Aug 25 2022, 23:51:50)
  AUTHOR: Georg Grunsky (georg.grunsky@iu-study.org)
"""

def task():
    """
    Run the main calculations to solve given task.

    PURPOSE:
        Evaluate ideal functions for a set of training data (1) and assign
        values of a test-dataset to those ideal functions (2)
    DETAILS:
        Used criteria for evaluation:
        (1) to match training data and ideal functions:
            minimum MeanSquaredError (MSE)
        (2) to match ideal functions and test data:
            precalculated MSE (1) * SquareRoot(2)

    Created on Fri Nov 18 08:45:16 2022
    in Python version: python: 3.9.13 (main, Aug 25 2022, 23:51:50)
    AUTHOR: Georg Grunsky (georg.grunsky@iu-study.org)
    """
# =============================================================================
# Import required modules
# =============================================================================
    print("# Load required modules")

    # import modules
    import sys
    import sqlite3
    import csv

    # import own modules
    import functionfinder.datafunctions as df
    from functionfinder.config import datafiles, dbname, out_data
    import functionfinder.classes as cl
    from functionfinder.log import logging

    # Set logger for main program
    logger = logging.getLogger('functionfinder')
    logging.getLogger('PIL').setLevel(logging.ERROR)
    logging.getLogger('matplotlib').setLevel(logging.ERROR)

    # Log Start-Time
    print("# Start functionfinder main task")
    logger.info("Start functionfinder main task")

# =============================================================================
# Read data for calculation.
# =============================================================================
    section = "Read CSV training data and ideal functions to SQLite-DB"
    print("#", section)
    logger.info(section)

    # Specify datasets and load them into sqlite
    df.create_empty_sqlitedb(dbname)
    csv_to_read = ("ideal", "train")
    for i in csv_to_read:
        try:
            df.csv2sql_directly(dbname, datafiles[i], i)
            logger.debug("Direct sql-import worked.")
            print("# Direct sql-import worked.")
        except:
            logger.debug("Direct sql-import didn't work, try pandas next.")
            try:
                df.csv2sql_pandas(dbname, datafiles[i], i)
                logger.debug("Pandas sql-import worked")
                print("# Pandas sql-import worked")
            except:
                print("CSV import to SQL didn't work at all.")
                logger.debug("CSV import to SQL didn't work at all.")
                sys.exit("Import to SQL failed. Exit programm")

# =============================================================================
# Save training-data plot
# =============================================================================
    section = "loading training data to class \"projectdata\" data"
    print("#", section)
    logger.info(section)

    train = cl.projectdata(dataname="train",
                           plotfile="train.png",
                           plottitle="Training Data")
    train.getdata()
    train.draw_train()

# =============================================================================
# Find matching ideal function for each of the four training functions
# =============================================================================
    section = ("Find matching ideal function for each of the four" +
               " training functions")
    print("#", section)
    logger.info(section)

    # read ideal from sqlite
    ideal = cl.idealdata(dataname="ideal",
                         plotfile="ideal.png",
                         plottitle="Matched ideal functions")
    ideal.getdata()

    ideal.matched_functions()
    for j in train.data.axes[1][1:]:
        match_set = train.data[j]
        ideal.matched[j] = df.min_error(match_set, ideal.data)

    logger.info("See below the numbers of the matched ideal functions " +
                 "plus the according deviation")
    logger.info("Ideal functions: %s", ideal.matched)

    # Remove unneeded objects from memory
    del(train, match_set)

# =============================================================================
# Save ideal-functions plot
# =============================================================================

    ideal.draw_ideal()


# =============================================================================
# Assign test data to ideal functions
# =============================================================================
    section = "Calculate assignment of test data to selected ideal functions"
    print("# ", section)
    logger.info(section)

    conn = sqlite3.connect(str(out_data + dbname))

    # Rowwise calculation of best ideal function for test data entries
    with open(datafiles["test"], newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # skip headers
        for row in reader:
            test_row = df.calculate_best_ideal(test_value=row,
                                               match_against=ideal.matched,
                                               index=float(row[0]),
                                               idealdata=ideal.data,
                                               function=min)
            test_row.insert(0, "x", row[0])
            test_row.insert(1, "y", row[1])
            # Append result to SQL Tabel "test"
            test_row.to_sql('test', conn, if_exists='append', index=False)

    conn.close()

# =============================================================================
# Evaluation of results
# =============================================================================
    section = "Evaluate calculated results."
    print("#", section)
    logger.info(section)

    # create object of class testdata
    test = cl.testdata(dataname="test",
                       plotfile="test.png",
                       plottitle="Test Data")

    test.getdata()

    # query database entries where deviation was higher than allowed
    try:
        test.off_limit()
    except:
        pass

    if len(test.off) > 0:

        logger.info("%s entries had a deviation above the set limit:",
                     len(test.off))
        logger.debug(test.off)
        logger.info("Calculating deviation for those entries " +
                     "from all matched ideal functions for comparision.")

        print("# " + str(len(test.off)) +
              " entries had a deviation above the set limit:")
        print(test.off)
        print()
        print("# Calculating deviation for those entries " +
              "from all matched ideal functions for comparision.")

        for k in test.off["x"]:
            test_value = test.data[test.data["x"] == str(k)][["x", "y"]]
            test_value = test_value.values.tolist()[0]
            test_row = df.calculate_best_ideal(test_value, ideal.matched, k,
                                               ideal.data, "raw")
            test_row.insert(0, "x", test_value[0])
            test_row.insert(1, "y", test_value[1])
            print(test_row)
            logger.debug(test_row)

# =============================================================================
# PLOT assignment of test-data, hue per ideal function,
# different symbol if off limit
# =============================================================================

    test.draw_test()

    logtext = ("Programm successfully terminated.\n See ouput folder for " +
               "figures, Database and log-files.")
    print("# " + logtext)
    logger.info(logtext)
