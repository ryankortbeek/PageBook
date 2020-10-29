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

    def __init__(self, current_uid=None, db_manager=None):
        """
        Clears the screen upon initialization and runs the child class' _setup method.
        :param current_uid: the uid of the user that is currently logged in (optional parameter)
        :param db_manager: sqlite database manager (optional parameter)
        """
        self.current_user = None if current_uid is None else current_uid
        self.db_manager = None if db_manager is None else db_manager
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
              '\t[2] unregistered user\n')

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
        BaseScreen.__init__(self, db_manager=db_manager)

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
        BaseScreen.__init__(self, db_manager=db_manager)

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
        Initializes an instance of this class.
        :param current_uid: the uid of the user that is currently logged in
        """
        BaseScreen.__init__(self, current_uid=current_uid)

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


class PostQuestionScreen(BaseScreen):
    """
    Class representing the post question screen.
    """

    def __init__(self, current_uid, db_manager):
        """
        Initializes an instance of this class.
        :param current_uid: the uid of the user that is currently logged in (optional parameter)
        :param db_manager: sqlite database manager (optional parameter)
        """
        BaseScreen.__init__(self, current_uid=current_uid, db_manager=db_manager)
        self.question_title = None
        self.question_body = None

    def _setup(self):
        print('POST QUESTION')

    def _get_new_question_data(self):
        """
        Prompts the user to enter the title and body texts of the question they want to add and sets the
        question_title and question_body class attributes accordingly.
        """
        print('\nPlease enter the title of your question:')
        self.question_title = input('> ')
        print('\nPlease enter the body of your question:')
        self.question_body = input('> ')

    def run(self):
        """
        Gets the title and body texts of the question that the user wants to add and then confirms with the user that
        they want to post the question that they entered - allowing them to either confirm and post their question,
        re-enter the question title and body, or return to the main menu and not post the question.
        """
        valid_inputs = ['Y', 'y', 'E', 'e', 'N', 'n']
        confirm = False
        while not confirm:
            self._get_new_question_data()
            print('\nQuestion Summary\nTitle: {}\nBody: {}\n'.format(self.question_title, self.question_body))
            print('Please select one of the following actions:\n'
                  '\t[Y/y] To confirm and post the question above\n'
                  '\t[E/e] To re-enter the question title and body\n'
                  '\t[N/n] To return to the main menu\n')
            selection = select_from_menu(valid_inputs)
            if selection.lower() == 'y':
                self.db_manager.post_new_question(self.question_title, self.question_body, self.current_user)
                print('\nQuestion Posted Successfully - you will now be returned to the main menu')
                sleep(0.5)
                break
            elif selection.lower() == 'n':
                break
