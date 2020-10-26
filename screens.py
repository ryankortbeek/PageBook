import os
from time import sleep


def clear_screen():
    """
    Clears the current shell screen.
    """
    os.system('clear')


class BaseScreen:
    """
    Base class representing a screen. Child classes must implement the _setup and run methods described below.
    """

    def __init__(self):
        """
        Clears the screen upon initialization and runs the child class' _setup method.
        """
        clear_screen()
        self._setup()

    def _setup(self):
        """
        This should print out the screen title and options that the screen supports. Called in the constructor. Must be
        implemented by subclass.
        """
        return NotImplementedError

    def run(self):
        """
        This should run the functionality supported by the screen and return the next screen. Must be implemented by
        subclass.
        """
        return NotImplementedError


class StartScreen(BaseScreen):
    """
    Class representing the user type selection screen.
    """

    def __init__(self):
        BaseScreen.__init__(self)

    def _setup(self):
        """
        Prints out the screen title and the options supported by this screen.
        """
        start_msg = '''WELCOME TO___________________________________________________
                                                            /
       ____________________________________                /
      /  ___   /  ___   /  _______/  _____/               /
     /  /__/  /  /__/  /  / _____/  /__                  /
    /  ______/  ___   /  / /_   /  ___/                 /
   /  /     /  /  /  /  /___/  /  /____                /
  /__/     /__/__/__/_________/_______/____  ___      /
          /  __  / /  _____  /  ____   /  / /  /     /
         /  /_/ /_/  /   /  /  /   /  /  /_/  /_    /
        /  ___   /  /   /  /  /   /  /  ____   /   /
       /  /__/  /  /___/  /  /___/  /  /   /  /   /
      /________/_________/_________/__/   /__/   /
                                                /
_______________________________________________/

Please select the type of user that you are:
\t[1] registered user
\t[2] unregistered user'''
        print(start_msg)

    def run(self):
        """
        Gets the user's type and returns it.
        :return: an integer corresponding to the user's type
        """
        valid_inputs = ['1', '2']
        user_type = input('> ')
        while user_type not in valid_inputs:
            print('"{}" is an invalid selection, please enter a valid selection from the menu above.'
                  .format(user_type))
            user_type = input('> ')
        return user_type


class LoginScreen(BaseScreen):
    """
    Class representing the login screen.
    """

    def __init__(self, cursor):
        """
        Initializes an instance of this class.
        :param cursor: sqlite cursor
        """
        BaseScreen.__init__(self)
        self.cursor = cursor

    def _setup(self):
        """
        Prints out the screen title.
        """
        print('LOGIN')

    def _login_uid_exists(self, login_uid):
        """
        Checks if there is a user in the database with a user id that matches login_uid (match is case-insensitive).
        :param login_uid: id of user to login as
        :return: a boolean value representing whether or not there is a user in the database who has a user id equal
                 to login_uid (case-insensitive)
        """
        query = 'select * from users where lower(uid)=:login_uid;'
        self.cursor.execute(query, {'login_uid': login_uid.lower()})
        users = self.cursor.fetchall()
        return len(users) == 1

    def _pwd_is_correct(self, login_uid, login_pwd):
        """
        Checks if there is a user in the database with a user id and password matching login_uid (match is case-
        insensitive) and password (match is case-sensitive), respectively.
        :param login_uid: id of user to login as
        :param login_pwd: password of user to login as
        :return: a boolean value representing whether or not there is a user in the database who has a user id equal
                 to login_uid (case-insensitive) and a password equal to login_pwd (case-sensitive)
        """
        query = 'select * from users where lower(uid)=:login_uid and pwd=:login_pwd'
        self.cursor.execute(query, {'login_uid': login_uid.lower(), 'login_pwd': login_pwd})
        users = self.cursor.fetchall()
        return len(users) == 1

    def run(self):
        """
        Carries out the login process. On successful login a message is displayed for 0.5 sec before the program
        continues and the uid of the logged in user is returned.
        :return: the uid of the logged in user
        """
        print('\nPlease enter your user id (max 4 characters):')
        login_uid = input('> ')
        while (len(login_uid) > 4) or (not self._login_uid_exists(login_uid)):
            print('Invalid user id, try again:')
            login_uid = input('> ')
        print('\nPlease enter your password:')
        login_pwd = input('> ')
        while not self._pwd_is_correct(login_uid, login_pwd):
            print('Incorrect password, try again:')
            login_pwd = input('> ')
        print('\nLogin Successful')
        sleep(0.5)
        return login_uid


class SignUpScreen(BaseScreen):
    """
    Class representing the sign up screen.
    """

    def __init__(self, connection, cursor):
        BaseScreen.__init__(self)
        self.connection = connection
        self.cursor = cursor

    def _setup(self):
        """
        Prints out the screen title.
        """
        print('SIGN UP')

    def _uid_already_exists(self, new_uid):
        """
        Checks if there is a user in the database that already has new_uid (match is case-insensitive).
        :param new_uid: desired new user id
        :return: a boolean value representing whether or not there is already a user in the database who has a user id
                 equal to new_uid (case-insensitive)
        """
        query = 'select * from users where lower(uid)=:new_uid;'
        self.cursor.execute(query, {'new_uid': new_uid.lower()})
        users = self.cursor.fetchall()
        return len(users) == 1

    def run(self):
        """
        Carries out the sign up process. On successful sign up a message is displayed for 0.5 sec before the program
        continues, the user is logged in, and the uid of the new logged in user is returned.
        :return: the uid of the logged in user
        """
        print('\nPlease enter a user id that you would like to use (max 4 characters):')
        new_uid = input('> ')
        while (len(new_uid) > 4) or (self._uid_already_exists(new_uid)):
            print('The entered user id either has more than 4 characters or already exists, try again:')
            new_uid = input('> ')
        print('\nPlease enter your name:')
        name = input('> ')
        print('\nPlease enter the name of the city you live in:')
        city = input('> ')
        print('\nPlease enter the password you would like to use:')
        pwd = input('> ')
        insertion = 'insert into users values (:new_uid, :name, :pwd, :city, date());'
        self.cursor.execute(insertion, {'new_uid': new_uid, 'name': name, 'pwd': pwd, 'city': city})
        self.connection.commit()
        print('\nSign Up Successful - you will now be logged in')
        sleep(0.5)
        return new_uid
