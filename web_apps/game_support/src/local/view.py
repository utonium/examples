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

import local.stash

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


@pyramid.view.view_config(route_name='view.create_user', request_method='GET')
def displayUserPage(request):
    """ Display a detail page about a user.
    """
    results = dict()

    response = pyramid.renderers.render_to_response("local:site/templates/user_detail.jinja2",
                                                    results,
                                                    request=request)
    return response


@pyramid.view.view_config(route_name='view.search_users', request_method='GET')
def searchForUsers(request):
    """ The page for searching for users.
    """
    print("DEBUG: Searching for users...")

    results = dict()
    results['error'] = ""
    results['users'] = list()

    if 'nickname' not in request.GET or request.GET['nickname'] == "":
        results['error'] = "Please specify a nick name for the search."

    else:
        users_stash = local.stash.UsersStash()
        found_users = users_stash.searchUsers(request.GET['nickname'])
        
        tmp_users = list()
        for nick_name in found_users.keys():
            user_uid = found_users[nick_name]
            tmp = dict()
            tmp['url'] = "/users/%s" % user_uid
            tmp['nickname'] = nick_name 
            tmp_users.append(tmp)
        results['users'] = tmp_users

    response = pyramid.renderers.render_to_response("local:site/templates/search_users.jinja2",
                                                    results,
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
