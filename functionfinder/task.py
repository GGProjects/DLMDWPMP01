#!/usr/bin/env python
# coding: utf-8

def task():
	'''
	Run the main calculations to solve given task
	
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
	'''
	
	# =============================================================================
	# Import required modules
	# =============================================================================
	print("# Load required modules")
	
	# import modules
	import sys
	import os
	from pathlib import Path
	import sqlite3
	import pandas as pd
	import seaborn as sns # not available on ipad
	from matplotlib import pyplot as plt
	from matplotlib import style
	import csv
	
	# import own modules
	from functionfinder.log import logging
	import functionfinder.datafunctions as df
	from functionfinder.config import datafiles, dbname, out_data
	import functionfinder.classes as cl
	
	# Log Start-Time
	print("# Start functionfinder main task")
	logging.info("Start functionfinder main task")
	
	
	# =============================================================================
	# Read data for calculation.
	# =============================================================================
	section = "Read CSV training data and ideal functions to SQLite-DB"
	print("#", section)
	logging.debug(section)
	
	# Specify datasets and load them into sqlite
	df.create_empty_sqlitedb(dbname)
	csv_to_read = ("ideal", "train")
	for i in csv_to_read:
			try:
				df.csv2sql_directly(dbname, datafiles[i], i)
				logging.debug("Direct sql-import worked.")
				print("Direct sql-import worked.")
			except:
				logging.debug("Direct sql-import didn't work, try pandas next.")
				try:
					df.csv2sql_pandas(dbname, datafiles[i], i)
					logging.debug("Pandas sql-import worked")
					print("Pandas sql-import worked")
				except:
					print("CSV import to SQL didn't work at all.")
					logging.debug("CSV import to SQL didn't work at all.")
					sys.exit("Import to SQL failed. Exit programm")
	
	
	# =============================================================================
	# Save training-data plot
	# =============================================================================
	section = "loading training data to class \"projectdata\" data and save plot"
	print("#", section)
	logging.debug(section)
	
	train = cl.projectdata(dataname="train",
						plotfile="train.png",
						plottitle="Training Data")
	train.getdata()
	train.drawplot()
	
	
	# =============================================================================
	# Find matching ideal function for each of the four training functions
	# =============================================================================
	section = ("Find matching ideal function for each of the four" +
			" training functions")
	print("#", section)
	logging.debug(section)
	
	# read ideal from sqlite
	ideal = cl.idealdata(dataname="ideal",
						plotfile="ideal.png",
						plottitle="Matched ideal functions")
	ideal.getdata()
	
	
	ideal.matched_functions()
	for j in train.data.axes[1][1:]:
		match_set = train.data[j]
		ideal.matched[j] = df.min_error(match_set, ideal.data)
	
	logging.info("See below the numbers of the matched ideal functions " +
				"plus the according deviation")
	logging.info("Ideal functions: %s", ideal.matched)
	
	# Remove unneeded objects from memory
	del(train, match_set)
	
	# =============================================================================
	# Save ideal-functions plot
	# =============================================================================
	
	ideal.drawplot()
	
	
	# =============================================================================
	# Assign test data to ideal functions
	# =============================================================================
	section = "Calculate assignment of test data to selected ideal functions"
	print("# ", section)
	logging.debug(section)
	
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
	logging.debug(section)
	
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
	
		logging.info("%s entries had a deviation above the set limit:",
					len(test.off))
		logging.info(test.off)
		logging.info("Calculating deviation for those entries from all matched " +
					"ideal functions for comparision.")
	
		print("# " + str(len(test.off)) +
			" entries had a deviation above the set limit:")
		print(test.off)
		print()
		print("# Calculating deviation for those entries from all matched ideal " +
			"functions for comparision.")
	
		for k in test.off["x"]:
			test_value = test.data[test.data["x"] == str(k)][["x", "y"]]
			test_value = test_value.values.tolist()[0]
			test_row = df.calculate_best_ideal(test_value, ideal.matched, k,
											ideal.data, "raw")
			test_row.insert(0, "x", test_value[0])
			test_row.insert(1, "y", test_value[1])
			print(test_row)
			logging.info(test_row)
	
	
	# =============================================================================
	# PLOT assignment of test-data, hue per ideal function,
	# different symbol if off limit
	# =============================================================================
	
	test.drawplot()
