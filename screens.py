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
        self.get_uid_from_table(login_uid)
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
    Class representing the main menu screen.
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
              '\t[4] Exit'.format(self.current_user))

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
        while True:
            self._get_new_question_data()
            print('\nQuestion Summary\nTitle: {}\nBody: {}\n'.format(self.question_title, self.question_body))
            print('Please select one of the following actions:\n'
                  '\t[Y/y] To confirm and post the question above\n'
                  '\t[E/e] To re-enter the question title and body\n'
                  '\t[N/n] To return to the main menu\n')
            selection = select_from_menu(valid_inputs)
            if selection.lower() == 'y':
                self.db_manager.new_post(self.question_title, self.question_body, self.current_user)
                clear_screen()
                print('POST QUESTION')
                print('\nQuestion posted successfully - please enter any key to return to the main menu:')
                input('> ')
                break
            elif selection.lower() == 'n':
                break


class SearchScreen(BaseScreen):
    """
    Class representing the search screen.
    """

    def __init__(self):
        """
        Initializes an instance of this class.
        """
        BaseScreen.__init__(self)
        self.question_title = None
        self.question_body = None

    def _setup(self):
        print('SEARCH')

    def run(self):
        """
        Prompts the user to enter one or more space seperated keywords.
        :return: list consisting of each space seperated keyword as a seperate element.
        """
        print('\nPlease enter a space separated list of keywords that you would like to search for:')
        search_string = input('> ')
        while search_string == '':
            print('You must enter at least one keyword, try again:')
            search_string = input('> ')
        return search_string.split(' ')


class SearchResultsScreen(BaseScreen):
    """
    Class representing the search results screen.
    """

    def __init__(self, db_manager, keywords_to_search):
        """
        Initializes an instance of this class.
        :param db_manager: sqlite database manager
        :param keywords_to_search: the search keywords specified by the user
        """
        self.keywords = keywords_to_search
        self.sorted_search_matches = None
        BaseScreen.__init__(self, db_manager=db_manager)

    def _setup(self):
        print('SEARCH RESULTS')
        self.sorted_search_matches = self.db_manager.execute_search(self.keywords)

    def _post_action_prompt(self, current_page, num_matches, page_upper_bound):
        """
        Prompts the user to select an action between returning to the main menu, seeing more matches (if there are more
        than 5, and so on), and selecting a post to perform an action on. A max of 5 posts are displayed at once.
        :param current_page: essentially the number of times the user has selected the see more matches action
        :param num_matches: total number of posts that contained a least one keyword in either its title, body, or tag
                            fields
        :param page_upper_bound: highest numbered matching post that is to be displayed on this page
        :return: the action that the user selected - will either be a string if they have selected to return to the
                 main menu or navigate to the next page or a tuple if they want to perform an action on a post
        """
        valid_inputs = [str(i) for i in range(current_page * 5, page_upper_bound + 1, 1)]
        if num_matches == page_upper_bound:
            valid_inputs += ['a']
            print('\nPlease select the action that you would like to take:\n'
                  '\t[a] Return to the main menu\n'
                  '\t[#] Enter the number corresponding to the post that you would like to perform an action on')
        else:
            valid_inputs += ['a', 'b']
            print('\nPlease select the action that you would like to take:\n'
                  '\t[a] Return to the main menu\n'
                  '\t[b] See more matches\n'
                  '\t[#] Enter the number corresponding to the post that you would like to perform an action on')
        selection = select_from_menu(valid_inputs)
        if selection == 'a':
            return 'main menu'
        elif selection == 'b':
            return 'next page'
        else:
            return selection

    def run(self):
        """
        Displays the results of the search - a max of 5 matching posts are displayed per page. Allows the user to either
        return to the main menu, navigate to the next page of matches and see up to the next 5 (if possible), or perform
        an action on one of the displayed posts.
        :return: a tuple corresponding to the data-fields of the selected post or 'done' if either no posts matched the
                 keywords that were searched or if the user simply selected the return to main menu option
        """
        if len(self.sorted_search_matches) == 0:
            print('\nNo posts matched your search - please enter any key to return to the main menu:')
            input('> ')
            return 'done'
        num_matches = len(self.sorted_search_matches)
        num_answers = 0
        current_page = 0
        for i in range(num_matches):
            if len(self.sorted_search_matches[i]) == 7:
                post_is_question = True
                pid, pdate, title, body, poster, num_answers, num_votes = self.sorted_search_matches[i]
            else:
                post_is_question = False
                pid, pdate, title, body, poster, num_votes = self.sorted_search_matches[i]
            print('\n\t[{}] {}\n'
                  '\t\t{}\n'
                  '\t\tID: {}\tDATE: {}\tPOSTER: {}\tVOTES: {}'
                  .format(i + 1, title, body, pid, pdate, poster, num_votes))
            if post_is_question:
                print('\t\tANSWERS: {}'.format(num_answers))
            if (((i + 1) % 5 == 0) and (i != 0)) or (i == num_matches - 1):
                action = self._post_action_prompt(current_page, num_matches, i + 1)
                if action == 'main menu':
                    return 'done'
                elif action == 'next page':
                    clear_screen()
                    print('SEARCH RESULTS')
                else:
                    return self.sorted_search_matches[int(action) - 1]


class PostActionScreen(BaseScreen):
    """
    Class representing the post action screen.
    """

    def __init__(self, db_manager, current_uid, post):
        """
        Initializes an instance of this class.
        :param db_manager: sqlite database manager
        :param current_uid: the uid of the user that is currently logged in
        :param post: a tuple corresponding to the data-fields of the selected post
        """
        if len(post) == 7:
            # Means its a question
            self.post_is_question = True
            self.pid, self.pdate, self.title, self.body, self.poster, self.num_answers, self.num_votes = post
        else:
            self.post_is_question = False
            self.num_answers = None
            self.pid, self.pdate, self.title, self.body, self.poster, self.num_votes = post
        BaseScreen.__init__(self, db_manager=db_manager, current_uid=current_uid)

    def _setup(self):
        """
        Prints the details of the selected post
        """
        print('POST ACTION')
        print('\n{}\n'
              '\t{}\n'
              '\tID: {}\tDATE: {}\tPOSTER: {}\tVOTES: {}'
              .format(self.title, self.body, self.pid, self.pdate, self.poster, self.num_votes))
        if self.post_is_question:
            print('\tANSWERS: {}'.format(self.num_answers))

    def _display_options(self):
        """
        Displays a list of actions that the user can take based on a number of factors. The actions are as
        follows... Post an answer: available when the selected post is a question and to all users. Vote for a post:
        available when the user has not already voted on the selected post and to all users. Mark as accepted: only
        available to privileged users when the selected post is an answer. Give a badge to the poster: only available to
        privileged users when the poster has not already been given a badge on the current day. Add tags to the post:
        only available to privileged users. Edit title and/or body of post: only available to privileged users.
        :return: a dictionary mapping the number to enter to trigger the corresponding action
        """
        privileged = self.db_manager.check_privilege(self.current_user)
        user_can_vote = self.db_manager.get_vote_eligibility(self.current_user, self.pid)
        poster_can_be_given_badge = self.db_manager.check_badge_eligibility(self.poster)
        choices = {}
        action_num = 1
        print('\nPlease select the action you would like to take:')
        if self.post_is_question:
            print('\t[{}] Post an answer'.format(action_num))
            choices[str(action_num)] = 'post answer'
            action_num += 1
        if user_can_vote:
            print('\t[{}] Vote on the post'.format(action_num))
            choices[str(action_num)] = 'add vote'
            action_num += 1
        if privileged:
            if not self.post_is_question:
                print('\t[{}] Mark as the accepted answer'.format(action_num))
                choices[str(action_num)] = 'mark accepted'
                action_num += 1
            if poster_can_be_given_badge:
                print('\t[{}] Give a badge'.format(action_num))
                choices[str(action_num)] = 'give badge'
                action_num += 1
            print('\t[{}] Add a tag'.format(action_num))
            choices[str(action_num)] = 'add tag'
            action_num += 1
            print('\t[{}] Edit post'.format(action_num))
            choices[str(action_num)] = 'edit'
        return choices

    def _get_new_answer_data(self):
        """
        Prompts the user to enter the title and body texts of the answer they want to add.
        :return: tuple consisting of the title and body fields of the answer that they want to add
        """
        print('\nPlease enter the title of your answer:')
        answer_title = input('> ')
        print('\nPlease enter the body of your answer:')
        answer_body = input('> ')
        return answer_title, answer_body

    def _post_answer(self):
        """
        Gets the title and body texts of the answer that the user wants to add and then confirms with the user that
        they want to post the answer that they entered - allowing them to either confirm and post their answer,
        re-enter the answer title and body, or return to the main menu and not post the answer.
        """
        valid_inputs = ['Y', 'y', 'E', 'e', 'N', 'n']
        while True:
            answer_title, answer_body = self._get_new_answer_data()
            print('\nAnswer Summary\nTitle: {}\nBody: {}\n'.format(answer_title, answer_body))
            print('Please select one of the following actions:\n'
                  '\t[Y/y] To confirm and post the answer above\n'
                  '\t[E/e] To re-enter the answer title and body\n'
                  '\t[N/n] To return to the main menu')
            selection = select_from_menu(valid_inputs)
            if selection.lower() == 'y':
                self.db_manager.new_post(answer_title, answer_body, self.current_user, True, self.pid)
                clear_screen()
                print('POST ACTION')
                print('\nAnswer posted successfully - please enter any key to return to the main menu:')
                input('> ')
                break
            elif selection.lower() == 'n':
                break

    def _add_vote(self):
        """
        Adds a vote to the selected post.
        """
        self.db_manager.add_vote(self.pid, self.current_user)
        clear_screen()
        print('POST ACTION')
        print('\nA vote has been added to the post - please enter any key to return to the main menu:')
        input('> ')

    def _mark_as_accepted(self):
        """
        Gives the privileged user the option to mark the selected post as the accepted answer to the linked question. If
        the linked question already has an accepted answer, prompts the user and asks if they would still like to change
        the accepted answer. The user can select to change the accepted answer or leave it unchanged
        """
        accepted_answer_exists = self.db_manager.check_for_accepted_answer(self.pid)
        if accepted_answer_exists:
            valid_inputs = ['Y', 'y', 'N', 'n']
            print('\nThe question linked to this answer already has an accepted answer - would you like to change it?\n'
                  '\t[Y/y] To change the accepted answer to this one\n'
                  '\t[N/n] To leave the accepted answer unchanged and return to the main menu')
            selection = select_from_menu(valid_inputs)
            if selection.lower() == 'n':
                return
        self.db_manager.update_accepted_answer(self.pid)
        clear_screen()
        print('POST ACTION')
        print('\n{} has been marked as the accepted answer - please enter any key to return to the main menu:'
              .format(self.pid))
        input('> ')

    def _give_badge(self):
        """
        Allows the user to give a badge to the poster of the selected post by providing a badge name.
        """
        bnames = self.db_manager.get_existing_badges()
        print('\nThe names of the badges that currently exist are:')
        for i in range(len(bnames)):
            bnames[i] = bnames[i].lower()
            print('\t- {}'.format(bnames[i]))
        print('\nPlease enter the name of the badge that you would like to give to {}:'.format(self.poster))
        badge_to_give = input('> ')
        while badge_to_give.lower() not in bnames:
            print('"{}" is an invalid selection, please enter a valid selection from the menu above.'
                  .format(badge_to_give))
            badge_to_give = input('> ')
        self.db_manager.give_badge(badge_to_give, self.poster)
        clear_screen()
        print('POST ACTION')
        print('\n{} has been given a badge with the name "{}" - please enter any key to return to the main menu:'
              .format(self.poster, badge_to_give))
        input('> ')

    def _add_tag(self):
        """
        Allows the user to add a tag to the post. Confirms that an identical tag has not already been added to the post.
        """
        print('\nPlease enter the name of the tag that you would like to add to {}:'.format(self.pid))
        tag_name = input('> ')
        success = self.db_manager.add_tag_to_post(self.pid, tag_name)
        clear_screen()
        print('POST ACTION')
        if success:
            print('\nSuccessfully added tag {} to {} - please enter any key to return to the main menu:'
                  .format(tag_name, self.pid))
        else:
            print('\nUnable to add tag {} to {} as it already exists - '
                  'please enter any key to return to the main menu:'.format(tag_name, self.pid))
        input('> ')

    def _edit_post(self):
        """
        Allows the user to edit the title and/or the body of the post. Other fields are not updated when the selected
        post is edited.
        """
        valid_inputs = ['1', '2', '3']
        print('\nPlease select one of the following actions:\n'
              '\t[1] Edit the title of the post\n'
              '\t[2] Edit the body of the post\n'
              '\t[3] Edit the title and the body of the post')
        selection = select_from_menu(valid_inputs)
        msg = '\n'
        if selection == '2':
            print('\nPlease enter the new body for the post:')
            new_body = input('> ')
            self.db_manager.update_post(self.pid, new_body=new_body)
            msg += 'Successfully updated the body of post {} - please enter any key to return to the main menu:'
        elif selection == '1':
            print('\nPlease enter the new title for the post:')
            new_title = input('> ')
            self.db_manager.update_post(self.pid, new_title=new_title)
            msg += 'Successfully updated the title of post {} - please enter any key to return to the main menu:'
        else:
            print('\nPlease enter the new title for the post:')
            new_title = input('> ')
            print('\nPlease enter the new body for the post:')
            new_body = input('> ')
            self.db_manager.update_post(self.pid, new_title=new_title, new_body=new_body)
            msg += 'Successfully updated the title and body of post {} - ' \
                   'please enter any key to return to the main menu:'
        clear_screen()
        print('POST ACTION')
        print(msg.format(self.pid))
        input('> ')

    def run(self):
        """
        Displays a list of actions that the user can take based on a number of factors then carries out the selected
        action. The actions are as follows... Post an answer: available when the selected post is a question and to all
        users. Vote for a post: available when the user has not already voted on the selected post and to all users.
        Mark as accepted: only available to privileged users when the selected post is an answer. Give a badge to the
        poster: only available to privileged users when the poster has not already been given a badge on the current
        day. Add tags to the post: only available to privileged users. Edit title and/or body of post: only available to
        privileged users. After an action has been completed the user is directed back to the main menu.
        """
        choices = self._display_options()
        valid_inputs = list(choices.keys())
        selection = select_from_menu(valid_inputs)
        action = choices[selection]
        if action == 'post answer':
            self._post_answer()
        elif action == 'add vote':
            self._add_vote()
        elif action == 'mark accepted':
            self._mark_as_accepted()
        elif action == 'give badge':
            self._give_badge()
        elif action == 'add tag':
            self._add_tag()
        elif action == 'edit':
            self._edit_post()
