import sys
from os import path

from screens import *
from db_manager import *


class PostBook:
    """
    Runs the program.
    """

    def __init__(self, db_path):
        """
        Gets a connection to the database at db_path and initializes so this program can be run.
        :param db_path: command line argument specifying the path to the database this program is to run on
        """
        self.current_user = None
        self.running = True
        self.db_manager = DBManager(db_path)

    def _run_login(self):
        """
        Runs the login process - user is first taken to the start screen where they are prompted to select the type
        of user that they are (i.e. registered or unregistered), and then are taken to either the LOGIN or SIGN UP
        screen. Upon successfully signing up (this also logs the user in) or logging in this function returns the uid
        of the logged in user.
        :return: the uid of the logged in user as a string
        """
        start_screen = StartScreen()
        user_type = start_screen.run()
        login_screen = LoginScreen(self.db_manager) if user_type == 'registered' else SignUpScreen(self.db_manager)
        return login_screen.run()

    def run(self):
        """
        Runs the program.
        """
        self.current_user = self._run_login()
        while self.running:
            if self.current_user is None:
                self.current_user = self._run_login()
            mm_screen = MainMenuScreen(self.current_user)
            task = mm_screen.run()
            if task == 'post question':
                post_question_screen = PostQuestionScreen(self.current_user, self.db_manager)
                post_question_screen.run()
            elif task == 'search':
                # TODO implement search functionality
                pass
            elif task == 'logout':
                self.current_user = None
            # Happens when task == 'exit'
            else:
                self.running = False
        self.db_manager.close_connection()
        clear_screen()


def main():
    assert (len(sys.argv) == 2), 'please enter the correct number of arguments - this program should be run using ' \
                                 '"python3 prj.py PATH_TO_DATABASE"'
    assert path.exists(sys.argv[1]), 'path does not exist - please specify a valid path'
    p = PostBook(sys.argv[1])
    p.run()


if __name__ == '__main__':
    main()
