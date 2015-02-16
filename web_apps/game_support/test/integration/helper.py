#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
integration/helper.py

Things used by all the tests.

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import os
import sys


# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------

TEST_USER_01_UID = None
TEST_USER_01_FIRST_NAME = "kevin"
TEST_USER_01_LAST_NAME = "cureton"
TEST_USER_01_NICK_NAME = "kevtonium"
TEST_USER_01_PASSWORD = "p@ssw0rd01"

TEST_USER_02_UID = None
TEST_USER_02_FIRST_NAME = "bob"
TEST_USER_02_LAST_NAME = "smith"
TEST_USER_02_NICK_NAME = "bobtonium"
TEST_USER_02_PASSWORD = "p@ssw0rd02"

TEST_USER_03_UID = None
TEST_USER_03_FIRST_NAME = "ann"
TEST_USER_03_LAST_NAME = "jones"
TEST_USER_03_NICK_NAME = "anntonium"
TEST_USER_03_PASSWORD = "p@ssw0rd03"


# ---------------------------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------
# Execute main and exit with the returned status.
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the module test harness")
    sys.exit(0)
