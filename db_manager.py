import sqlite3


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

    def uid_exists(self, uid_to_check):
        """
        Checks if there is a user in the database with a user id that matches login_uid (match is case-insensitive).
        :param uid_to_check: uid of user to login as
        :return: a boolean value representing whether or not there is a user in the database who has a user id equal
                 to login_uid (case-insensitive)
        """
        query = 'select * from users where lower(uid)=:login_uid;'
        self.cursor.execute(query, {'login_uid': uid_to_check.lower()})
        users = self.cursor.fetchall()
        return len(users) == 1

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
        return len(users) == 1

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

    def close_connection(self):
        """
        Closes the connection with the database.
        """
        self.connection.close()
