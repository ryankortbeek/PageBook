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

    def _post_is_question(self, pid):
        """
        Checks if the pid passed to this method as a parameter is a question.
        :param pid: pid of to check if in questions table
        :return: boolean value corresponding to whether pid is in the questions tables or not
        """
        post_is_question_query = 'select * from questions where pid=:pid;'
        self.cursor.execute(post_is_question_query, {'pid': pid})
        return len(self.cursor.fetchall()) == 1

    def _post_is_answer(self, pid):
        """
        Checks if the pid passed to this method as a parameter is an answer.
        :param pid: pid of to check if in answers table
        :return: boolean value corresponding to whether pid is in the answers tables or not
        """
        post_is_answer_query = 'select * from answers where pid=:pid;'
        self.cursor.execute(post_is_answer_query, {'pid': pid})
        return len(self.cursor.fetchall()) == 1

    def _get_question_info(self, pid):
        """
        Gets all the columns of the posts table as well as the number of votes and answers that the question identified
        by pid has.
        :param pid: pid to get pid, pdate, title, body, poster, num_answers, and num_votes for
        :return: tuple corresponding to the pid, pdate, title, body, poster, num_answers, and num_votes of the question
                 identified by pid
        """
        num_votes_query = 'select p.pid, ifnull(count(v.pid), 0) as num_votes ' \
                          'from posts p, votes v ' \
                          'where p.pid=:pid and v.pid=p.pid group by (p.pid)'
        num_ans_query = 'select p.pid, ifnull(count(a.pid), 0) as num_answers ' \
                        'from posts p, answers a ' \
                        'where p.pid=:pid and a.qid=p.pid group by (p.pid)'
        num_votes_and_questions_a = 'select pid, num_votes, num_answers ' \
                                    'from (' + num_votes_query + ') left outer join (' + num_ans_query + ') using (pid)'
        num_votes_and_questions_b = 'select pid, num_votes, num_answers ' \
                                    'from (' + num_ans_query + ') left outer join (' + num_votes_query + ') using (pid)'
        # Need to do a full join in order to cover all the possible cases
        num_votes_and_questions = num_votes_and_questions_a + ' union ' + num_votes_and_questions_b
        question_info_query = 'select p.pid, p.pdate, p.title, p.body, p.poster from posts p where p.pid=:pid'
        query = 'select pid, pdate, title, body, poster, ifnull(num_answers, 0), ifnull(num_votes, 0) ' \
                'from (' + question_info_query + ') left outer join (' + num_votes_and_questions + ') using (pid);'
        self.cursor.execute(query, {'pid': pid})
        return self.cursor.fetchone()

    def _get_answer_info(self, pid):
        """
        Gets all the columns of the posts table as well as the number of votes that the answer identified by pid has.
        :param pid: pid to get pid, pdate, title, body, poster, and num_votes for
        :return: tuple corresponding to the pid, pdate, title, body, poster, and num_votes of the answer with
                 identified by pid
        """
        num_votes_query = 'select p.pid, ifnull(count(v.pid), 0) as num_votes ' \
                          'from posts p, votes v ' \
                          'where p.pid=:pid and v.pid=p.pid group by (p.pid)'
        answer_info_query = 'select p.pid, p.pdate, p.title, p.body, p.poster from posts p where p.pid=:pid'
        query = 'select pid, pdate, title, body, poster, ifnull(num_votes, 0) ' \
                'from (' + answer_info_query + ') left outer join (' + num_votes_query + ') using (pid);'
        self.cursor.execute(query, {'pid': pid})
        return self.cursor.fetchone()

    def pid_exists(self, pid_to_check):
        """
        Checks if pid_to_check already exists as a pid for an existing post or question or answer (case insensitive).
        :param pid_to_check: pid to check whether it already exists
        :return: boolean value corresponding to whether or not pid_to_check already exists (True if already exists)
        """
        query = 'select * from posts where lower(posts.pid)=:pid_to_check;'
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
        query = 'select * from users where lower(uid)=:login_uid and pwd=:login_pwd;'
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

    def new_post(self, new_title, new_body, poster, is_an_answer=False, associated_question=None):
        """
        Creates a new post in the posts table that is either a question or an answer (and adds it to the respective
        table between questions or answers). If new post is an answer is_an_answer should be specified as being True and
        associated_question should be specified as the pid corresponding to the question that this answer is to be
        linked to. If new post is a question is_an_answer and associated_question can be ignored.
        :param new_title: title of new post
        :param new_body: body of new post
        :param poster: uid of user that is currently logged in and creating the post
        :param is_an_answer: should be True if the post that is to be created is an answer (default False)
        :param associated_question: if the post that is to be created is an answer this should be specified as the pid
                                    corresponding to the question that this answer is to be linked to
        """
        unique = False
        new_pid = ''
        while not unique:
            new_pid = self._generate_id(4)
            unique = not self.pid_exists(new_pid)
        insertion = 'insert into posts values (:new_pid, date(\'now\', \'localtime\'), :title, :body, :poster);'
        self.cursor.execute(
            insertion, {'new_pid': new_pid, 'title': new_title, 'body': new_body, 'poster': poster}
        )
        if not is_an_answer:
            insertion = 'insert into questions (pid) values (:new_pid);'
            self.cursor.execute(insertion, {'new_pid': new_pid})
        else:
            insertion = 'insert into answers values (:new_pid, :qid);'
            self.cursor.execute(insertion, {'new_pid': new_pid, 'qid': associated_question})
        self.connection.commit()

    def execute_search(self, keywords_to_search):
        """
        Searches the database
        :param keywords_to_search:
        :return:
        """
        search_results = {}
        search = 'select p.pid ' \
                 'from posts p ' \
                 'where lower(p.title) like :keyword or lower(p.body) like :keyword or exists(' \
                 'select pid from tags t where t.pid=p.pid and lower(t.tag) like :keyword);'
        for keyword in keywords_to_search:
            self.cursor.execute(search, {'keyword': '%' + keyword.lower() + '%'})
            posts = self.cursor.fetchall()
            for i in range(len(posts)):
                post = posts[i][0]
                if post in search_results:
                    search_results[post] += 1
                else:
                    search_results[post] = 1
        return sorted(search_results.items(), key=lambda x: x[1], reverse=True)

    def get_printable_post_info(self, sorted_pids):
        """
        Gets the pid, pdate, title, body, poster, num_answers (only in the case that the post of relevance is a
        question), and num_votes for each post identified by the pids in sorted_pids. Returns a list of these tuples.
        :param sorted_pids: List of pids that correspond to posts in the posts table - in the typical use case they are
                            the pids of posts that matched at least one of the searched keywords, sorted in order from
                            pids corresponding to posts that matched the largest number of keywords first
        :return: List of the tuples corresponding to the info retreived from the database by either
                 _get_question_info(..) or _get_answer_info(..)
        """
        printable_post_info = []
        for i in range(len(sorted_pids)):
            post_pid = sorted_pids[i][0]
            if self._post_is_question(post_pid):
                printable_post_info.append(self._get_question_info(post_pid))
            elif self._post_is_answer(post_pid):
                printable_post_info.append(self._get_answer_info(post_pid))
        return printable_post_info

    def get_vote_eligibility(self, uid, pid):
        """
        Checks if a user has already voted on a post or not.
        :param uid: uid of user to check whether they have already voted on the post identified by pid
        :param pid: pid of post to check
        :return: boolean value corresponding to whether the user identified by uid has already voted on post pid (True
                 if they have, False otherwise)
        """
        query = 'select * from votes where pid=:pid and uid=:uid;'
        self.cursor.execute(query, {'pid': pid, 'uid': uid})
        return len(self.cursor.fetchall()) == 0

    def check_privilege(self, uid):
        """
        Checks if the user identified by uid is a privileged user.
        :param uid: uid of user to check if privileged
        :return: boolean value corresponding to whether the user identified by uid is a privileged user (True if so)
        """
        query = 'select * from privileged where uid=:uid;'
        self.cursor.execute(query, {'uid': uid})
        return len(self.cursor.fetchall()) >= 1

    def add_vote(self, pid, current_user):
        """
        Adds a vote from the user identified by current_user to the post identified by pid.
        :param pid: pid of post to add a vote to
        :param current_user: uid of user who is adding a vote
        """
        # Generates a vno by adding 1 to the current max vno associated with the post
        query = 'select ifnull(max(vno), 0) from votes where pid=:pid;'
        self.cursor.execute(query, {'pid': pid})
        highest_current_vno = self.cursor.fetchone()[0]
        new_vno = highest_current_vno + 1
        insertion = 'insert into votes values (:pid, :vno, date(\'now\', \'localtime\'), :current_user);'
        self.cursor.execute(insertion, {'pid': pid, 'vno': new_vno, 'current_user': current_user})
        self.connection.commit()

    def check_for_accepted_answer(self, pid):
        """
        Checks if the question linked to the answer identified by pid has an accepted answer.
        :param pid: pid of answer to check the linked question of to see if it has an accepted answer or not
        :return: boolean value corresponding to whether the question linked to the answer identified by pid has
                 an accepted answer (True if so, False otherwise)
        """
        query = 'select q.theaid from questions q where q.pid=(select a.qid from answers a where a.pid=:pid);'
        self.cursor.execute(query, {'pid': pid})
        return False if self.cursor.fetchone()[0] is None else True

    def update_accepted_answer(self, pid_of_new_answer):
        """
        Updates the accepted answer the a question linked to the answer identified by pid_of_new_answer to the answer
        identified by pid_of_new_answer.
        :param pid_of_new_answer: pid of answer to set as the accepted answer to the question it is linked to
        """
        query = 'select qid from answers where pid=:pid_of_new_answer;'
        qid = self.cursor.execute(query, {'pid_of_new_answer': pid_of_new_answer}).fetchone()[0]
        update = 'update questions set theaid=:pid_of_new_answer where pid=:qid;'
        self.cursor.execute(update, {'pid_of_new_answer': pid_of_new_answer, 'qid': qid})
        self.connection.commit()

    def check_badge_eligibility(self, poster):
        """
        Returns True/False depending on whether the user identified by poster has already received a badge on the
        current date (if the user already has received a badge they are ineligible to receive another until tomorrow).
        :param poster: uid of user to give badge to
        :return: boolean value corresponding to whether the user identified by poster has already received a
                 badge on the current date (False if so, True otherwise)
        """
        query = 'select * from ubadges where uid=:poster and bdate=date(\'now\', \'localtime\');'
        self.cursor.execute(query, {'poster': poster})
        return len(self.cursor.fetchall()) == 0

    def give_badge(self, name, uid):
        """
        Creates a badge with name and adds it to the badges table if a badge with that name does not already exist. Then
        gives the user identified by uid the badge.
        :param name: name of badge to give
        :param uid: uid of user to give badge to
        """
        query = 'select * from badges where bname=:name;'
        self.cursor.execute(query, {'name': name})
        if self.cursor.fetchall() == 0:
            insertion = 'insert into badges (bname) values (:name);'
            self.cursor.execute(insertion, {'name': name})
            self.connection.commit()
        insertion = 'insert into ubadges values (:uid, date(\'now\', \'localtime\'), :name);'
        self.cursor.execute(insertion, {'uid': uid, 'name': name})
        self.connection.commit()

    def add_tag_to_post(self, pid, tag_name):
        """
        Adds a tag with name tag_name to the post identified by pid.
        :param pid: pid of post to add the tag to
        :param tag_name: name of the new tag
        :return: boolean value corresponding to the success of the operation - if there is already a tag with the same
                 name that has been given to the post identified by pid this function returns False, otherwise it
                 returns True after successfully adding the tag
        """
        query = 'select * from tags where pid=:pid and tag=:tag_name;'
        self.cursor.execute(query, {'pid': pid, 'tag_name': tag_name})
        if len(self.cursor.fetchall()) >= 1:
            return False
        insertion = 'insert into tags values (:pid, :tag_name);'
        self.cursor.execute(insertion, {'pid': pid, 'tag_name': tag_name})
        self.connection.commit()
        return True

    def update_post(self, pid, new_title=None, new_body=None):
        """
        Updates the title and/or body of a post identified by pid.
        :param pid: pid of post to update the title and/or body fields of
        :param new_title: new title of post (if no value is passed the title field of the post will not be updated)
        :param new_body: new body of post (if no value is passed the body field of the post will not be updated)
        """
        if (new_title is not None) and (new_body is not None):
            update = 'update posts set title=:new_title, body=:new_body where pid=:pid;'
            self.cursor.execute(update, {'new_title': new_title, 'new_body': new_body, 'pid': pid})
        elif new_body is not None:
            update = 'update posts set body=:new_body where pid=:pid;'
            self.cursor.execute(update, {'new_body': new_body, 'pid': pid})
        else:
            update = 'update posts set title=:new_title where pid=:pid;'
            self.cursor.execute(update, {'new_title': new_title, 'pid': pid})
        self.connection.commit()

    def close_connection(self):
        """
        Closes the connection with the database.
        """
        self.connection.close()
