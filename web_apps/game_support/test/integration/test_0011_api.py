#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
integration/test_stash.py

Test associated with stash.py module.

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import json
import os
import nose.plugins.skip
import nose.tools
import sys
import requests
import urllib
import urllib2

import helper
import local.stash


# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------
TEST_NAME = "test_stash"


# ---------------------------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------------------------
def setup():
    print("%s setup..." % TEST_NAME)


def teardown():
    print("%s teardown..." % TEST_NAME)


def test_createUsers():
    """ Test to create new users.
    """
    print("Executing test_createUsers...")

    url = 'http://localhost:8080/api/users'

    payload = {
      'first' : helper.TEST_USER_01_FIRST_NAME,
      'last' : helper.TEST_USER_01_LAST_NAME,
      'nickname' : helper.TEST_USER_01_NICK_NAME,
      'password' : helper.TEST_USER_01_PASSWORD,
    }
    req = requests.post(url, data=payload)
    result_01 = req.json()
    helper.TEST_USER_01_UID = result_01['userid']

    payload = {
      'first' : helper.TEST_USER_02_FIRST_NAME,
      'last' : helper.TEST_USER_02_LAST_NAME,
      'nickname' : helper.TEST_USER_02_NICK_NAME,
      'password' : helper.TEST_USER_02_PASSWORD,
    }
    req = requests.post(url, data=payload)
    result_02 = req.json()
    helper.TEST_USER_02_UID = result_02['userid']

    payload = {
      'first' : helper.TEST_USER_03_FIRST_NAME,
      'last' : helper.TEST_USER_03_LAST_NAME,
      'nickname' : helper.TEST_USER_03_NICK_NAME,
      'password' : helper.TEST_USER_03_PASSWORD,
    }
    req = requests.post(url, data=payload)
    result_03 = req.json()
    helper.TEST_USER_03_UID = result_03['userid']

    nose.tools.assert_false(result_01['error'])
    nose.tools.assert_false(result_02['error'])
    nose.tools.assert_false(result_03['error'])


def test_unauthenticatedAccess():
    """ Test to verify unauthenicated access doesn't work.
    """
    print("Executing test_unauthenticatedAccess...")

    url = "http://localhost:8080/api/users/"
    payload = {
      "field" : "first",
      "value" : "grumpy",
    }

    req = requests.put(url + helper.TEST_USER_01_UID,
                       data=payload, auth=(helper.TEST_USER_01_UID, "some_bogus_password"))
    result = req.json()
    nose.tools.assert_true(result['error'])


def test_updateUserPasswords():
    """ Test to update user passwords.
    """
    print("Executing test_updateUserPasswords...")

    url = "http://localhost:8080/api/users/"
    new_password = "s0m3-n3w-P@55w0rd!-"

    payload = {
      "field" : "password",
      "value" : new_password + "01",
    }
    req = requests.put(url + helper.TEST_USER_01_UID,
                       data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_false(result['error'])
    helper.TEST_USER_01_PASSWORD = new_password + "01"

    payload = {
      "field" : "password",
      "value" : new_password + "02",
    }
    req = requests.put(url + helper.TEST_USER_02_UID,
                       data=payload, auth=(helper.TEST_USER_02_UID, helper.TEST_USER_02_PASSWORD))
    result = req.json()
    nose.tools.assert_false(result['error'])
    helper.TEST_USER_02_PASSWORD = new_password + "02"

    payload = {
      "field" : "password",
      "value" : new_password + "03",
    }
    req = requests.put(url + helper.TEST_USER_03_UID,
                       data=payload, auth=(helper.TEST_USER_03_UID, helper.TEST_USER_03_PASSWORD))
    result = req.json()
    nose.tools.assert_false(result['error'])
    helper.TEST_USER_03_PASSWORD = new_password + "03"

def test_updateOtherUserAttributes01():
    """ Test to update other user attributes.
    """
    print("Executing test_updateOtherUserAttributes01...")

    url = "http://localhost:8080/api/users/"
    payload = {
      "field" : "first_name",
      "value" : "kev",
    }
    req = requests.put(url + helper.TEST_USER_01_UID,
                       data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_false(result['error'])

def test_updateOtherUserAttributes02():
    """ Test to update other user attributes.
    """
    print("Executing test_updateOtherUserAttributes02...")

    url = "http://localhost:8080/api/users/"
    payload = {
      "field" : "last_name",
      "value" : "cureton-lemberg",
    }
    req = requests.put(url + helper.TEST_USER_01_UID,
                       data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_false(result['error'])

def test_updateOtherUserAttributes03():
    """ Test to update other user attributes.
    """
    print("Executing test_updateOtherUserAttributes03...")

    url = "http://localhost:8080/api/users/"
    payload = {
      "field" : "wins",
      "value" : "1000000",
    }
    req = requests.put(url + helper.TEST_USER_01_UID,
                       data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_true(result['error'])

def test_createBattleLogs():
    """ Test to create a number of battle logs.
    """
    print("Executing test_createBattleLogs...")

    # TODO: Create the battle logs using the API instead of directly
    # with the stash.

    url = "http://localhost:8080/api/battles"

    payload = {
      "attacker" : helper.TEST_USER_01_UID,
      "defender" : helper.TEST_USER_02_UID,
      "winner" : helper.TEST_USER_01_UID,
      "start" : "2014-10-31T20:15:35",
      "end" : "2014-10-31T20:43:12",
    }
    req = requests.put(url, data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_true(result['error'])

    payload = {
      "attacker" : helper.TEST_USER_01_UID,
      "defender" : helper.TEST_USER_03_UID,
      "winner" : helper.TEST_USER_03_UID,
      "start" : "2014-11-10T11:12:13",
      "end" : "2014-11-10T11:37:53",
    }
    req = requests.put(url, data=payload, auth=(helper.TEST_USER_03_UID, helper.TEST_USER_03_PASSWORD))
    result = req.json()
    nose.tools.assert_true(result['error'])

    payload = {
      "attacker" : helper.TEST_USER_02_UID,
      "defender" : helper.TEST_USER_03_UID,
      "winner" : helper.TEST_USER_03_UID,
      "start" : "2014-11-15T22:13:15",
      "end" : "2014-11-15T23:07:43",
    }
    req = requests.put(url, data=payload, auth=(helper.TEST_USER_02_UID, helper.TEST_USER_02_PASSWORD))
    result = req.json()
    nose.tools.assert_true(result['error'])

    payload = {
      "attacker" : helper.TEST_USER_01_UID,
      "defender" : helper.TEST_USER_02_UID,
      "winner" : helper.TEST_USER_02_UID,
      "start" : "2014-12-25T00:13:22",
      "end" : "2014-12-25T04:20:00",
    }
    req = requests.put(url, data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_true(result['error'])

    payload = {
      "attacker" : helper.TEST_USER_01_UID,
      "defender" : helper.TEST_USER_03_UID,
      "winner" : helper.TEST_USER_03_UID,
      "start" : "2014-12-31T23:55:35",
      "end" : "2015-01-01T01:48:33",
    }
    req = requests.put(url, data=payload, auth=(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD))
    result = req.json()
    nose.tools.assert_true(result['error'])


def test_removeUsers():
    """ Test to remove users.
    """
    print("Executing test_removeUsers...")
    users_stash = local.stash.UsersStash()

    users_stash.removeUser(helper.TEST_USER_01_UID)
    users_stash.removeUser(helper.TEST_USER_02_UID)
    users_stash.removeUser(helper.TEST_USER_03_UID)

    all_users = users_stash.getAllUsers()
    nose.tools.assert_equal(len(all_users), 0)

# ---------------------------------------------------------------------------------------------
# Execute main and exit with the returned status.
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the module test harness")
    sys.exit(0)