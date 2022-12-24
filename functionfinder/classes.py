#!/usr/bin/env python
# coding: utf-8

"""
Created on Fri Nov 18 08:45:16 2022

@author: Grunsky

@module: DLMDWPM01

@description: main programm. 

@purpose: evaluate ideal functions for a set of training data (1) and assign 
    values of a test-dataset to those ideal functions (2)

@details: Used criteria for evaluation:
    (1) to match training data and ideal functions: 
        minimum MeanSquaredError (MSE)
    (2) to match ideal functions and test data: 
        precalculated MSE (1) * SquareRoot(2)

@Python_Version: python: 3.9.13 (main, Aug 25 2022, 23:51:50) 
"""

class projectdata():

    # Define Constructor
    def __init__(self, dataname="train", ylabel="Y", xlabel="X",
                 plottitle="no title", plotfile="testplot.png"):
        from functionfinder.config import out_data, out_figures, dbname
        self._table = dataname
        self._style = "ggplot"
        self.ylabel = ylabel
        self.xlabel = xlabel
        self.title = plottitle
        self.fname = out_figures + plotfile
        self._dbcon = out_data + dbname

    # Define method to get data from sqlite db
    def getdata(self):
        import pandas as pd
        import sqlite3
        con = sqlite3.connect(self._dbcon)
        selectstring = "SELECT * FROM " + self._table
        self.data = pd.read_sql_query(selectstring, con)
        con.close()

    # Define drawing method
    def draw_train(self):
        import pandas as pd
        from matplotlib import pyplot as plt
        from matplotlib import style
        from pathlib import Path

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
        plt.savefig(Path(self.fname))
        plt.close()


class idealdata(projectdata):
    # Define method to match data against ideal functions
    def matched_functions(self, match_result=dict()):
        self.matched = match_result

    # Define drawing method
    def draw_ideal(self):
        import pandas as pd
        from matplotlib import pyplot as plt
        from matplotlib import style
        from pathlib import Path

        style.use(self._style)
        fig, iax = plt.subplots(figsize=(6, 4))
        for i in self.matched.keys():
            iax.plot(pd.to_numeric(self.data["x"]),
                     pd.to_numeric(self.data[self.matched[i][0]]),
                     label=i,
                     linewidth=2)
        # ax.legend()
        # ax.grid(True, color="k")
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.title(self.title)
        plt.savefig(Path(self.fname))
        plt.close()


class testdata(projectdata):
    # Define method to receive data out of limit
    def off_limit(self):
        import pandas as pd
        import sqlite3
        con = sqlite3.connect(self._dbcon)
        selstring = "SELECT * FROM " + self._table + " WHERE Off_limit = True"
        self.off = pd.read_sql_query(selstring, con)
        con.close()

    def draw_test(self):
        import seaborn as sns
        import pandas as pd
        from matplotlib import pyplot as plt
        from matplotlib import style
        from pathlib import Path

        # https://matplotlib.org/ (22-11-13)
        style.use(self._style)
        #fig, tax = plt.subplots(figsize=(6, 4))
        tax = sns.scatterplot(x=pd.to_numeric(self.data.x),
                              y=pd.to_numeric(self.data.y),
                              data=self.data,
                              hue="Idealfunktion", style="Off_limit")
        # ax.legend()
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