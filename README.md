# PageBook
This repo showcases some of the possibilities that result from using SQL in a host programming language. Specifically, PageBook uses a Python interface to SQLite3 via pysqlite.

PageBook is a command line program that allows users to post questions and answers, search posts, or vote on a post and further allows priveleged users to mark an answer as the accepted answer for a question, give a badge to another user, add a tag to a post, or edit the title and/or body of a post. Unregistered users can also sign up and login by providing a unique username along with other info. The database is updated accordingly.

## Developers
- Ryan Kortbeek
- Harsh Shah

## Installation
1. Download source (clone repo)

2. Ensure sqlite3 is installed (see [here](https://www.sqlite.org/download.html) for more info)

3. Ensure pysqlite is installed

`pip install pysqlite` | `pip3 install pysqlite`

4. Create a database following the schema from [prj-tables.sql](https://github.com/ryankortbeek/PageBook/blob/master/prj-tables.sql) (optimally so that its located in the source directory)

`sqlite3 DBNAME.db <prj-tables.sql`

The sqlite3 database, DBNAME.db, can then be populated with the desired data.

## Instructions for Use
1. Navigate to the directory containing the source code files for PageBook
2. Run PageBook on the database (as created above) located at PATH_TO_DATABASE

`python3 prj.py PATH_TO_DATABASE`

## System Architecture
*Note that more details can be found regarding all aspects of the classes and methods below through the comments and structure of the source code.*

PageBook is based on the individual design of various components in which users will enter and query data. The software architecture is designed to incorporate all data entries and modification into an integrated database.

The main components that comprising our software architecture are: the DBManager class, the Screen classes (StartScreen, SignUpScreen, LoginScreen, MainMenuScreen, PostQuestion Screen, SearchScreen, SearchResultsScreen, and PostActionScreen), and the PageBook class.

### DBManager
This class handles the interaction between python and the sqlite database this program is running on. Some of the major functions are:
- def valid_login
- def add_user
- def new_post
- def execute_search
- def add_vote
- def updated_accepted_answer - def give_badge
- def add_tag_to_post
- def update_post
- def check_privilege

### BaseScreen
This class will be handling layers of user interactions and executing certain functionalities based on user input. Few major function definitions used are:
- def _setup: must be implemented by all subclasses and is called in the constructor
- def run: this method should be the single access point to the functionality that the screen
supports and should run that functionality upon being called - depending on the screen it may
or may not return something

### StartScreen
Allows users to specify whether they are a registered or unregistered user. Also allows the user to exit the program.

### LoginScreen
Registered users are taken here and they can login with their username (matches are case-insensitive) and password (matches are case-sensitive).

### SignUpScreen
Unregistered users are taken here and are able to sign up and login by providing a unique uid along with a name, a city, and a password.

### MainMenuScreen
Upon logging in, a user is able to select from the following options: “post a question”, “search for a post”, “logout”, and “exit”. Selecting the post a question option will direct the user to the post question screen. Selecting the search for a post option will direct the user to the search screen. Selecting the logout option will direct the user to the first screen of the system. Selecting the exit option will allow the user to exit the program directly.

### PostQuestionScreen
Allows the user to post a question by providing title and body texts.

### SearchScreen
Allows the user to provide one or more keywords and finds all the posts that contain at least one keyword in either its title, body, or tag fields. If there are no matching search results, notifies the user and take them back to the main menu screen. If there are matching results, directs the user to the search results screen.

### SearchResultsScreen
Displays at most 5 matching posts at a time and allows the user to return to the main menu, see more matching posts (if there are any), or select a post to perform a post action on.
Notable private method:
- def _post_action_prompt

### PostActionScreen
Displays the post that the user has selected to perform an action on and gives the user a list of actions that they can take based on a number of factors (see below). The actions are as follows:
- Post an answer: available when the selected post is a question and to all users
- Vote for a post: available when the user has not already voted on the selected post and to all
users
- Mark as accepted: only available to privileged users when the selected post is an answer
- Give a badge to the poster: only available to privileged users when the poster has not
already been given a badge on the current day
- Add tags to the post: only available to privileged users
- Edit title and/or body of post: only available to privileged users
After an action has been completed the user is directed back to the main menu. Notable private methods:
- def display_options 
- def add_vote
- def get_new_answer_data
- def edit_pos
- def post_answer

### PageBook
This class initializes an instance of the DBManager class and controls the flow of the program, namely which screens to navigate to based on return values from the Screen.run() methods. Calls the DBManager.close_connection() when exiting to ensure that the connection to the database is closed properly.
