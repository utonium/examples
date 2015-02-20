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
import os
import nose.tools
import sys

import helper
import local.stash


# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------
TEST_NAME = "test_0001_stash"


# ---------------------------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------------------------
def setup():
    print("%s setup..." % TEST_NAME)

def teardown():
    print("%s teardown..." % TEST_NAME)

    # TODO: Remove the created battle logs

def test_createUsers():
    """ Test to create new users.
    """
    print("Executing test_createUsers...")
    users_stash = local.stash.UsersStash()

    helper.TEST_USER_01_UID = users_stash.createUser(helper.TEST_USER_01_FIRST_NAME,
                                                     helper.TEST_USER_01_LAST_NAME,
                                                     helper.TEST_USER_01_NICK_NAME,
                                                     helper.TEST_USER_01_PASSWORD)
    nose.tools.assert_not_equal(helper.TEST_USER_01_UID, None)

    helper.TEST_USER_02_UID = users_stash.createUser(helper.TEST_USER_02_FIRST_NAME,
                                                     helper.TEST_USER_02_LAST_NAME,
                                                     helper.TEST_USER_02_NICK_NAME,
                                                     helper.TEST_USER_02_PASSWORD)
    nose.tools.assert_not_equal(helper.TEST_USER_02_UID, None)

    helper.TEST_USER_03_UID = users_stash.createUser(helper.TEST_USER_03_FIRST_NAME,
                                                     helper.TEST_USER_03_LAST_NAME,
                                                     helper.TEST_USER_03_NICK_NAME,
                                                     helper.TEST_USER_03_PASSWORD)
    nose.tools.assert_not_equal(helper.TEST_USER_03_UID, None)

def test_updateUsers():
    """ Test to update existing users.
    """
    print("Executing test_updateUsers...")
    users_stash = local.stash.UsersStash()

    users_stash.updateUserPassword(helper.TEST_USER_01_UID, "s0m3-n3w-P@55w0rd!-01")
    helper.TEST_USER_01_PASSWORD = "s0m3-n3w-P@55w0rd!-01"

    users_stash.updateUserPassword(helper.TEST_USER_02_UID, "s0m3-n3w-P@55w0rd!-02")
    helper.TEST_USER_02_PASSWORD = "s0m3-n3w-P@55w0rd!-02"

    users_stash.updateUserPassword(helper.TEST_USER_03_UID, "s0m3-n3w-P@55w0rd!-03")
    helper.TEST_USER_03_PASSWORD = "s0m3-n3w-P@55w0rd!-03"

def test_createBattleLogs():
    """ Test to create a number of battle logs.
    """
    print("Executing test_createBattleLogs...")
    battles_stash = local.stash.BattlesStash()

    battles_stash.createBattleLog(helper.TEST_USER_01_UID, helper.TEST_USER_02_UID,
                                  helper.TEST_USER_01_UID, "2014-10-31T20:15:35", "2014-10-31T20:43:12")
    battles_stash.createBattleLog(helper.TEST_USER_01_UID, helper.TEST_USER_03_UID,
                                  helper.TEST_USER_03_UID, "2014-11-10T11:12:13", "2014-11-10T11:37:53")
    battles_stash.createBattleLog(helper.TEST_USER_02_UID, helper.TEST_USER_03_UID,
                                  helper.TEST_USER_03_UID, "2014-11-15T22:13:15", "2014-11-15T23:07:43")
    battles_stash.createBattleLog(helper.TEST_USER_01_UID, helper.TEST_USER_02_UID,
                                  helper.TEST_USER_02_UID, "2014-12-25T00:13:22", "2014-12-25T04:20:00")
    battles_stash.createBattleLog(helper.TEST_USER_01_UID, helper.TEST_USER_03_UID,
                                  helper.TEST_USER_03_UID, "2014-12-31T23:55:35", "2015-01-01T01:48:33")

def test_removeUsers():
    """ Test to remove users.
    """
    print("Executing test_removeUsers...")
    users_stash = local.stash.UsersStash()

    users_stash.removeUser(helper.TEST_USER_01_UID)
    users_stash.removeUser(helper.TEST_USER_02_UID)
    users_stash.removeUser(helper.TEST_USER_03_UID)

    all_users = users_stash.getAllUserUids()
    nose.tools.assert_equal(len(all_users), 0)

# ---------------------------------------------------------------------------------------------
# Execute main and exit with the returned status.
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the module test harness")
    sys.exit(0)
