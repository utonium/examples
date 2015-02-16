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
import nose.plugins.skip
import nose.tools
import sys

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
    users_stash = local.stash.UsersStash()

    helper.TEST_USER_01_UID = users_stash.createUser(helper.TEST_USER_01_FIRST_NAME,
                                                     helper.TEST_USER_01_LAST_NAME,
                                                     helper.TEST_USER_01_NICK_NAME,
                                                     helper.TEST_USER_01_PASSWORD)
    print("Test user 01 uid is '%s'" % helper.TEST_USER_01_UID)
    nose.tools.assert_is_not_none(helper.TEST_USER_01_UID)

    helper.TEST_USER_02_UID = users_stash.createUser(helper.TEST_USER_02_FIRST_NAME,
                                                     helper.TEST_USER_02_LAST_NAME,
                                                     helper.TEST_USER_02_NICK_NAME,
                                                     helper.TEST_USER_02_PASSWORD)
    print("Test user 02 uid is '%s'" % helper.TEST_USER_02_UID)
    nose.tools.assert_is_not_none(helper.TEST_USER_02_UID)

    helper.TEST_USER_03_UID = users_stash.createUser(helper.TEST_USER_03_FIRST_NAME,
                                                     helper.TEST_USER_03_LAST_NAME,
                                                     helper.TEST_USER_03_NICK_NAME,
                                                     helper.TEST_USER_03_PASSWORD)
    print("Test user 03 uid is '%s'" % helper.TEST_USER_03_UID)
    nose.tools.assert_is_not_none(helper.TEST_USER_03_UID)


def test_updateUsers():
    """ Test to update existing users.
    """
    print("Executing test_updateUsers...")
    users_stash = local.stash.UsersStash()

    helper.TEST_USER_01_PASSWORD = "s0m3-n3w-P@55w0rd!-01"
    users_stash.updateUserPassword(helper.TEST_USER_01_UID, helper.TEST_USER_01_PASSWORD)

    helper.TEST_USER_02_PASSWORD = "s0m3-n3w-P@55w0rd!-02"
    users_stash.updateUserPassword(helper.TEST_USER_02_UID, helper.TEST_USER_02_PASSWORD)

    helper.TEST_USER_03_PASSWORD = "s0m3-n3w-P@55w0rd!-03"
    users_stash.updateUserPassword(helper.TEST_USER_03_UID, helper.TEST_USER_03_PASSWORD)


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
