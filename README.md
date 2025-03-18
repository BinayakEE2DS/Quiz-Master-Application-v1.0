# The app "Prasnottari -Quiz Master Apllication - v1.0" is using Flask for application back-end Jinja2 templating, HTML, CSS and Bootstraps for application front-endSQLite for database 

Technologies Used:
1.	Flask: A lightweight web framework for Python used to build the backend of the application.
2.	Flask-SQLAlchemy: An ORM (Object-Relational Mapping) tool to interact with the SQLite database.
3.	Flask-Security: Used for authentication and authorization, ensuring secure user and admin login.
4.	Flask-Login: Manages user sessions and login functionality.
5.	Matplotlib: Generates charts for summary statistics.
6.	Jinja2: Templating engine for rendering HTML pages dynamically.
7.	Bootstrap: Frontend framework for responsive and visually appealing UI.
8.	SQLite: Lightweight database for storing application data. Implemented database qmsdata.sqlite3

Technologies Used:
1.	Flask: A lightweight web framework for Python used to build the backend of the application.
2.	Flask-SQLAlchemy: An ORM (Object-Relational Mapping) tool to interact with the SQLite database.
3.	Flask-Security: Used for authentication and authorization, ensuring secure user and admin login.
4.	Flask-Login: Manages user sessions and login functionality.
5.	Matplotlib: Generates charts for summary statistics.
6.	Jinja2: Templating engine for rendering HTML pages dynamically.
7.	Bootstrap: Frontend framework for responsive and visually appealing UI.
8.	SQLite: Lightweight database for storing application data. Implemented database qmsdata.sqlite3

# API Design:
The application exposes the following API routes:
1.	User/Admin Login: /userlogin - Handles user and admin login.
2.	Logout: /logout - Manages logout functionality.
3.	Registration: /register - Handles new user registration.
4.	Admin Dashboard: /admin - Displays the admin dashboard.
5.	Quiz Management: /admin_quiz_management - Manages quizzes.
6.	Subject/Chapter/Quiz Operations:
o	Create/Delete Subject: /create_new_subject, /delete_subject/<int:subject_id>
o	Create/Edit/Delete Chapter: /create_new_chapter/<int:subject_id>, /edit_chapter/<int:chapter_id>, /delete_chapter/<int:chapter_id>
o	Create/Delete Quiz: /create_new_quiz, /delete_quiz/<int:quiz_id>
7.	Question Operations:
o	Edit/Delete Question: /edit_question/<int:question_id>, /delete_question/<int:question_id>
8.	Quiz Information: /quiz_information/<int:quiz_id> - Displays quiz details.
9.	Admin Search: /admin_search - Implements search functionality.
10.	Admin Summary Charts: /admin_summary_charts - Displays admin statistics.
11.	User Dashboard: /user/<int:user_id> - Displays user-specific quizzes and scores.
12.	Quiz Attempt: /start_quiz/<int:quiz_id>/<int:question_id> - Starts a quiz for the user.
13.	Save Answer: /save_answer - Saves user answers during quiz attempts.
14.	User Scores: /user_scores/<int:user_id> - Displays user scores.
15.	User Summary Charts: /user_summary_charts/<int:user_id> - Displays user statistics.

# Architecture and Features:
# Project Organization
•	Controllers: Flask routes handle all backend logic.
•	Models: SQLAlchemy models define the database schema.
•	Templates: Jinja2 templates render dynamic HTML pages.
•	Static Files: CSS and images are stored in the static folder.

# Core Features Implemented:
1.	Admin Features: Create, edit, and delete subjects, chapters, quizzes, and questions. View quiz information and summary statistics. Search functionality for chapters, subjects, and quizzes.
2.	User Features: Attempt quizzes. View quiz scores and performance history. Access personalized summary charts.
# Additional Features:
•	Secure Login System: Implemented using Flask-Login.
•	Visualization: Matplotlib generates charts for admin and user statistics.


# The required processes to start the application Quiz-Master-Application-v1.0
# Working on in Powershell in VS CODE
1. Install python -> pip install python3.12
2. Create virtual environment for the application -> python -m venv env
3. Activate environment -> .env\Scripts\Activate
4. In case the environment(.env) is corrupted/lost/deleted to install it at a go->pip install -r requirements.txt
5. We are using Bootstrap CSS Framework.External css styling hasbeen used in the frontend html pages.The front end html templates are present in the templates folder.the css files used in styling are present in the static folder.
6. application folder contains three files controllers.py,database.py and models.py file used to setup the database models and controllers for running the app.py file.
7. app.py file runs the application
8. To run the application follow the following steps:
    (a) Activate the virtual environment ->.env/bin/activate
    (b) Run the app.py file -> python app.py