# Importing required libraries/frameworks

from flask import Flask , render_template , redirect , request ,session ,url_for, flash
from flask import current_app as app
from application.models import *
from datetime import datetime , date
from sqlalchemy import and_, or_, func
import numpy as np
import matplotlib.pyplot as plt
import matplotlib,os
matplotlib.use("Agg")


############################################ ROUTE FUNCTIONALITIES COMMON FOR ADMIN/USER ###########################################



# Routing for user/admin login page 

@app.route('/userlogin', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        u_name = request.form.get('u_name')  # u_name refers to the input provided as username
        pwd = request.form.get('pwd')  # pwd refers to the input provided as password
        # User Authentication process
        this_user = User.query.filter_by(username=u_name).first()
        if this_user:
            if this_user.password == pwd:
                session['user_id'] = this_user.id  # Store user_id in session
                if this_user.type == "admin":
                    return redirect('/admin')
                else:
                    return redirect(f'/user/{this_user.id}')
            else:
                return "Incorrect password!"
        else:
            return "User does not exist!"
    return render_template('login.html')



# Routing for user/admin logout operation

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user_id from the session
    return redirect('/userlogin')



# Routing for Registration operation 

@app.route('/register' , methods=['GET' , 'POST'])
def user_register():
    if request.method == 'POST':
        u_name = request.form.get('u_name') #u_name refers to the input provided as username 
        pwd = request.form.get('pwd') #pwd refers to the input provided as password 
        f_name = request.form.get('f_name') #f_name refers to the input provided as fullname 
        qlf = request.form.get('qlf') #qlf refers to the input provided as qualification
        dob = request.form.get('dob') #dob refers to the input provided as date of birth
        d_o_b=datetime.strptime(dob,'%Y-%m-%d').date() #Converting string into Date object
        
        #User authentication process
        this_user = User.query.filter_by(username = u_name).first()
        if this_user:
            return 'User already exists!'
        else:
            new_user = User(username=u_name,password=pwd,fullname=f_name,qualification=qlf,date_of_birth=d_o_b)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')
    return render_template ('register.html')


############################################ ROUTE FUNCTIONALITIES FOR ADMIN ###########################################

# Routing for admin dashboard page

@app.route('/admin', methods=['GET','POST'])
def admin_login():
    # Fetch user(type="admin")
    user = User.query.filter_by(type="admin").first()
    # Fetch all subjects and chapters from the database
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()

    # Render the admin dashboard template
    return render_template(
        'admin_dashboard.html',
        user=user,
        subjects=subjects,
        chapters=chapters,
        quizzes=quizzes
    )



# Routing for admin quiz management page

@app.route('/admin_quiz_management', methods=['GET','POST'])
def admin_quiz_management():
    # Fetch user(type="admin")
    user = User.query.filter_by(type="admin").first()
    # Fetch all quizzes, chapters, and questions from the database
    quizzes = Quiz.query.all()
    chapters = Chapter.query.all()
    questions = Question.query.all()

    # Render the admin quiz management template
    return render_template(
        'admin_quiz_management.html',
        quizzes=quizzes,
        chapters=chapters,
        questions=questions,
        user=user
    )



# Routing to implement create new subject functionality in admin dashboard page

@app.route('/create_new_subject',methods=['GET' , 'POST'])
def new_subject():
    if request.method=='POST':
        name=request.form.get('subject_name')
        description=request.form.get('description')
        new_subject=Subject(name=name,description=description)
        # db.session.commit(new_subject)
        db.session.add(new_subject)
        db.session.commit()
        return redirect('/admin')
    return render_template('new_subject.html')



# Routing to implement delete a subject functionality in admin dashboard page

@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    # Fetch the subject to be deleted
    subject = Subject.query.get_or_404(subject_id)
    # Delete the subject and all related data
    try:
        db.session.delete(subject)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    # Redirect back to the admin dashboard
    return redirect('/admin')



# Routing to implement create new chapter functionality in admin dashboard page

@app.route('/create_new_chapter/<int:subject_id>', methods=['GET', 'POST'])
def new_chapter(subject_id):
    # Fetch the subject details
    subject = Subject.query.get_or_404(subject_id)

    if request.method == 'POST':
        # Get form data
        chapter_name = request.form.get('chapter_name')
        description = request.form.get('description')

        # Create a new Chapter entry
        new_chapter = Chapter(
            subject_id=subject.id,
            name=chapter_name,
            description=description
        )

        # Add and commit to the database
        db.session.add(new_chapter)
        db.session.commit()

        return redirect('/admin')  # Redirect to the admin dashboard after saving

    # Render the form template for GET requests
    return render_template('new_chapter.html', subject=subject)



# Routing to implement edit chapter functionality in admin dashboard page

@app.route('/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    # Fetch the chapter details
    chapter = Chapter.query.get_or_404(chapter_id)
    subject = Subject.query.get_or_404(chapter.subject_id)

    if request.method == 'POST':
        # Update the chapter details with form data
        chapter.name = request.form.get('chapter_name')
        chapter.description = request.form.get('description')

        # Commit changes to the database
        db.session.commit()

        return redirect('/admin')  # Redirect to the admin dashboard after saving

    # Render the edit chapter template for GET requests
    return render_template(
        'edit_chapter.html',
        chapter=chapter,
        subject=subject
    )



# Routing to implement delete chapter functionality in admin dashboard page

@app.route('/delete_chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    # Fetch the chapter to be deleted
    chapter = Chapter.query.get_or_404(chapter_id)

    # Fetch all quizzes associated with the chapter
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()

    # Delete all questions associated with the quizzes
    for quiz in quizzes:
        Question.query.filter_by(quiz_id=quiz.id).delete()

    # Delete all quizzes associated with the chapter
    Quiz.query.filter_by(chapter_id=chapter.id).delete()

    # Delete the chapter
    db.session.delete(chapter)

    # Commit changes to the database
    db.session.commit()

    # Redirect back to the admin dashboard page
    return redirect('/admin')



# Routing to implement new quiz functionality in admin quiz management page

@app.route('/create_new_quiz', methods=['GET', 'POST'])
def new_quiz():
    # Fetch all subjects and chapters from the database
    subjects = Subject.query.all()
    chapters = Chapter.query.all()

    if request.method == 'POST':
        # Get form data
        subject_id = request.form.get('subject_name')
        chapter_id = request.form.get('chapter_name')
        date_string = request.form.get('date')
        duration_string = request.form.get('duration')

        # Validate and convert date
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Expected YYYY-MM-DD."

        # Validate and convert duration
        try:
            # Append ":00" to make it HH:MM:SS for HH:MM format
            duration_string = f"{duration_string}:00"
            duration = datetime.strptime(duration_string, '%H:%M:%S').time()
        except ValueError:
            return "Invalid duration format. Expected HH:MM."

        # Create a new Quiz entry
        new_quiz = Quiz(
            subject_id=subject_id,
            chapter_id=chapter_id,
            date_of_quiz=date,
            time_duration=duration,
            no_of_questions=0  # Initialize with 0 questions
        )

        # Add and commit to the database
        db.session.add(new_quiz)
        db.session.commit()

        return redirect('/admin_quiz_management')

    # Render the form template for GET requests
    return render_template('new_quiz.html', subjects=subjects, chapters=chapters)



# Routing to implement delete quiz functionality in admin quiz management page

@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    try:
        # Fetch the quiz to be deleted
        quiz = Quiz.query.get_or_404(quiz_id)

        # Delete the quiz (cascade will handle related questions/scores)
        db.session.delete(quiz)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        
    return redirect('/admin_quiz_management')



# Routing to implement new question functionality in admin quiz management page

@app.route('/create_new_question/<int:quiz_id>', methods=['GET', 'POST'])
def new_question(quiz_id):
    # Fetch the quiz and chapter details
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter = Chapter.query.get_or_404(quiz.chapter_id)

    if request.method == 'POST':
        # Get form data
        question_statement = request.form.get('question_statement')
        question_topic = request.form.get('question_topic')
        option_1 = request.form.get('option1')
        option_2 = request.form.get('option2')
        option_3 = request.form.get('option3')
        option_4 = request.form.get('option4')
        correct_option = int(request.form.get('correctOption'))

        # Create a new Question entry
        new_question = Question(
            quiz_id=quiz.id,
            subject_id=quiz.subject_id,
            chapter_id=quiz.chapter_id,
            question_statement=question_statement,
            question_topic=question_topic,   
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            correct_option=correct_option
        )

        # Add and commit to the database
        db.session.add(new_question)

        # Update the number of questions in the Quiz table
        quiz.no_of_questions = Question.query.filter_by(quiz_id=quiz.id).count()
        db.session.commit()

        return redirect(f'/create_new_question/{quiz_id}')  # Redirect to the same page to add more questions

    # Render the form template for GET requests
    return render_template('new_question.html', quiz=quiz, chapter=chapter)



# Routing to implement edit question functionality in admin quiz management page

@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    # Fetch the question details
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get_or_404(question.quiz_id)
    chapter = Chapter.query.get_or_404(quiz.chapter_id)

    if request.method == 'POST':
        # Update the question details with form data
        question.question_topic = request.form.get('question_topic')  # Corrected this line
        question.question_statement = request.form.get('question_statement')
        question.option_1 = request.form.get('option1')
        question.option_2 = request.form.get('option2')
        question.option_3 = request.form.get('option3')
        question.option_4 = request.form.get('option4')
        question.correct_option = int(request.form.get('correctOption'))

        # Commit changes to the database
        db.session.commit()

        return redirect(f'/admin_quiz_management')  # Redirect to the quiz management page after saving

    # Render the edit question template for GET requests
    return render_template(
        'edit_question.html',
        question=question,
        quiz=quiz,
        chapter=chapter
    )



# Routing to implement delete question  functionality in admin quiz management page

@app.route('/delete_question/<int:question_id>', methods=['GET','POST'])
def delete_question(question_id):
    # Fetch the question to be deleted
    question = Question.query.get_or_404(question_id)
    
    # Fetch the associated quiz
    quiz = Quiz.query.get_or_404(question.quiz_id)

    # Delete the question from the database
    db.session.delete(question)
    
    # Update the number of questions in the quiz
    quiz.no_of_questions = Question.query.filter_by(quiz_id=quiz.id).count()
    
    # Commit changes to the database
    db.session.commit()

    # Redirect back to the quiz management page
    return redirect('/admin_quiz_management')



# Routing to implement visualization of question information functionality in admin quiz management page

@app.route('/quiz_information/<int:quiz_id>', methods=['GET','POST'])
def quiz_information(quiz_id):
    # Fetch the quiz details
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Fetch the associated subject and chapter details
    subject = Subject.query.get_or_404(quiz.subject_id)
    chapter = Chapter.query.get_or_404(quiz.chapter_id)

    # Render the quiz information template
    return render_template(
        'quiz_information.html',
        quiz=quiz,
        subject=subject,
        chapter=chapter
    )



# Routing to implement search fuctionality for admin search operation 

@app.route('/admin_search', methods=['GET'])
def admin_search():
    search_query = request.args.get('search')  # Get the search query from the URL parameters

    # Perform the search query
    if search_query:
        # Search for quizzes based on subject name, chapter name, or quiz ID
        results = db.session.query(Quiz, Subject, Chapter) \
            .join(Subject, Quiz.subject_id == Subject.id) \
            .join(Chapter, Quiz.chapter_id == Chapter.id) \
            .filter(
                (Subject.name.ilike(f'%{search_query}%')) |
                (Chapter.name.ilike(f'%{search_query}%')) |
                (Quiz.id == search_query)
            ) \
            .all()
    else:
        results = []

    # Render the search results template
    return render_template('admin_search.html', results=results, search_query=search_query)



# Routing to implement admin summary charts page 

@app.route('/admin_summary_charts')
def admin_summary_charts():
    generate_summary_charts()
    return render_template('admin_summary_charts.html')



# Function to generate bar charts for admin summary statistics page

def generate_summary_charts():
    # Fetch all subjects
    subjects = Subject.query.all()
    
    # Create a figure with subplots
    n = int(len(subjects)/2 if len(subjects)%2==0 else len(subjects)//2+1)
    # fig, axes = plt.subplots(n, 2, figsize=(15, 5 * n))
    
    for i, subject in enumerate(subjects):
        # Fetch all quizzes for the subject
        quizzes = Quiz.query.filter_by(subject_id=subject.id).all()
        
        # Calculate total marks for the subject
        total_marks = sum(quiz.no_of_questions for quiz in quizzes)
        
        # Fetch all users whose type is not "admin"
        users = User.query.filter(User.type != "admin").all()
        
        user_names=[user.username for user in users]

        # Calculate marks obtained by each user for the subject
        user_marks = []
        for user in users:
            marks_obtained = 0
            for quiz in quizzes:
                quiz_performances = QuizPerformance.query.filter_by(user_id=user.id, quiz_id=quiz.id).all()
                marks_obtained += sum(qp.question_score for qp in quiz_performances)
            user_marks.append(marks_obtained)
        
        
        # Plot the bar chart
        plt.rcParams['figure.figsize']=[20,16]
        plt.subplot(n,2,i+1)
        colors=plt.get_cmap('coolwarm',len(users))
        plt.bar( user_names,user_marks,label=user_names,color=colors(range(len(users))) )
        plt.title(f"Plot-{i+1}:Performance in {subject.name} out of {total_marks}",fontsize=14)
        plt.xlabel("Users",fontsize=12)
        plt.ylabel("Marks Scored",fontsize=12)
        plt.ylim(0, 30)  # Set y-axis limit to 0-30
        plt.legend(fontsize=12)
    
    # Save the figure to the static folder
    chart_path = os.path.join('static', 'summary_chart.png')
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()




############################################ ROUTE FUNCTIONALITIES FOR USER ###########################################



# Routing to implement functionality for user dashboard page

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_log_in(user_id):
    
    # Check if the user is logged in for the session or not
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect('/userlogin')  # Redirect to login if user is not logged in
    user = User.query.get_or_404(user_id)

    # Fetch all quizzes for the current user in the session
    quizzes = Quiz.query.all()

    # Initialize QuizStatus entries for the user if they don't exist
    for quiz in quizzes:
        quiz_status = QuizStatus.query.filter_by(user_id=user_id, quiz_id=quiz.id).first()
        if not quiz_status:
            quiz_status = QuizStatus(user_id=user_id, quiz_id=quiz.id, status='unattempted')
            db.session.add(quiz_status)
    db.session.commit()

    # Update QuizStatus for expired quizzes
    for quiz in quizzes:
        if quiz.date_of_quiz < date.today():  # Check if the quiz date has passed
            quiz_status = QuizStatus.query.filter_by(user_id=user_id, quiz_id=quiz.id).first()
            if quiz_status and quiz_status.status == 'unattempted':
                quiz_status.status = 'quiz expired'
                db.session.commit()

    # Step 1: Define the join condition between Quiz and QuizStatus datatables
    join_condition = Quiz.id == QuizStatus.quiz_id

    # Step 2: Define the filter conditions for unattempted upcoming quizzes
    filter_conditions = and_(
        QuizStatus.user_id == user_id,  # Filter by the logged-in user
        QuizStatus.status == 'unattempted',  # Filter by unattempted status
        Quiz.date_of_quiz >= date.today()  # Filter by upcoming quizzes
    )

    # Step 3: Perform the query
    upcoming_unattempted_quizzes = (
        db.session.query(Quiz)
        .join(QuizStatus, join_condition)  # Join Quiz and QuizStatus
        .filter(filter_conditions)  # Apply the filter conditions
        .all()  # Fetch all matching quizzes
    )

    # Fetch the first question ID for each quiz
    for quiz in upcoming_unattempted_quizzes:
        first_question = Question.query.filter_by(quiz_id=quiz.id).first()
        quiz.first_question_id = first_question.id if first_question else None

    return render_template('user_dashboard.html', user=user, quizzes=upcoming_unattempted_quizzes)




# Routing to implement quiz information display functionality in user dashboard page

@app.route('/user_quiz_information/<int:quiz_id>', methods=['GET', 'POST'])
def user_quiz_information(quiz_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect('/userlogin')  # Redirect to login if user is not logged in

    # Fetch the quiz details
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Fetch the associated subject and chapter details
    subject = Subject.query.get_or_404(quiz.subject_id)
    chapter = Chapter.query.get_or_404(quiz.chapter_id)

    # Fetch the logged-in user from the session
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    # Render the quiz information template
    return render_template(
        'user_quiz_information.html',
        quiz=quiz,
        subject=subject,
        chapter=chapter,
        user=user  # Pass the user object to the template
    )


# Routing to implement start quiz functionality in user dashboard page

@app.route('/start_quiz/<int:quiz_id>/<int:question_id>', methods=['GET'])
def start_quiz(quiz_id, question_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect('/userlogin')  # Redirect to login if user is not logged in

    # Fetch the logged-in user
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    # Fetch the quiz
    quiz = Quiz.query.get_or_404(quiz_id)

    # Update QuizStatus to 'attempted' for the current user and quiz
    quiz_status = QuizStatus.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
    if quiz_status and quiz_status.status == 'unattempted':
        quiz_status.status = 'attempted'
        db.session.commit()

    # Fetch all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.id).all()

    # Fetch the current question
    current_question = Question.query.get_or_404(question_id)

    # Calculate the current question's index
    current_question_index = next((index for index, q in enumerate(questions) if q.id == question_id), 0) + 1

    # Render the start_the_quiz template
    return render_template(
        'start_the_quiz.html',
        user=user,
        quiz=quiz,
        questions=questions,
        current_question=current_question,
        current_question_index=current_question_index  # Pass the current question index
    )



# Routing to implement save answer functionality of save and next button of start quiz page

@app.route('/save_answer', methods=['POST'])
def save_answer():
    # Get form data
    user_id = request.form.get('user_id')
    quiz_id = request.form.get('quiz_id')
    question_id = request.form.get('question_id')
    user_answer = request.form.get('answer')
    action = request.form.get('action')  # 'save_and_next' or 'submit'

    # Fetch the current question
    question = Question.query.get_or_404(question_id)

    # Handle Save & Next action
    if action == 'save_and_next':
        # Validate if an option is selected
        if not user_answer:
            flash("Please select an option to continue.", "error")
            return redirect(url_for('start_quiz', quiz_id=quiz_id, question_id=question_id))

        # Save the answer to QuizPerformance
        is_correct = int(user_answer) == question.correct_option
        question_score = 1 if is_correct else 0

        quiz_performance = QuizPerformance(
            user_id=user_id,
            quiz_id=quiz_id,
            question_id=question_id,
            user_answer=int(user_answer),
            question_score=question_score
        )
        db.session.add(quiz_performance)
        db.session.commit()

        # Fetch all questions for the quiz
        questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.id).all()

        # Find the index of the current question
        current_index = next((index for index, q in enumerate(questions) if q.id == int(question_id)), 0)

        # Determine the next question ID
        next_index = (current_index + 1) % len(questions)  # Loop back to the first question if at the end
        next_question_id = questions[next_index].id
        return redirect(url_for('start_quiz', quiz_id=quiz_id, question_id=next_question_id))

    # Handle Submit action
    elif action == 'submit':
        # Save the answer to QuizPerformance if an option is selected
        if user_answer:
            is_correct = int(user_answer) == question.correct_option
            question_score = 1 if is_correct else 0

            quiz_performance = QuizPerformance(
                user_id=user_id,
                quiz_id=quiz_id,
                question_id=question_id,
                user_answer=int(user_answer),
                question_score=question_score
            )
            db.session.add(quiz_performance)
            db.session.commit()

        # Evaluate the quiz and save the results to the Score table
        return evaluate_quiz_and_redirect(user_id, quiz_id)

    # Default fallback
    return redirect(url_for('start_quiz', quiz_id=quiz_id, question_id=question_id))

# Function to implement evaluation of quiz and redirect to user score page on submit button operation

def evaluate_quiz_and_redirect(user_id, quiz_id):
    # Fetch all questions for the quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    total_questions = len(questions)

    # Fetch the latest QuizPerformance entry for each question
    latest_performances = (
        db.session.query(
            QuizPerformance.question_id,
            func.max(QuizPerformance.id).label('latest_id')
        )
        .filter_by(user_id=user_id, quiz_id=quiz_id)
        .group_by(QuizPerformance.question_id)
        .subquery()
    )

    # Join with QuizPerformance to get the latest scores
    quiz_performances = (
        db.session.query(QuizPerformance)
        .join(
            latest_performances,
            QuizPerformance.id == latest_performances.c.latest_id
        )
        .all()
    )

    # Calculate the user's score based on the latest answers
    user_score = sum(performance.question_score for performance in quiz_performances)

    # Fetch the quiz to get subject_id and chapter_id
    quiz = Quiz.query.get_or_404(quiz_id)

    # Save the results to the Score table
    score_entry = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        subject_id=quiz.subject_id,
        chapter_id=quiz.chapter_id,
        time_stamp_of_attempt=datetime.now().date(),
        total_score=user_score,
        full_score=total_questions  # Total marks is the number of questions
    )
    db.session.add(score_entry)
    db.session.commit()

    # Redirect the user to the user_scores.html page
    return redirect(url_for('user_scores', user_id=user_id))




# Routing to implement user score page functionality 

@app.route('/user_scores/<int:user_id>')
def user_scores(user_id):
    # Fetch the logged-in user
    user = User.query.get_or_404(user_id)

    # Step 1: Check QuizStatus for quizzes with status "quiz expired"
    expired_quizzes = (
        db.session.query(QuizStatus.quiz_id)
        .filter_by(user_id=user_id, status="quiz expired")
        .all()
    )

    # Step 2: Update the Score table for expired quizzes
    for quiz_status in expired_quizzes:
        quiz_id = quiz_status.quiz_id

        # Fetch the quiz to get the number of questions
        quiz = Quiz.query.get_or_404(quiz_id)
        total_questions = quiz.no_of_questions

        # Check if a Score entry already exists for this quiz and user
        score_entry = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()

        if not score_entry:
            # Create a new Score entry if it doesn't exist
            score_entry = Score(
                quiz_id=quiz_id,
                user_id=user_id,
                subject_id=quiz.subject_id,
                chapter_id=quiz.chapter_id,
                time_stamp_of_attempt=None,
                total_score=0,
                full_score=total_questions
            )
            db.session.add(score_entry)
        else:
            # Update the existing Score entry
            score_entry.time_stamp_of_attempt = None
            score_entry.total_score = 0
            score_entry.full_score = total_questions

    db.session.commit()

    # Step 3: Fetch all scores for the user with related Quiz, Subject, Chapter, and QuizStatus data
    scores = (
        db.session.query(Score, QuizStatus.status)
        .join(Quiz, Score.quiz_id == Quiz.id)
        .join(Subject, Quiz.subject_id == Subject.id)
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .outerjoin(QuizStatus, (QuizStatus.quiz_id == Score.quiz_id) & (QuizStatus.user_id == Score.user_id))
        .options(db.joinedload(Score.score_quiz).joinedload(Quiz.quiz_subject))
        .options(db.joinedload(Score.score_quiz).joinedload(Quiz.quiz_chapter))
        .filter(Score.user_id == user_id)
        .all()
    )

    # Step 4: Pass the scores data to the template
    return render_template('user_scores.html', user=user, scores=scores)




# Routing to implement search functionality for user

@app.route('/user_search/<int:user_id>', methods=['GET'])
def user_search(user_id):
    search_query = request.args.get('search')  # Get the search query from the URL parameters

    # Fetch the user object
    user = User.query.get_or_404(user_id)

    # Perform the search query
    if search_query:
        # Search for quizzes based on subject name, chapter name, or quiz ID
        results = db.session.query(Quiz, Subject, Chapter, QuizStatus) \
            .join(Subject, Quiz.subject_id == Subject.id) \
            .join(Chapter, Quiz.chapter_id == Chapter.id) \
            .join(QuizStatus, Quiz.id == QuizStatus.quiz_id) \
            .filter(
                and_(
                    QuizStatus.user_id == user_id,  # Ensure the quiz status belongs to the logged-in user
                    or_(
                        Subject.name.ilike(f'%{search_query}%'),
                        Chapter.name.ilike(f'%{search_query}%'),
                        Quiz.id == search_query
                    )
                )
            ) \
            .all()
    else:
        results = []

    # Render the search results template
    return render_template('user_search.html', results=results, search_query=search_query, user=user)




# Route to generate  user summary statistics page

@app.route('/user_summary_charts/<int:user_id>')
def user_summary_charts(user_id):

    # Fetch the logged-in user
    user = User.query.get_or_404(user_id)

    chart_filename = generate_user_summary_charts(user_id)
    return render_template('user_summary_charts.html', user=user, chart_filename=chart_filename)

#Function to generate bar charts for user summary statistics

def generate_user_summary_charts(user_id):
    # Fetch the user
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")

    # Fetch all subjects
    subjects = Subject.query.all()

    # Prepare data for plotting
    subject_names = []
    subject_marks = []
    total_marks_list = []

    for subject in subjects:
        # Fetch all quizzes for the subject
        quizzes = Quiz.query.filter_by(subject_id=subject.id).all()

        # Calculate total marks for the subject
        total_marks = sum(quiz.no_of_questions for quiz in quizzes)

        # Calculate marks obtained by the user for the subject
        marks_obtained = 0
        for quiz in quizzes:
            quiz_performances = QuizPerformance.query.filter_by(user_id=user.id, quiz_id=quiz.id).all()
            marks_obtained += sum(qp.question_score for qp in quiz_performances)

        # Append data for plotting
        subject_names.append(subject.name)
        subject_marks.append(marks_obtained)
        total_marks_list.append(total_marks)

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(subject_names)))  # Generate distinct colors

    bars = plt.bar(subject_names, subject_marks, color=colors)

    # Add labels and title
    plt.title(f"Performance of {user.username} in various subjects")
    plt.xlabel("Subjects")
    plt.ylabel("Marks Scored")
    plt.ylim(0, 30)  # Set y-axis limit to 0-30
    plt.xticks(rotation=0, ha="center")  # Rotate x-axis labels for better readability

    # Add legend to the plot
    legend_labels = [f"Subject:{subject_names[i]} | Total marks:{total_marks_list[i]}" for i in range(len(subject_names))]
    plt.legend(bars, legend_labels, title="Subject Details", bbox_to_anchor=(.55, 1), loc='upper left')

    # Save the figure to the static folder
    chart_filename = f'user_summary_chart_{user.id}.png'
    chart_path = os.path.join(app.static_folder, chart_filename)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_filename  # Return the filename for use in the template