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
import dateutil.parser
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
USER_ATTR_LOSSES = "loses"
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
    USER_ATTR_LOSSES,
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

        # TODO: Supply this value from a higher level (read config file install by Chef)
        # in case we want to run Redis on it's own node. That would also allow for multiple
        # web servers running this code since they would all coordinate via the backend Redis.
        # For now hardcode it to the IP address we're using for the VM.
        self.__datastore_server = "10.0.0.10"

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

    # ---------------------------------------------------------------
    # User creation/removal
    # ---------------------------------------------------------------
    def createUser(self, first_name, last_name, nick_name, password):
        """ Create a new unique user record. Returns the new user uid.
        """
        #print("DEBUG: Creating user ('%s', '%s', '%s')..." % (first_name, last_name, nick_name))

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
        user_data[USER_ATTR_LOSSES] = 0
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
        #print("DEBUG: Removing user '%s'..." % (user_uid))

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        nick_name = self._getDatastoreConnection().hget(user_key, USER_ATTR_NICK_NAME)

        # Delete the entry from the nick name to user id hash table.
        # Delete the entry for the user.
        self._getDatastoreConnection().hdel(USER_NICK_NAMES_TO_UID, nick_name)
        self._getDatastoreConnection().delete(user_key)

    def getUserInfo(self, user_uid):
        """ Get information about a user.
        """
        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        user_info = self._getDatastoreConnection().hgetall(user_key)
        del user_info[USER_ATTR_PASSWORD]
        del user_info[USER_ATTR_SALT]
        return user_info

    # ---------------------------------------------------------------
    # Getting users
    # ---------------------------------------------------------------
    def getAllUserUids(self):
        """ Return a list of all user uids.
        """
        # TODO: Returning this won't scale well as the total number of users
        # gets large. This will need to return an iterator.
        all_user_uids = self._getDatastoreConnection().hvals(USER_NICK_NAMES_TO_UID)
        return all_user_uids

    def getAllUserNicknames(self):
        """ Return a list of all user uids.
        """
        # TODO: Returning this won't scale well as the total number of users
        # gets large. This will need to return an iterator.
        all_nicknames = self._getDatastoreConnection().hkeys(USER_NICK_NAMES_TO_UID)
        return all_nicknames

    def getUserIdFromNickName(self, nick_name):
        """ Get the user's uid given their nick name.
        """
        user_uid = None
        if self._getDatastoreConnection().hexists(USER_NICK_NAMES_TO_UID, nick_name):
            user_uid = self._getDatastoreConnection().hget(USER_NICK_NAMES_TO_UID, nick_name)
        return user_uid

    def getNickNameFromUserId(self, user_uid):
        """ Get the nick name given user's uid.
        """
        nick_name = self.getUserData(user_uid, USER_ATTR_NICK_NAME)
        return nick_name

    def searchUsers(self, search_nickname):
        """ Return a list of all user uids that match against the partial nickname.
        """
        # TODO: Scrub the incoming search_nickname. The odds of something bad in this
        # are low since it is a matching expression, but frankly you never know how the
        # underlying implementation is built.

        #print("DEBUG: Searching users stash for '%s'..." % search_nickname)
        users = dict()
        iterator = self._getDatastoreConnection().hscan_iter(USER_NICK_NAMES_TO_UID, match="*" + search_nickname + "*")
        while True:
            try:
                nick_name, user_uid = iterator.next()
                users[nick_name] = user_uid
            except StopIteration:
                break
        return users

    # ---------------------------------------------------------------
    # Authenticating users
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # Custom update user attributes methods
    # ---------------------------------------------------------------
    def incrementUserWins(self, user_uid):
        """ Increment the user's win counter.
        """
        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        self._getDatastoreConnection().hincrby(user_key, USER_ATTR_WINS)

        # Bump up the current win streak as well.
        self._getDatastoreConnection().hincrby(user_key, USER_ATTR_CURRENT_WIN_STREAK)

    def incrementUserLoses(self, user_uid):
        """ Increment the user's loses counter.
        """
        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        self._getDatastoreConnection().hincrby(user_key, USER_ATTR_LOSSES)

        # Reset the current win streak back to zero. Wah-wah!
        self._getDatastoreConnection().hset(user_key, USER_ATTR_CURRENT_WIN_STREAK, 0)

    def updateUserPassword(self, user_uid, new_password):
        """ Update the user's password.
        """
        self.setUserData(user_uid, USER_ATTR_PASSWORD, new_password)

    def updateLastSeenForUser(self, user_uid):
        """ Update the last seen attribute for the given user.
        """
        last_seen = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.setUserData(user_uid, USER_ATTR_LAST_SEEN, last_seen)

    # ---------------------------------------------------------------
    # General update user attributes methods
    # ---------------------------------------------------------------
    def getUserData(self, user_uid, attribute):
        """ Get the vaule for a given user attribute.
        """
        #print("DEBUG: Getting user data (%s, %s)..." % (user_uid, attribute))

        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        value = self._getDatastoreConnection().hget(user_key, attribute)
        return value

    def setUserData(self, user_uid, attribute, value):
        """ Set the vaule for a given user attribute.
        """
        #print("DEBUG: Setting user data (%s, %s, %s)..." % (user_uid, attribute, value))

        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        if attribute == USER_ATTR_PASSWORD:
            new_salt = self._generateSalt()
            new_hashed_password = self._hashPassword(new_salt, value)
            self._getDatastoreConnection().hset(user_key, USER_ATTR_SALT, new_salt)
            self._getDatastoreConnection().hset(user_key, USER_ATTR_PASSWORD, new_hashed_password)
        else:
            self._getDatastoreConnection().hset(user_key, attribute, value)

        # TODO: Nickname updates will need to update the overall list that maps
        # from nickname to uid.
        # or
        # TODO: Don't allow nicknames to be updated.

    def unsetUserData(self, user_uid, attribute):
        """ Unset the vaule for a given user attribute.
        """
        #print("DEBUG: Unsetting user data (%s, %s)..." % (user_uid, attribute))

        if attribute not in USER_ATTRS:
            raise UsersStashInvalidAttributeError()

        user_key = self._getDatastoreKey(USER_PREFIX, user_uid)
        self._getDatastoreConnection().hdel(user_key, attribute)

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

    # ---------------------------------------------------------------
    # Public methods
    # ---------------------------------------------------------------
    def createBattleLog(self, attacker_uid, defender_uid, winner_uid, start_time, end_time):
        """ Create a new battle log entry.
        """
        #print("DEBUG: Creating new battle log...")

        loser_uid = attacker_uid
        if attacker_uid == winner_uid:
            loser_uid = defender_uid

        start_time = self._reformatDate(start_time)
        end_time = self._reformatDate(end_time)

        battle_id = string.join((random.choice(string.ascii_letters) for i in range(20)), "")
        battle_key = BATTLE_PREFIX + "." + battle_id + "." + start_time + "." + end_time
        battle_data = dict()
        battle_data[BATTLE_ATTR_ATTACKER_UID] = attacker_uid
        battle_data[BATTLE_ATTR_DEFENDER_UID] = defender_uid
        battle_data[BATTLE_ATTR_WINNER_UID] = winner_uid

        # TODO: Whether or not to store these as separate attributes in the hash
        # (which does take up space) or let them come from the key name. Leaning
        # to key name due to the space issue. At scale that becomes a non-trivial
        # problem. Sharding on the keys eventually (based on the time, assuming
        # access patterns favor newer information over older).
        # or
        # Store the battle logs in a relational database.
        battle_data[BATTLE_ATTR_BATTLE_START_TIME] = start_time
        battle_data[BATTLE_ATTR_BATTLE_END_TIME] = end_time
        self._getDatastoreConnection().hmset(battle_key, battle_data)

        # Update the win and lose counters for the attacker and defender.
        users_stash = UsersStash()
        users_stash.incrementUserWins(winner_uid)
        users_stash.incrementUserLoses(loser_uid)


    def searchBattleLogs(self, start_time, end_time):
        """ Get the list of battle logs that occur between the start
            and end times.
        """
        #print("DEBUG: Searching for battle logs between %s and %s..." % (start_time, end_time))

        start_dtobj = dateutil.parser.parse(start_time)
        end_dtobj = dateutil.parser.parse(end_time)

        if not start_dtobj < end_dtobj:
            raise BattlesStashStartDateNotBeforeEndData()

        start_year = start_dtobj.year
        start_month = start_dtobj.month
        start_day = start_dtobj.day

        # TODO: Build a better match string. Really though, the battle logs should probably
        # be stored someplace other than Redis given the nature of how they are used. I'd
        # probably stick an AMQP system in place to receive incoming battle log messages and
        # warehouse them asynchronously.
        match_string = "*"

        battle_logs = list()
        iterator = self._getDatastoreConnection().scan_iter(match=match_string)
        while True:
            try:
                battle_log_key = iterator.next()
                tmp_1, tmp_2, battle_start_time, battle_end_time = string.split(battle_log_key, ".")

                battle_start_dtobj = dateutil.parser.parse(battle_start_time)
                battle_end_dtobj = dateutil.parser.parse(battle_end_time)

                should_include_log = False
                if start_dtobj < battle_start_dtobj and battle_start_dtobj < end_dtobj:
                    should_include_log = True
                elif start_dtobj < battle_end_dtobj and battle_end_dtobj < end_dtobj:
                    should_include_log = True

                if should_include_log:
                    battle_log_info = self._getDatastoreConnection().hgetall(battle_log_key)
                    battle_logs.append(battle_log_info)

            except StopIteration:
                break

        return battle_logs

#        start_time = self._reformatDate(start_time)
#        end_time = self._reformatDate(end_time)


    # ---------------------------------------------------------------
    # Protected methods
    # ---------------------------------------------------------------
    def _reformatDate(self, in_date):
        """ Take in a string date and reform it for use as part of a
            battle log key.
        """
        in_dtobj = dateutil.parser.parse(in_date)
        out_date = in_dtobj.isoformat()
        return out_date


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
class BattlesStashError(StashError):
    pass

class BattlesStashStartDateNotBeforeEndData(StashError):
    pass

# ---------------------------------------------------------------------------------------------
# Module test harness
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the test harness for the module")
    sys.exit(0)
