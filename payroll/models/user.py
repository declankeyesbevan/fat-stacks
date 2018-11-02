class User:

    _MAX_ATTEMPTS = 3

    def __init__(self, username, password, is_locked, failed_attempts):
        self._username = username
        self._password = password
        self._is_locked = is_locked
        self._failed_attempts = failed_attempts

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def is_locked(self):
        return self._is_locked

    @property
    def failed_attempts(self):
        return self._failed_attempts

    def update_attempts(self, number):
        self._failed_attempts += number
        if self._failed_attempts == self._MAX_ATTEMPTS:
            self._is_locked = True
