import sqlite3
import string
import random


class DBManager:
    """
    Class handling the interaction between python and the sqlite database this program is running on.
    """

    def __init__(self, db_path):
        """
        Connects to the database at db_path.
        :param db_path: path to the database this program is to run on
        """
        assert db_path.endswith('.db'), 'invalid file type - please specify the path to a database'
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def _generate_id(self, length):
        """
        Generates a string of desired length consisting of random digits and ascii letters.
        :param length: number of characters in random string
        :return: string with length number of random characters
        """
        _id = ''
        random_chars = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
        _id = _id.join(random_chars)
        return _id

    def pid_exists(self, pid_to_check):
        """
        Checks if pid_to_check already exists as a pid for an existing post or question or answer (case insensitive).
        :param pid_to_check: pid to check whether it already exists
        :return: boolean value corresponding to whether or not pid_to_check already exists (True if already exists)
        """
        # TODO: verify this query
        query = 'select * from posts, questions, answers where lower(posts.pid)=:pid_to_check or lower(' \
                'questions.pid)=:pid_to_check or lower(answers.pid)=:pid_to_check; '
        self.cursor.execute(query, {'pid_to_check': pid_to_check.lower()})
        posts = self.cursor.fetchall()
        return len(posts) >= 1

    def uid_exists(self, uid_to_check):
        """
        Checks if there is a user in the database with a user id that matches login_uid (match is case-insensitive).
        :param uid_to_check: uid of user to login as
        :return: a boolean value representing whether or not there is a user in the database who has a user id equal
                 to login_uid (case-insensitive)
        """
        query = 'select * from users where lower(uid)=:uid_to_check;'
        self.cursor.execute(query, {'uid_to_check': uid_to_check.lower()})
        users = self.cursor.fetchall()
        return len(users) >= 1

    def valid_login(self, login_uid, login_pwd):
        """
        Checks if there is a user in the database with a user id and password matching login_uid (match is case-
        insensitive) and password (match is case-sensitive), respectively.
        :param login_uid: uid of user to login as
        :param login_pwd: password of user to login as
        :return: a boolean value representing whether or not there is a user in the database who has a user id equal
                 to login_uid (case-insensitive) and a password equal to login_pwd (case-sensitive)
        """
        query = 'select * from users where lower(uid)=:login_uid and pwd=:login_pwd'
        self.cursor.execute(query, {'login_uid': login_uid.lower(), 'login_pwd': login_pwd})
        users = self.cursor.fetchall()
        return len(users) >= 1

    def add_user(self, new_uid, name, pwd, city):
        """
        Adds a new user to the users table. Assumes that new_uid is not already in the users table.
        :param new_uid: uid of new user
        :param name: name of new user
        :param pwd: password of new user
        :param city: city of new user
        """
        insertion = 'insert into users values (:new_uid, :name, :pwd, :city, date(\'now\', \'localtime\'));'
        self.cursor.execute(insertion, {'new_uid': new_uid, 'name': name, 'pwd': pwd, 'city': city})
        self.connection.commit()

    def post_new_question(self, new_question_title, new_question_body, poster):
        """
        Creates a new post in the posts table and a question in the questions table with the same unique pid. First
        generates a unique pid (one that is not currently used by any question, answer, or post) and then inserts the
        new question in the posts table with pid, the current date, new_question_title, new_question_body, and the
        poster and and the question table with pid.
        :param new_question_title:
        :param new_question_body:
        :param poster:
        :return:
        """
        unique = False
        new_pid = ''
        while not unique:
            new_pid = self._generate_id(4)
            unique = not self.pid_exists(new_pid)
        insertion = 'insert into posts values (:new_pid, date(\'now\', \'localtime\'), :title, :body, :poster);'
        self.cursor.execute(
            insertion, {'new_pid': new_pid, 'title': new_question_title, 'body': new_question_body, 'poster': poster}
        )
        insertion = 'insert into questions (pid) values (:new_pid);'
        self.cursor.execute(insertion, {'new_pid': new_pid})
        self.connection.commit()

    def close_connection(self):
        """
        Closes the connection with the database.
        """
        self.connection.close()
