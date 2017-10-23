class Signup:
    def __init__(self, **kwargs):
        self._name = kwargs.get('name', None)
        self._surname = kwargs.get('surname', None)
        self._patronymic = kwargs.get('patronymic', None)
        self._username = kwargs.get('username', None)
        self._password = kwargs.get('password', None)
        self._confirm_password = kwargs.get('confirm_password', None)

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def patronymic(self):
        return self._patronymic

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def confirm_password(self):
        return self._confirm_password
