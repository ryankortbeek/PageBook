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
        Gets a connection to the database at db_path and runs the program.
        :param db_path: command line argument specifying the path to the database this program is to run on
        """
        self.connection = None
        self.cursor = None
        self.db_manager = DBManager(db_path)
        self._run()

    def _run(self):
        """
        Runs the program.
        """
        user_select_screen = StartScreen()
        user_type = user_select_screen.run()
        login_screen = LoginScreen(self.db_manager) if user_type == '1' else SignUpScreen(self.db_manager)
        logged_in_uid = login_screen.run()
        # TODO: implement the main menu
        self.connection.close()


def main():
    assert (len(sys.argv) == 2), 'please enter the correct number of arguments - this program should be run using ' \
                                 '"python3 prj.py PATH_TO_DATABASE"'
    assert path.exists(sys.argv[1]), 'path does not exist - please specify a valid path'
    p = PostBook(sys.argv[1])


if __name__ == '__main__':
    main()
