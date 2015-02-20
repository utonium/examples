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


@pyramid.view.view_config(route_name='view.display_user', request_method='GET')
def displayUserPage(request):
    """ Display a detail page about a user.
    """
    user_uid = request.matchdict['user_uid']

    results = dict()
    results['error'] = ""

    users_stash = local.stash.UsersStash()
    user_info = users_stash.getUserInfo(user_uid)

    results['user'] = user_info

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
    print("DEBUG: Displaying battle logs...")

    results = dict()
    results['error'] = ""
    results['initial_start_time'] = ""
    results['initial_end_time'] = ""
    results['logs'] = list()

    if 'start_time' not in request.GET or request.GET['start_time'] == "":
        results['error'] = "Please specify a start time for displaying battle logs."

    if 'end_time' not in request.GET or request.GET['end_time'] == "":
        results['error'] = "Please specify a end time for displaying battle logs."

    if results['error']:
        # Send back the entered start and end times since there was an error.
        if 'start_time' in request.GET:
            results['initial_start_time'] = request.GET['start_time']

        if 'end_time' in request.GET:
            results['initial_end_time'] = request.GET['end_time']

    else:
        start_time = request.GET['start_time']
        end_time = request.GET['end_time']

        # TODO: Use this to map from UID to nickname.
        users_stash = local.stash.UsersStash()

        battles_stash = local.stash.BattlesStash()
        battle_logs = battles_stash.searchBattleLogs(start_time, end_time)

        for battle_log in battle_logs:
            tmp = dict()
            tmp['attacker_nick_name'] = battle_log['attacker_uid']
            tmp['defender_nick_name'] = battle_log['defender_uid']
            tmp['winner_nick_name'] = battle_log['winner_uid']
            tmp['battle_start_time'] = battle_log['battle_start_time']
            tmp['battle_end_time'] = battle_log['battle_end_time']
            results['logs'].append(tmp)

    response = pyramid.renderers.render_to_response("local:site/templates/display_battles.jinja2",
                                                    results,
                                                    request=request)
    return response


# ---------------------------------------------------------------------------------------------
# Module test harness
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the test harness for the module")
    sys.exit(0)
