from assemblyline_client.v4_client.common.utils import (
    api_path,
    api_path_by_module,
    get_function_kwargs,
)


class Avatar(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, username):
        """\
Loads the user's avatar.

Required:
username    : User key (string)

Throws a Client exception if the user does not exist.
"""
        return self._connection.get(api_path('user', 'avatar', username))

    def update(self, username, avatar):
        """\
Update the user's avatar.

Required:
username    : User key (string)
avatar      : New avatar for the user

Throws a Client exception if the user does not exist.
"""
        return self._connection.post(api_path('user', 'avatar', username), data=avatar)


class Favorites(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, username):
        """\
Loads the user's favorites.

Required:
username    : User key (string)

Throws a Client exception if the user does not exist.
"""
        return self._connection.get(api_path('user', 'favorites', username))

    def add(self, username, fav_type, fav_data):
        """\
Add a favorite to the user's favorites.

Required:
username    : User key (string)
fav_type    : Type of favorite to remove (string)
fav_data    : Data block of the favority to add (dict)

Throws a Client exception if the user does not exist.
"""
        return self._connection.put(api_path('user', 'favorites', username, fav_type), json=fav_data)

    def delete(self, username, fav_type, name):
        """\
Remove a favorite from the user's favorites.

Required:
username    : User key (string)
fav_type    : Type of favorite to remove (string)
name        : Name of favorite to remove (string)

Throws a Client exception if the user does not exist.
"""
        return self._connection.delete(api_path('user', 'favorites', username, fav_type), json=name)

    def update(self, username, favorites):
        """\
Update the user's favorite queries.

Required:
username    : User key (string)
favorites   : New favorites for the user

Throws a Client exception if the user does not exist.
"""
        return self._connection.post(api_path('user', 'favorites', username), json=favorites)


class Quotas(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, username):
        """\
Get the current user's settings.

Required:
username    : User key (string)
"""
        return self._connection.get(api_path('user', 'quotas', username))


class Settings(object):
    def __init__(self, connection):
        self._connection = connection

    def __call__(self, username):
        """\
Get the current user's settings.

Required:
username    : User key (string)
"""
        return self._connection.get(api_path('user', 'settings', username))

    def update(self, username, settings):
        """\
Update the user's settings.

Required:
username    : User key (string)
settings    : New settings for the user

Throws a Client exception if the user does not exist.
"""
        return self._connection.post(api_path('user', 'settings', username), json=settings)


class User(object):
    def __init__(self, connection):
        self._connection = connection
        self.avatar = Avatar(connection)
        self.favorites = Favorites(connection)
        self.quotas = Quotas(connection)
        self.settings = Settings(connection)

    def __call__(self, username):
        """\
Return the profile for the given username.

Required:
username: User key. (string).

Throws a Client exception if the user does not exist.
"""
        return self._connection.get(api_path('user', username))

    def add(self, username, user_data):
        """\
Add a user to the system

Required:
username    : Name of the user to add to the system
user_data   : Profile data of the user to add
"""
        return self._connection.put(api_path('user', username), json=user_data)

    def delete(self, username):
        """\
Remove the account specified by the username.

Required:
username    : Name of the user to remove from the system
"""
        return self._connection.delete(api_path('user', username))

    def list(self, query="*:*", rows=10, offset=0, sort="uname asc"):
        """\
List users of the system (per page)

Required:
offset     : Offset in the user index
query      : Filter to apply to the user list
rows       : Max number of user returned
sort       : Sort order
"""
        return self._connection.get(api_path_by_module(self, **get_function_kwargs('self')))

    def submission_params(self, username, profile="default"):
        """\
Return the submission parameters for the given username.

Required:
username    : User key (string)

Optional:
profile     : Name of the submission profile to use (string)

Throws a Client exception if the user does not exist.
"""
        return self._connection.get(api_path_by_module(self, username, profile))

    def tos(self, username):
        """\
Specified user send agreement to Terms of Service

Required:
username    : Username of the user that agrees with terms of service (string)

Throws a Client exception if the user does not exist.
"""
        return self._connection.get(api_path_by_module(self, username))

    def update(self, username, user_data):
        """\
Update a user profile in the system.

Required:
username    : Name of the user to update in the system
user_data   : Profile data of the user to update
"""
        return self._connection.post(api_path('user', username), json=user_data)

    def whoami(self):
        """\
Return the currently logged in user as well as the system configuration.
"""
        return self._connection.get(api_path_by_module(self))
