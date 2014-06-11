#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Run from the command line

usage: run.py [-h] {shell,db,runserver} ...

positional arguments:
  {shell,db,runserver}
    shell               Runs a Python shell inside Flask application context.
    db                  Perform database migrations
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -h, --help            show this help message and exit
"""

from app import manager
manager.run()