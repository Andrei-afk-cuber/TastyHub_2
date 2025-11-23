class User(object):
    def __init__(self, username, password, admin=False, authorized=False, id=0):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__admin = admin
        self.__authorized = authorized

    def getId(self):
        return self.__id

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def isAdmin(self):
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

