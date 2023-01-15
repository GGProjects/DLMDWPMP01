#!/usr/bin/env python
# coding: utf-8
"""Definition of object classes.

This module defines three classes used to store data information. The latter
two are subclasses of the first class projectdata.
"""

import sqlite3
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
from pathlib import Path

from functionfinder.config import out_data, out_figures, dbname


class projectdata():
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

    def __init__(self, dataname="train", ylabel="Y", xlabel="X",
                 plottitle="no title", plotfile="testplot.png"):
        """Construct attributes for this class.

        Parameters
        ----------
        dataname : string
            Provide SQLite table name to read data from.
            The default is "train".
        ylabel : string, optional
            Provide y-axis title for plotting. The default is "Y".
        xlabel : string, optional
            Provide x-axis title for plotting. The default is "X".
        plottitle : string
            Provide plot-title for contained data. The default is "no title".
        plotfile : string
            Provide name of PNG to save plot. The default is "testplot.png".
        """
        self._table = dataname
        self._style = "ggplot"
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.title = plottitle
        self.fname = out_figures + plotfile
        self._dbcon = out_data + dbname

    def getdata(self):
        """Query SQLite database to read and store data in 'data' attribute."""
        con = sqlite3.connect(self._dbcon)
        selectstring = "SELECT * FROM " + self._table
        self.data = pd.read_sql_query(selectstring, con)
        con.close()

    def draw(self):
        """Plot data and save to png file."""
        style.use(self._style)
        fig, trax = plt.subplots(figsize=(6, 4))
        for i in self.data.axes[1][1:]:
            trax.plot(pd.to_numeric(self.data["x"]),
                      pd.to_numeric(self.data[i]),
                      label=i,
                      linewidth=2)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(self.title)
        plt.legend(loc="upper right")
        plt.savefig(Path(self.fname))
        plt.close()


class idealdata(projectdata):
    """Subclass of class 'projectdata' to store and handle data operations.

    Contains recurring methods for the ideal functions dataset.

    Attributes
    ----------
    As in class 'projectdata' plus additionally:
    matched : dictionary
        Results of matching training data to ideal functions

    Methods
    -------
    As in class 'projectdata' plus additionally:
    matched_functions(match_result=dict())
        Assign dictionary to 'matched' attribute
    """

    def matched_functions(self, match_result=dict()):
        """Assign dictionary to 'matched' attribute.

        Parameters
        ----------
        match_result : dictionary, optional
            Provide dictionary to store in 'matched' attribute.
            The default is dict().
        """
        self.matched = match_result

    def draw(self):
        """Plot data and save to png file."""
        style.use(self._style)
        fig, iax = plt.subplots(figsize=(6, 4))
        for i in self.matched.keys():
            iax.plot(pd.to_numeric(self.data["x"]),
                     pd.to_numeric(self.data[self.matched[i][0]]),
                     label=self.matched[i][0],
                     linewidth=2)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(self.title)
        plt.legend(loc="upper right")
        plt.savefig(Path(self.fname))
        plt.close()


class testdata(projectdata):
    """Subclass of class 'projectdata' to store and handle data operations.

    Contains recurring methods for the test dataset.

    Attributes
    ----------
    As in class 'projectdata' plus additionally:
    off : pandas.DataFrame
        Results of matching test data to ideal functions, which exceed the
        predefined limit.

    Methods
    -------
    As in class 'projectdata' plus additionally:
    off_limit()
        Query SQLite database to read and store entries, which exceeded the
        predefined limit, to 'off' attribute.
    """

    def off_limit(self):
        """Read data, exceeding predifined deviation limit, from SQLite."""
        con = sqlite3.connect(self._dbcon)
        selstring = "SELECT * FROM " + self._table + " WHERE Off_limit = True"
        self.off = pd.read_sql_query(selstring, con)
        con.close()

    def draw(self):
        """Plot data and save to png file."""
        style.use(self._style)
        tax = sns.scatterplot(x=pd.to_numeric(self.data.x),
                              y=pd.to_numeric(self.data.y),
                              data=self.data,
                              hue="Idealfunktion", style="Off_limit")
        lgd = sns.move_legend(tax,
                              bbox_to_anchor=(1.01, 1.02),
                              loc='upper left')
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(self.title)
        plt.savefig(Path(self.fname),
                    bbox_extra_artists=(lgd),
                    bbox_inches='tight')
        plt.close()
