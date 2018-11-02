from collections import namedtuple

from payroll.controllers.data import Data
from payroll.models.user import User


class Authenticate:

    _MESSAGES = {
        'locked': 'User is locked',
        'granted': 'Access Granted',
        'incorrect': 'Username/password combination not correct',
        'exit_application': "Or Exit (X) application?",
        'exit_menu': "Or Exit (X) menu?",
        'valid': "Error: please enter valid choice\n",
    }
    _SELECTIONS = {
        't': True,
        'x': None,
    }

    def __init__(self, tui):
        self._tui = tui
        self._users = Data().load_data('authentication.txt')
        self._loaded_user = None

    def authenticate_user(self):
        authenticated = False
        while not authenticated:
            authenticated = self._cycle()
            if authenticated is None:
                return False
            elif authenticated:
                return True

    def _cycle(self):
        auth = self._auth_cycle()
        while not auth:
            self._tui.print_message("Try again (T) or exit (X)?\n")
            try_again = self._tui.get_input("Enter 'T' or 'X'\n")
            try:
                proceed = self._SELECTIONS[try_again.lower()]
            except KeyError:
                self._tui.print_message(self._MESSAGES.get('valid'))
                auth = self._auth_cycle()
            else:
                if proceed is None:
                    return
                auth = self._auth_cycle()
        else:
            return True

    def _auth_cycle(self):
        username = self._tui.user_name()
        password = self._tui.password()
        response = self._challenge_response(username, password)
        self._tui.print_message(response.message)
        return response.granted

    def _challenge_response(self, username, password):
        Access = namedtuple('Access', 'granted message')

        matched_user = self._match_user(username)
        if matched_user:
            self._create_user(self._users.iloc[matched_user[0]])
            if self._loaded_user.is_locked:
                return Access(False, self._MESSAGES.get('locked'))
            if password == self._loaded_user.password:
                return Access(True, self._MESSAGES.get('granted'))
            else:
                self._loaded_user.update_attempts(1)
                self._flush_user_to_users()
                return Access(False, self._MESSAGES.get('incorrect'))
        return Access(False, self._MESSAGES.get('incorrect'))

    def _create_user(self, matched_user):
        self._loaded_user = User(
            matched_user.username, matched_user.password,
            self._cast_lock_to_bool(matched_user.is_locked), matched_user.failed_attempts
        )

    def _match_user(self, username):
        username_matching_column = self._users.username.str.match(fr'^{username}$', case=True)
        return self._users.username.index[username_matching_column].tolist()

    def _flush_user_to_users(self):
        matched_user = self._match_user(self._loaded_user.username)
        database_user = self._users.iloc[matched_user[0]]
        memory_user = self._loaded_user
        database_user.failed_attempts = memory_user.failed_attempts
        database_user.is_locked = self._cast_lock_to_string(memory_user.is_locked)
        self._users.iloc[matched_user[0]] = database_user
        self._flush_to_disk(database_user)

    @classmethod
    def _flush_to_disk(cls, database_user):
        Data().dump_data('authentication.txt', database_user)

    @classmethod
    def _cast_lock_to_bool(cls, locked):
        return True if locked == 'Y' else False

    @classmethod
    def _cast_lock_to_string(cls, locked):
        return 'Y' if locked else 'N'
