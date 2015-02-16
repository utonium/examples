#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
main.dev.wsgi

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import os
import sys

import pyramid.config
import wsgiref.simple_server

# ---------------------------------------------------------------
# Configure the Python environment
# ---------------------------------------------------------------
SCRIPT_NAME = os.path.normpath(os.path.basename(sys.argv[0]))
SCRIPT_HOME = os.path.normpath(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.join(SCRIPT_HOME, "..", "src"))

import local.configurator


# ---------------------------------------------------------------------------------------------
# Setup and run the Pyramind WSGI application.
# ---------------------------------------------------------------------------------------------
config = local.configurator.getPyramidConfigurator(is_dev_server=True)

application = config.make_wsgi_app()

server = wsgiref.simple_server.make_server('0.0.0.0', 8080, application)
server.serve_forever()
