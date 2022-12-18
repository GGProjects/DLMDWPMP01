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
print("env_functions")


conda env create -f config/DLMDWPMP01.yaml --prefix ./venv/

# exception handling for windows/linux
conda activate .\\venv


conda env list
conda list



################################################
try:
    print(2/0)
except ZeroDivisionError:
    print("geht nicht")

try:
    print(2/4)
except ZeroDivisionError:
    print("geht nicht")

try:
    import pip
except ImportError:
    print("Fehler")


try:
    import conda
except ImportError:
    print("Fehler")


import importlib.util
import sys

# For illustrative purposes.
name = 'itertools'
name = "hanswurst"

if name in sys.modules:
    print(f"{name!r} already in sys.modules")
elif (spec := importlib.util.find_spec(name)) is not None:
    # If you choose to perform the actual import ...
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    print(f"{name!r} has been imported")
else:
    print(f"can't find the {name!r} module")

# =============================================================================
# #### mögliche UMgebungsfunktionen
# # git repo clonen bzw. download und entpacken
# # check environment
# # check packages
# # conda or pip
# # required packages
# =============================================================================

# conda clone from existing
conda create --clone base -n testenv

# conda create from yml
conda env create --name environment_name -f environment.yml

# conda export to yml
conda env export | grep -v "^prefix: " > env.yml
conda env export --file SOME_FILE

# save to txt file
conda list --explicit > bio-env.txt

# create from txt file
conda env create --file bio-env.txt

conda activate iu_python_task

conda create myenv --prefix=/work/<mygroup>/<mydirectory>

###########################################################
will look like that in the requirements.txt:

jupyter==1.0.0
pandas==1.0.0
scikit-learn==0.22.1

and then create and switch to your virtual environment

and then do

pip install -r requirements.txt

# output pip requirements.file
pip freeze [options]

############################################################

Setup the pip package manager

Check to see if your Python installation has pip. Enter the following in your terminal:

pip -h

If you see the help text for pip then you have pip installed, otherwise download and install pip
Install the virtualenv package

The virtualenv package is required to create virtual environments. You can install it with pip:

pip install virtualenv

Create the virtual environment

To create a virtual environment, you must specify a path. For example to create one in the local directory called ‘mypython’, type the following:

virtualenv mypython

Activate the virtual environment

You can activate the python environment by running the following command:
Mac OS / Linux

source mypython/bin/activate

Windows

mypthon\Scripts\activate

You should see the name of your virtual environment in brackets on your terminal line e.g. (mypython).

Any python commands you use will now work with your virtual environment
Deactivate the virtual environment

To decativate the virtual environment and use your original Python environment, simply type ‘deactivate’.

deactivate




# =============================================================================
# ### Conda_Kernels
# # nb_conda_kernels
#
#
# # # Git Repo einrichten / lokal erstellen
#
#
#
# # Eigenes Verzeichnis nach UserInput auf lokalem Datenträger erstellen
# # fork von git repo von GGProjects anlegen nach Eingabe der eigenen GitCredentials
# # Exception Handling falls nicht möglich
#
#
# # # VE erstellen / Darstellen der eigenen Environment
#
# conda --version
# #conda info
# #conda env list
#
#
#
# # VE erstellen oder, falls vorhanden laden
# conda env create --file DLMDWPMP01.yaml
# conda env
# #Systembefehl: python -m venv E:\my_env # userInput für verzeichnis
#
#
#
# Umgebung
# #Nach Erstellung der VE, muss sie aktiviert werden, damit sie verwendet werden kann.
# #Um die VE unter Windows zu aktivieren, führen wir Folgendes aus:
# E:\my_env\Scripts\activate.bat
# #Um die VE unter Unix oder MacOS zu aktivieren:
# source my_env/bin/activate
#
#

#
# =============================================================================


