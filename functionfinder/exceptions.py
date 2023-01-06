#!/usr/bin/env python
# coding: utf-8
"""Docstring for module exceptions.py.

This module contains userdefined exceptions.
"""


class TypeError(Exception):
    """Storage defined to handle necessary data operations.

    Contains recurring methods for the given types of datasets.

    Attributes
    ----------
    _table : string
        Refered table name in SQLite Database
    _style : string
        Matplotlib plotting style
    ylabel : string
        Label of y-axis for plotting
    xlabel : string
        Label of x-axis for plotting
    title : string
        Title of plot
    fname : string
        Name of png file to save plots
    _dbcon : string
        Name and location of SQLite Database
    data : pandas.DataFrame
        Data read in from SQLite Database

    Methods
    -------
    __init__(dataname="train", ylabel="Y", xlabel="X", plottitle = "no title",
             plotfile="testplot.png")
        Constructor method to specify relevant attributes.
    getdata()
        Query SQLite database to read and store data in 'data' attribute.
    draw()
        Plot data and save to png file.
    """


def __init__(self):
    my_message = 'Die Römer haben nichts für uns getan'
    self.my_message = my_message
