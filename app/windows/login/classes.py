# class User
class User:
    def __init__(self, username: str, password: str, admin: bool=False, authorized: bool=False, id: int=0) -> None:
        self.__id = id
        self.__username = username
        self.__password = password
        self.__admin = admin
        self.__authorized = authorized

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    def admin(self):
        return self.__admin

    def isAuthorized(self):
        return self.__authorized

    def setUsername(self, login):
        self.__username = login

    def setPassword(self, password):
        self.__password = password

    def setAdmin(self, admin):
        self.__admin = admin

    def activateAccount(self):
        self.__authorized = True

    def deactivateAccount(self):
        self.__authorized = False

