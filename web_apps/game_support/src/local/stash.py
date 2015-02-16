#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
local/stash.py

The API for accessing data in the Redis cluster.

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# TODO
#
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import datetime
import hashlib
import os
import random
import string
import sys
import uuid

import redis

# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------

# -----------------------------------------------------
# Users datastore
# -----------------------------------------------------
USER_DATASTORE_NAME = "Users"
USER_PREFIX = "user"

USER_ATTR_UID = "uid"
USER_ATTR_FIRST_NAME = "first_name"
USER_ATTR_LAST_NAME = "last_name"
USER_ATTR_NICK_NAME = "nick_name"
USER_ATTR_PASSWORD = "password"
USER_ATTR_SALT = "pw_salt"
USER_ATTR_WINS = "wins"
USER_ATTR_LOSES = "loses"
USER_ATTR_CURRENT_WIN_STREAK = "current_win_streak"
USER_ATTR_CREATED = "created"
USER_ATTR_LAST_SEEN = "last_seen"
USER_ATTRS = [
    USER_ATTR_UID,
    USER_ATTR_FIRST_NAME,
    USER_ATTR_LAST_NAME,
    USER_ATTR_NICK_NAME,
    USER_ATTR_PASSWORD,
    USER_ATTR_SALT,
    USER_ATTR_WINS,
    USER_ATTR_LOSES,
    USER_ATTR_CURRENT_WIN_STREAK,
    USER_ATTR_CREATED,
    USER_ATTR_LAST_SEEN,
]

USER_NICK_NAMES_TO_UID = "nick_names_to_uid"

# -----------------------------------------------------
# Battles datastore
# -----------------------------------------------------
BATTLE_DATASTORE_NAME = "Battles"

BATTLE_PREFIX = "battle"

BATTLE_ATTR_ATTACKER_UID = "attacker_uid"
BATTLE_ATTR_DEFENDER_UID = "defender_uid"
BATTLE_ATTR_WINNER_UID = "winner_uid"
BATTLE_ATTR_BATTLE_START_TIME = "battle_start_time"
BATTLE_ATTR_BATTLE_END_TIME = "battle_end_time"
BATTLE_ATTRS = [
    BATTLE_ATTR_ATTACKER_UID,
    BATTLE_ATTR_DEFENDER_UID,
    BATTLE_ATTR_WINNER_UID,
    BATTLE_ATTR_BATTLE_START_TIME,
    BATTLE_ATTR_BATTLE_END_TIME,
]

# ---------------------------------------------------------------
# Redis connection pool.
# ---------------------------------------------------------------
CONNECTION_POOL = dict()

# ---------------------------------------------------------------------------------------------
# Stash classes
# ---------------------------------------------------------------------------------------------
class StashCommon(object):
    """ The common methods used by both stashes.
    """
    # ---------------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------------
    def __init__(self, datastore_name, datastore_port):
        """ Initialize the Redis datastore object. This include creating connection pools, if they
            don't already exist, for the datastore.
        """
        self.__datastore_name = datastore_name
        self.__datastore_port = datastore_port

        # TODO: Supply this value from a higher level in case we want to run Redis
        # on it's own node. That would also allow for multiple web servers running this
        # code since they would all coordinate via the backend Redis.
        self.__datastore_server = "localhost"

        if self.__datastore_port not in CONNECTION_POOL:
            try:
                CONNECTION_POOL[self.__datastore_port] = redis.ConnectionPool(host=self.__datastore_server,
                                                                              port=self.__datastore_port, db=0)
            except redis.RedisError, e:
                msg = "Redis general exception caught adding to the pool: %s" % str(e)
                print(msg)
                raise StashInitializationError()

    # ---------------------------------------------------------------
    # Protected methods
    # ---------------------------------------------------------------
    def _getDatastoreKey(self, prefix, dsuid=None):
        """ Get a datastore key using the given prefix. If no datastore unique id (dsuid) is
            provided, one will be created.
        """
        datastore_key = None
        if dsuid is not None:
            datastore_key = "%s:%s" % (prefix, dsuid)
        else:
            dsuid = self._getDatastoreUID()
            datastore_key = "%s:%s" % (prefix, dsuid)
            while self._getDatastoreConnection().exists(datastore_key):
                # The generated DSUID is already in use! Throw it out and try a new
                # one until we get one that hasn't been used before.
                dsuid = unicode(uuid.uuid4())
                datastore_key = "%s:%s" % (prefix, dsuid)

        return datastore_key

    def _parseDatastoreKey(self, datastore_key):
        """ Parse the datastore key, returning each component.
        """
        datastore_prefix = None
        datastore_uid = None
        try:
            datastore_prefix, datastore_uid = datastore_key.split(":")
        except ValueError as e:
            msg = "Invalid datastore key, %s, unable to parse." % datastore_key
            print(msg)
            raise am.pipeline.stash.error.StashError(msg)
        return (datastore_prefix, datastore_uid)

    def _uidFromKey(self, datastore_key):
        """ Extract the datastore uid from the given datastore key.
        """
        (datastore_prefix, datastore_uid) = self._parseDatastoreKey(datastore_key)
        return datastore_uid

    def _getDatastoreUID(self):
        """ Get a datastore unique id.
        """
        dsuid = unicode(uuid.uuid4())
        return dsuid

    def _getDatastoreConnection(self):
        """ Get a Redis connection object.
        """
        redis_obj = None
        try:
            redis_obj = redis.Redis(connection_pool=CONNECTION_POOL[self.__datastore_port])
        except redis.RedisError, e:
            msg = "Redis general exception caught creating object: %s" % str(e)
            print(msg)
            raise StashConnectionError(msg)
        return redis_obj


class UsersStash(StashCommon):
    """ The users stash.
    """
    def __init__(self):
        super(UsersStash, self).__init__("Users", "26000")

    def createUser(self, first_name, last_name, nick_name, password):
        """ Create a new unique user record. Returns the new user uid.
        """
        print("DEBUG: Creating user ('%s', '%s', '%s')..." % (first_name, last_name, nick_name))

        if self._getDatastoreConnection().hexists(USER_NICK_NAMES_TO_UID, nick_name):
            msg = "Nick name already in use"
            print(msg)
            raise UsersStashNickNameTakenError()

        user_key = self._getDatastoreKey(USER_PREFIX)
        user_uid = self._uidFromKey(user_key)

        # Generate a random salt for the user.
        salt = self._generateSalt()
        hashed_password = self._hashPassword(salt, password)

        user_data = dict()
        user_data[USER_ATTR_UID] = user_uid
        user_data[USER_ATTR_FIRST_NAME] = first_name
        user_data[USER_ATTR_LAST_NAME] = last_name
        user_data[USER_ATTR_NICK_NAME] = nick_name
        user_data[USER_ATTR_SALT] = salt
        user_data[USER_ATTR_PASSWORD] = hashed_password
        user_data[USER_ATTR_WINS] = 0
        user_data[USER_ATTR_LOSES] = 0
        user_data[USER_ATTR_CURRENT_WIN_STREAK] = 0
        user_data[USER_ATTR_CREATED] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_data[USER_ATTR_LAST_SEEN] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self._getDatastoreConnection().hmset(user_key, user_data)

        # Add the nick name to the map from nick name to uid.
        self._getDatastoreConnection().hset(USER_NICK_NAMES_TO_UID, nick_name, user_uid)

        return user_uid

    def removeUser(self, user_uid):
        """ Remove the specified user.
        """
        print("DEBUG: Removing user '%s'..." % (user_uid))

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        nick_name = self._getDatastoreConnection().hget(user_key, USER_ATTR_NICK_NAME)

        # Delete the entry from the nick name to user id hash table.
        # Delete the entry for the user.
        self._getDatastoreConnection().hdel(USER_NICK_NAMES_TO_UID, nick_name)
        self._getDatastoreConnection().delete(user_key)

    def getAllUsers(self):
        """ Return a list of all user uids.
        """
        all_users = self._getDatastoreConnection().hvals(USER_NICK_NAMES_TO_UID)
        return all_users

    def getUserIdFromNickName(self, nick_name):
        """ Get the user's uid given their nick name.
        """
        user_uid = None
        if self._getDatastoreConnection().hexists(USER_NICK_NAMES_TO_UID, nick_name):
            user_uid = self._getDatastoreConnection().hget(USER_NICK_NAMES_TO_UID, nick_name)
        return user_uid

    def updateUserPassword(self, user_uid, new_password):
        """ Update the user's password.
        """
        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        new_salt = self._generateSalt()
        new_hashed_password = self._hashPassword(new_salt, new_password)
        self._getDatastoreConnection().hset(user_key, USER_ATTR_SALT, new_salt)
        self._getDatastoreConnection().hset(user_key, USER_ATTR_PASSWORD, new_hashed_password)

    def authenticatedUserByNickname(self, nick_name, incoming_password):
        """ Given the user's nick name and password, authenticate the user
            and return the user's uid.
        """
        user_uid = self._getDatastoreConnection().hget(USER_NICK_NAMES_TO_UID, nick_name)
        auth_user_uid = self.authenticateUser(user_uid, incoming_password)
        return auth_user_uid

    def authenticatedUser(self, user_uid, incoming_password):
        """ Given the user's uid and password, authenticate the user
            and return the user's uid.
        """
        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        user_salt = self._getDatastoreConnection().hget(user_key, USER_ATTR_SALT)
        user_hashed_password = self._getDatastoreConnection().hget(user_key, USER_ATTR_PASSWORD)
        incoming_hashed_password = self._hashPassword(user_salt, incoming_password)
        if user_hashed_password == incoming_hashed_password:
            return user_uid
        else:
            return None

    def getUserData(self, user_uid, attribute):
        """ Get the vaule for a given user attribute.
        """
        print("DEBUG: Getting user data (%s, %s)..." % (user_uid, attribute))

        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        value = self._getDatastoreConnection().hget(user_key, attribute)
        return value

    def setUserData(self, user_uid, attribute, value):
        """ Set the vaule for a given user attribute.
        """
        print("DEBUG: Setting user data (%s, %s, %s)..." % (user_uid, attribute, value))

        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

        # TODO: Nickname updates will need to update the overall list that maps
        # from nickname to uid.
        # or
        # TODO: Don't allow nicknames to be updated.

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        self._getDatastoreConnection().hset(user_key, attribute, value)

    def unsetUserData(self, user_uid, attribute):
        """ Unset the vaule for a given user attribute.
        """
        print("DEBUG: Unsetting user data (%s, %s)..." % (user_uid, attribute))

        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        self._getDatastoreConnection().hdel(user_key, attribute)

    def updateLastSeenForUser(self, user_uid):
        """ Update the last seen attribute for the given user.
        """
        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._getDatastoreConnection().hset(user_key, USER_ATTR_LAST_SEEN, last_seen)

    # ---------------------------------------------------------------
    # Protected methods
    # ---------------------------------------------------------------
    def _isValidUserAttribute(self, attribute):
        """ Validate for a correct attribute name.
        """
        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

    def _generateSalt(self, length=10):
        """ Generate a random salt string.
        """
        salt = string.join((random.choice(string.ascii_letters) for i in range(length)), "")
        return salt

    def _hashPassword(self, salt, password):
        """ Encode the salt and the bare password and hash them.
        """
        hashed_password = hashlib.md5(salt + password).hexdigest()
        return hashed_password


class BattlesStash(StashCommon):
    """ The battles stash.
    """
    def __init__(self):
        super(BattlesStash, self).__init__("Battles", "26010")

    def createBattleLog(self, attacker_uid, defender_uid, winner_uid, start_time, end_time):
        """ Create a new battle log entry.
        """
        battle_key = self._getDatastoreKey(BATTLE_PREFIX)
        battle_uid = self._uidFromKey(battle_key)

        battle_data = dict()
        battle_data[BATTLE_ATTR_ATTACKER_UID] = attacker_uid
        battle_data[BATTLE_ATTR_DEFENDER_UID] = defender_uid
        battle_data[BATTLE_ATTR_WINNER_UID] = winner_uid
        battle_data[BATTLE_ATTR_BATTLE_START_TIME] = start_time
        battle_data[BATTLE_ATTR_BATTLE_END_TIME] = end_time

        self._getDatastoreConnection().hmset(battle_key, battle_data)

        return user_uid


# ---------------------------------------------------------------------------------------------
# Stash errors
# ---------------------------------------------------------------------------------------------

# General errors
class StashError(Exception):
    pass

class StashInitializationError(StashError):
    pass

class StashConnectionError(StashError):
    pass

# Users stash errors
class UsersStashError(StashError):
    pass

class UsersStashNickNameTakenError(UsersStashError):
    pass

class UsersStashInvalidAttributeError(UsersStashError):
    pass

# Battle stash errors
class BattleStashError(StashError):
    pass


# ---------------------------------------------------------------------------------------------
# Module test harness
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the test harness for the module")
    sys.exit(0)
