import os
from time import sleep


def clear_screen():
    """
    Clears the current shell screen.
    """
    os.system('clear')


def select_from_menu(valid_inputs):
    """
    This allows a user to enter an input from a selection of values denoted by valid_inputs. It is assumed that the
    "menu" is already printed as this function just grabs the users input and checks if it is in the passed list
    valid_inputs (therefore being valid). If the input is invalid the user is prompted to make another selection
    until a valid input is entered.
    :param valid_inputs: list including all the inputs that should be considered valid
    :return: a string corresponding to the users valid selection
    """
    selection = input('> ')
    while selection not in valid_inputs:
        print('"{}" is an invalid selection, please enter a valid selection from the menu above.'
              .format(selection))
        selection = input('> ')
    return selection


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
        print('WELCOME TO___________________________________________________\n'
              '                                                            /\n'
              '       ____________________________________                /\n'
              '      /  ___   /  ___   /  _______/  _____/               /\n'
              '     /  /__/  /  /__/  /  / _____/  /__                  /\n'
              '    /  ______/  ___   /  / /_   /  ___/                 /\n'
              '   /  /     /  /  /  /  /___/  /  /____                /\n'
              '  /__/     /__/__/__/_________/_______/____  ___      /\n'
              '          /  __  / /  _____  /  ____   /  / /  /     /\n'
              '         /  /_/ /_/  /   /  /  /   /  /  /_/  /_    /\n'
              '        /  ___   /  /   /  /  /   /  /  ____   /   /\n'
              '       /  /__/  /  /___/  /  /___/  /  /   /  /   /\n'
              '      /________/_________/_________/__/   /__/   /\n'
              '                                                /\n'
              '_______________________________________________/\n'
              '\n'
              'Please select the type of user that you are:\n'
              '\t[1] registered user\n'
              '\t[2] unregistered user')

    def run(self):
        """
        Gets the user's type and returns it.
        :return: a string corresponding to the type of user that the current user is
        """
        types = {'1': 'registered', '2': 'unregistered'}
        valid_inputs = ['1', '2']
        return types[select_from_menu(valid_inputs)]


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
        print('\nPlease enter your user id (max 4 characters):')
        login_uid = input('> ')
        while (len(login_uid) > 4) or (not self.db_manager.uid_exists(login_uid)):
            print('Invalid user id, try again:')
            login_uid = input('> ')
        print('\nPlease enter your password:')
        login_pwd = input('> ')
        while not self.db_manager.valid_login(login_uid, login_pwd):
            print('Incorrect password, try again:')
            login_pwd = input('> ')
        print('\nLogin Successful')
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
        print('\nPlease enter a user id that you would like to use (max 4 characters):')
        new_uid = input('> ')
        while (len(new_uid) > 4) or (self.db_manager.uid_exists(new_uid)):
            print('The entered user id either has more than 4 characters or already exists, try again:')
            new_uid = input('> ')
        print('\nPlease enter your name:')
        name = input('> ')
        print('\nPlease enter the name of the city you live in:')
        city = input('> ')
        print('\nPlease enter the password you would like to use:')
        pwd = input('> ')
        # TODO look into timezone with date()
        self.db_manager.add_user(new_uid, name, pwd, city)
        print('\nSign Up Successful - you will now be logged in')
        sleep(0.5)
        return new_uid


class MainMenuScreen(BaseScreen):
    """
    Class representing the login screen.
    """

    def __init__(self, current_uid):
        """
        Initializes an instance of this class and sets the uid of the user that is currently logged in as a class
        attribute.
        :param current_uid: the uid of the user that is currently logged in
        """
        self.current_user = current_uid
        BaseScreen.__init__(self)

    def _setup(self):
        """
        Prints out the screen title and the options supported by this screen.
        """
        print('MAIN MENU\n'
              '\n'
              'Welcome {}!\n'
              '\n'
              'Please select the task that you would like to perform:\n'
              '\t[1] Post a question\n'
              '\t[2] Search for posts\n'
              '\t[3] Logout\n'
              '\t[4] Exit\n'.format(self.current_user))

    def run(self):
        """
        Gets the task that the user would like to perform and returns it.
        :return: a string representing the task the user would like to perform
        """
        tasks = {'1': 'post question', '2': 'search', '3': 'logout', '4': 'exit'}
        valid_inputs = ['1', '2', '3', '4']
        return tasks[select_from_menu(valid_inputs)]
