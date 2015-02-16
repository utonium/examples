#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
local/view.py

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import json
import os
import string

import pyramid.renderers
import pyramid.view


# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# View methods
# ---------------------------------------------------------------------------------------------
@pyramid.view.view_config(route_name='index', request_method='GET')
def indexPage(request):
    """ The index (starting) page for the application.
    """
    response = pyramid.renderers.render_to_response("local:site/templates/index.jinja2",
                                                    dict(),
                                                    request=request)
    return response


@pyramid.view.view_config(route_name='view.create_user', request_method='GET')
def createNewUserPage(request):
    """ The page for creating a new user.
    """
    response = pyramid.renderers.render_to_response("local:site/templates/create_user.jinja2",
                                                    dict(),
                                                    request=request)
    return response


@pyramid.view.view_config(route_name='view.search_users', request_method='GET')
def searchForUsers(request):
    """ The page for searching for users.
    """
    # TODO: Get the url parameters for nickname

    response = pyramid.renderers.render_to_response("local:site/templates/search_users.jinja2",
                                                    dict(),
                                                    request=request)
    return response


@pyramid.view.view_config(route_name='view.display_battles', request_method='GET')
def displayBattlesPage(request):
    """ The page for displaying battles.
    """
    # TODO: Get the url parameters for start and end times.

    response = pyramid.renderers.render_to_response("local:site/templates/display_battles.jinja2",
                                                    dict(),
                                                    request=request)
    return response


# ---------------------------------------------------------------------------------------------
# Module test harness
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the test harness for the module")
    sys.exit(0)
