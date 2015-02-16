#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------
"""
local/configurator.py

The Pyramid configurator object for the site.

Copyright (c) 2015 Kevin Cureton
"""
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import os
import string

import paste.httpheaders
import pyramid.config
import pyramid.renderers
import pyramid.security
import pyramid.view

import local
import local.stash

# ---------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# Authentication and Configuration
# ---------------------------------------------------------------------------------------------
class CustomAuthPolicy(object):
    """ A Pyramind authentcation policy class. The interface is as
        required by Pyramid.

        Pulled from http://pyramid-cookbook.readthedocs.org/en/latest/auth/basic.html
    """
    # ---------------------------------------------------------------
    # Pyramid auth policy methods
    # ---------------------------------------------------------------
    def authenticated_userid(self, request):
        print("DEBUG: In authenticated_userid...")
        user_uid = self._authenticateCredentials(request)
        return user_uid

#        credentials = self._getRequestCredentials(request)
#        if credentials is None:
#            return None
#        login_name = credentials['login']
#        if self._validateCredentials(credentials, request) is not None:
#            users_stash = local.stash.UsersStash()
#            authenticated = users_stash.authenticatedUser(login_name, password)
#            return login_name

    def effective_principals(self, request):
        print("DEBUG: In effective_principals...")

        effective_principals = [ pyramid.security.Everyone ]

        user_uid = self._authenticateCredentials(request)
        if user_uid:
            effective_principals.append(pyramid.security.Authenticated)
            effective_principals.append(user_uid)

        return effective_principals

    def unauthenticated_userid(self, request):
        print("DEBUG: In unauthenticated_userid...")
        credentials = self._getRequestCredentials(request)
        if credentials is not None:
            return credentials['login']
        else:
            return None

    def remember(self, request, principal, **kw):
        print("DEBUG: In remember...")
        return []

    def forget(self, request):
        print("DEBUG: In forget...")
        head = paste.httpheaders.WWW_AUTHENTICATE.tuples('Basic realm="%s"' % self.realm)
        return head

    # ---------------------------------------------------------------
    # Protected methods
    # ---------------------------------------------------------------
    def _authenticateCredentials(self, request):
        """ Authenticate the user credentials that are in the request.
        """
        credentials = self._getRequestCredentials(request)
        if credentials:
            users_stash = local.stash.UsersStash()
            user_uid = users_stash.authenticatedUser(credentials['login'], credentials['password'])
            return user_uid
        else:
            return None

    def _getRequestCredentials(self, request):
        """ Get the credentials pulled from the request.
        """
        authorization = paste.httpheaders.AUTHORIZATION(request.environ)
        try:
            auth_method, auth = authorization.split(' ', 1)
        except ValueError:
            # Not enough values to unpack.
            return None

        if auth_method.lower() == 'basic':
            try:
                auth = auth.strip().decode('base64')
            except binascii.Error:
                # Cannot decode.
                return None

            try:
                login, password = auth.split(':', 1)
            except ValueError:
                # Not enough values to unpack.
                return None

            return {'login': login, 'password': password}

        else:
            return None

#    def _validateCredentials(credentials, request):
#        """ Validate the user credentials against the Users stash.
#        """
#        login_name = credentials['login']
#        password = credentials['password']
#
#        users_stash = local.stash.UsersStash()
#        authenticated = users_stash.authenticatedUser(login_name, password)
#        if authenticated:
#            return [ 'api' ]
#        else:
#            return None



def getPyramidConfigurator(is_dev_server=False):
    """
    Get a pre-configurated Pyramid WSGI application.
    """
    # Configure and create the WSGI application.
    config = pyramid.config.Configurator(authentication_policy=CustomAuthPolicy())

    # Configuration settings.
    settings = dict()

    if is_dev_server:
        settings['pyramid.reload_templates'] = True

    config.add_settings(settings)

    # Include additional pyramid modules.
    config.include('pyramid_jinja2')

    # Scan the code for view declarations.
    config.scan(local)

    # Setup the views.
    config.add_route('index', '/')
    config.add_route('view.create_user', pattern='/users/create')
    config.add_route('view.search_users', pattern='/users/search')
    config.add_route('view.display_battles', pattern='/battles')

    # Setup the APIs.
    config.add_route('api.create_user', pattern='/api/users')
    config.add_route('api.modify_user', pattern='/api/users/{user_id}')
    config.add_route('api.create_battle_log', pattern='/api/battles')
    config.add_route('api.list_users', pattern='/api/list_users')

    # Add static views
    config.add_static_view("styles", "local:site/styles/")

    return config


# ---------------------------------------------------------------------------------------------
# Module test harness
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("This is the test harness for the module")
    sys.exit(0)
