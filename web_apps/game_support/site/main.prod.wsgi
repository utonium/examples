#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
main.prod.wsgi

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import os
import sys

import pyramid.config


# ---------------------------------------------------------------
# Configure the Python environment
# ---------------------------------------------------------------
sys.path.append("/var/www/code/src"))

import local.configurator


# ---------------------------------------------------------------------------------------------
# Setup and run the Pyramind WSGI application.
# ---------------------------------------------------------------------------------------------
config = local.configurator.getPyramidConfigurator()

application = config.make_wsgi_app()
