#!/usr/bin/env python
# coding: utf-8
"""Docstring for module ffrunner.py.

This script contains the main part of the programm which orchestrates
calculations and can be called, after installation, by the CLI-command ff.

Methods
-------
task()
    Run the calculations to solve the given task.
"""


def task():
    """Run the calculations to solve the given task.

    Evaluate ideal functions for a set of training data (1) and assign
    values of a test-dataset to those ideal functions (2)

    Used criteria for evaluation:
    (1) to match training data and ideal functions:
    minimum SummedSquaredError (SSE)
    (2) to match ideal functions and test data:
    precalculated SSE (1) * SquareRoot(2)
    """
# =============================================================================
# Import required modules
# =============================================================================
    print("# Import required modules")

    # import standard modules
    import sys
    import sqlite3
    import csv

    # import own modules
    import functionfinder.datafunctions as df  # data handling methods
    from functionfinder.config import datafiles, dbname, out_data
    import functionfinder.classes as cl
    from functionfinder.log import logging

# =============================================================================
# Define logger for main program, define logging helper
# =============================================================================
    logger = logging.getLogger('functionfinder')
    logging.getLogger('PIL').setLevel(logging.ERROR)  # prevent massive logging
    logging.getLogger('matplotlib').setLevel(logging.ERROR)  # prevent logging

    def printandlog(textin):
        """Print and log titles of script sections."""
        print("#", textin)
        logger.info(textin)

    # Start logging the programm.
    printandlog("Start functionfinder program")

# =============================================================================
# Read data for calculation.
# =============================================================================
    printandlog("Read CSV training data and ideal functions to SQLite-DB")

    # create empty sqlite database
    df.create_empty_sqlitedb(dbname)

    # define which csv entries from datafiles variable (config module) to read
    csv_to_read = ("ideal", "train")

    # iterate through csv_to_read an try importing via direct import or the
    # use of pandas
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
# Load training-data in defined class and plot to png
# =============================================================================
    printandlog("loading training data to class \"projectdata\" data")

    # assign self defined class projectdata
    train = cl.projectdata(dataname="train",
                           plotfile="train.png",
                           plottitle="Training Data")

    # load data from sqlite database
    train.getdata()

    # render and save plot to specified file
    train.draw()

# =============================================================================
# Load ideal-data in defined class and plot to png
# =============================================================================
    printandlog("Load ideal data.")

    # assign defined class idealdata (subclass of projectdata) to ideal data
    ideal = cl.idealdata(dataname="ideal",
                         plotfile="ideal.png",
                         plottitle="Matched ideal functions")

    # read ideal data from sqlite
    ideal.getdata()

# =============================================================================
# Find matching ideal function for each of the four training functions
# =============================================================================
    printandlog("Find matching ideal function for each of the four" +
                " training functions")

    ideal.matched_functions()  # create empty dictionary in ideal.matched

    # iterate through training data columns, apply method to find matching
    # ideal function and add result to ideal.matched dictionary
    for j in train.data.axes[1][1:]:
        match_set = train.data[j]
        ideal.matched[j] = df.min_error(match_set, ideal.data)

    # plot results to png
    ideal.draw()

    # log results for manual evaluation
    logger.info("See below the numbers of the matched ideal functions " +
                "plus the according deviation")
    logger.info("Ideal functions: %s", ideal.matched)

    # Remove unneeded objects from memory
    del(train, match_set)

# =============================================================================
# Assign test data to ideal functions and write to SQLite table "test"
# =============================================================================
    printandlog("Calculate assignment of test data to " +
                "selected ideal functions and write to sqlite database.")

    # open connection to sqlite database
    conn = sqlite3.connect(str(out_data + dbname))

    # Rowwise calculation of best ideal function for test.csv specified in
    # datafiles dictionary
    with open(datafiles["test"], newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # skip headers
        for row in reader:
            # execute method to find best matching ideal function, see
            # method documentation for information on parameters.
            test_row = df.calculate_best_ideal(test_value=row,
                                               match_against=ideal.matched,
                                               index=float(row[0]),
                                               idealdata=ideal.data,
                                               function=min)
            test_row.insert(0, "x", row[0])  # add original x-value
            test_row.insert(1, "y", row[1])  # add original y-value
            # Append result to SQLite table "test"
            test_row.to_sql('test', conn, if_exists='append', index=False)

    # close connection to database
    conn.close()

# =============================================================================
# Evaluation of results
# =============================================================================
    printandlog("Evaluate calculated results.")

    # assign object of class testdata (as subclass of projectdata)
    test = cl.testdata(dataname="test",
                       plotfile="test.png",
                       plottitle="Test Data")

    # read test data from sqlite db
    test.getdata()

    # query database entries where deviation was higher than allowed and
    # write dataframe to test.off
    try:
        test.off_limit()
    except:
        pass

    if len(test.off) > 0:  # execute only if there are entries off limit

        # log and print results to file/screen.
        printandlog(str(len(test.off)) +
                    " entries had a deviation above the set limit:")
        printandlog(test.off)
        printandlog("Calculating deviation for those entries " +
                    "from all matched ideal functions for comparision.")

        # pass data off_limit to calculation method and return all deviation
        # values for comparison and manual evaluation. Log and print results.
        for k in test.off["x"]:
            test_value = test.data[test.data["x"] == str(k)][["x", "y"]]
            test_value = test_value.values.tolist()[0]
            test_row = df.calculate_best_ideal(test_value, ideal.matched, k,
                                               ideal.data, "raw")
            test_row.insert(0, "x", test_value[0])
            test_row.insert(1, "y", test_value[1])
            printandlog(test_row)

    # plot to png, hue per ideal function, different symbol if off_limit
    test.draw()

# =============================================================================
# End of program
# =============================================================================

    printandlog("Programm successfully terminated.\n See ouput folder for " +
                "figures, Database and log-files.")


# Only execute when called directly
if __name__ == "__main__":
    task()
