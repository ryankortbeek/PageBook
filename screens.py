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
        print('SELECT USER TYPE')
        print('Please enter the number corresponding to the type of user that you are:')
        print('\t[1] Registered User\n\t[2] Unregistered User\n')

    def run(self):
        """
        Gets the user's type and returns it.
        :return: an integer corresponding to the user's type
        """
        valid_inputs = ['1', '2']
        user_type = input()
        while user_type not in valid_inputs:
            user_type = input('"{}" is an invalid selection, please enter a valid selection from the menu above.\n'.
                              format(user_type))
        return user_type


class LoginScreen(BaseScreen):
    """
    Class representing the login screen.
    """

    def __init__(self, db_manager):
        """
        Initializes an instance of this class.
        :param db_manager: sqlite database manager
        """
        BaseScreen.__init__(self)
        self.db_manager = db_manager

    def _setup(self):
        """
        Prints out the screen title.
        """
        print('LOGIN')

    def run(self):
        """
        Carries out the login process. On successful login a message is displayed for 0.5 sec before the program
        continues and the uid of the logged in user is returned.
        :return: the uid of the logged in user
        """
        login_uid = input('Please enter your user id (max 4 characters):\n')
        while (len(login_uid) > 4) or (not self.db_manager.uid_exists(login_uid)):
            login_uid = input('Invalid user id, try again:\n')
        login_pwd = input('Please enter your password:\n')
        while not self.db_manager.valid_login(login_uid, login_pwd):
            login_pwd = input('Incorrect password, try again:\n')
        print('Login Successful')
        sleep(0.5)
        return login_uid


class SignUpScreen(BaseScreen):
    """
    Class representing the sign up screen.
    """

    def __init__(self, db_manager):
        """
        Initializes an instance of this class.
        :param db_manager: sqlite database manager
        """
        BaseScreen.__init__(self)
        self.db_manager = db_manager

    def _setup(self):
        """
        Prints out the screen title.
        """
        print('SIGN UP')

    def run(self):
        """
        Carries out the sign up process. On successful sign up a message is displayed for 0.5 sec before the program
        continues, the user is logged in, and the uid of the new logged in user is returned.
        :return: the uid of the logged in user
        """
        new_uid = input('Please enter a user id that you would like to use (max 4 characters):\n')
        while (len(new_uid) > 4) or (self.db_manager.uid_exists(new_uid)):
            new_uid = input('The entered user id either has more than 4 characters or already exists, try again:\n')
        name = input('Please enter your name:\n')
        city = input('Please enter the name of the city you live in:\n')
        pwd = input('Please enter the password you would like to use:\n')
        self.db_manager.add_user(new_uid, name, pwd, city)
        print('Sign Up Successful - you will now be logged in')
        sleep(0.5)
        return new_uid
