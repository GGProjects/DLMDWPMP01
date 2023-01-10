#!/usr/bin/env python
# coding: utf-8
"""Docstring for module exceptions.py.

This module contains userdefined exceptions.
"""


class TypeError(Exception):
    """Exception raised during check of datatypes of function parameters."""


def __init__(self):
    my_message = 'Eine übergebene Variable hat einen falschen Datentyp'
    self.my_message = my_message
