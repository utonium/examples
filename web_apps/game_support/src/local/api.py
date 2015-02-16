#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
local/api.py

The API for the example customer support system.

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import datetime
import json
import os
import re
import string

import pyramid.httpexceptions
import pyramid.renderers
import pyramid.security
import pyramid.view

import local.stash

# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# API Methods
# ---------------------------------------------------------------------------------------------
@pyramid.view.view_config(
    route_name='api.create_user', renderer='json', request_method='POST'
)
def createUser(request):
    """ Create a new user.
    """
    print("LOG: creating new user...")

    errors = list()
    required_params = [
        'first', 'last', 'nickname', 'password',
    ]
    for required_param in required_params:
        if required_param not in request.POST:
            errors.append("Required parameter, '%s', missing" % required_param)

    if len(errors):
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = string.join(errors, "; ")
        return response
        
    first_name = request.POST['first']
    last_name = request.POST['last']
    nick_name = request.POST['nickname']
    password = request.POST['password']

    user_uid = None
    try:
        users_stash = local.stash.UsersStash()
        user_uid = users_stash.createUser(first_name, last_name, nick_name, password)

    except local.stash.UsersStashNickNameTakenError, e:
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = "Nickname '%s' is already in use, please select another one" % nick_name
        return response

    except local.stash.StashError, e:
    # TODO: This should catch other exceptions from the stash layer, such as not being able
    # to reach the Redis server, etc.

    response = dict()
    response['error'] = False
    response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response['userid'] = user_uid

    return response


@pyramid.view.view_config(
    route_name='api.modify_user', renderer='json', request_method='PUT'
)
def modifyUser(request):
    """ Modify an existing user.
    """
    print("LOG: modifying user...")

    if pyramid.security.authenticated_userid(request) is None:
        print("INFO: Unauthenticated access attempted")
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = "Unauthenticated access attempted, please supply a valid username/password"
        return response

    user_uid = request.matchdict['user_id']
    attribute = request.POST['field']
    value = request.POST['value']

    # Block certain attributes from being updated directly by this
    # interface.
    valid_attributes = [
        local.stash.USER_ATTR_FIRST_NAME,
        local.stash.USER_ATTR_LAST_NAME,
        local.stash.USER_ATTR_PASSWORD,
    ]
    if attribute not in valid_attributes:
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = "Attribute '%s' does not allow update" % attribute
        return response

    try:
        users_stash = local.stash.UsersStash()
        users_stash.setUserData(user_uid, attribute, value)
        users_stash.updateLastSeenForUser(user_uid)

    except local.stash.UsersStashInvalidAttributeError, e:
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = "Invalid attribute name, '%s', ignored " % attribute
        return response

    # TODO: Catch other exceptions here. Probably should have an overall exception handler
    # to keep all exceptions as internal errors and allow for graceful recovery.

    response = dict()
    response['error'] = False
    response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return response


@pyramid.view.view_config(
    route_name='api.create_battle_log', renderer='json', request_method='POST'
)
def createBattleLog(request):
    """ Create a battle log entry for the user.
    """
    print("LOG: creating battle log...")

    if pyramid.security.authenticated_userid(request) is None:
        print("INFO: Unauthenticated access attempted")
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = "Unauthenticated access attempted, please supply a valid username/password"
        return response

    errors = list()
    required_params = [
        'attacker', 'defender', 'winner', 'start', 'end',
    ]
    for required_param in required_params:
        if required_param not in request.POST:
            errors.append("Required parameter, '%s', missing" % required_param)

    if len(errors):
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = string.join(errors, "; ")
        return response
        
    attacker_uid = request.POST['attacker']
    defender_uid = request.POST['defender']
    winner_uid = request.POST['winner']
    start_time = request.POST['start']
    end_time = request.POST['end']

    try:
        battles_stash = local.stash.BattlesStash()
        battles_stash.createBattleLog(attacker_uid, defender_uid, winner_uid, start_time, end_time)

    except local.stash.BattlesStashError, e:
        response = dict() 
        response['error'] = True
        response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response['msg'] = "Unknown error while attempting to create new battle log"
        return response

    # TODO: Catch other exceptions here. Probably should have an overall exception handler
    # to keep all exceptions as internal errors and allow for graceful recovery.

    response = dict()
    response['error'] = False
    response['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return response


@pyramid.view.view_config(
    route_name='api.list_users', renderer='json', request_method='GET'
)
def listUsers(request):
    """ Get a list of the active users.
    """
    print("LOG: Getting list of users...")

    if pyramid.security.authenticated_userid(request) is None:
        return pyramid.httpexceptions.HTTPUnauthorized()

    users_stash = local.stash.UsersStash()
    users = users_stash.getAllUsers()
    return users


# ---------------------------------------------------------------------------------------------
# Module test harness
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the test harness for the module")
    sys.exit(0)
