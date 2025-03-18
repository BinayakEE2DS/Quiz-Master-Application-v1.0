from .database import db    # '.datebase' because its not in root folder but in application
#from datetime import datetime 
import datetime


# Data table for User:

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), default='general')
    fullname = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    # Relationship with Scores (one-to-many)
    user_score = db.relationship("Score", back_populates="score_user", cascade="all, delete-orphan")
    
    # Relationship with QuizStatus (one-to-many)
    user_quiz_status = db.relationship("QuizStatus", back_populates="quiz_status_user", cascade="all, delete-orphan")

    # Relationship with QuizPerformance (one-to-many)
    user_quiz_performance = db.relationship("QuizPerformance", back_populates="quiz_performance_user", cascade="all, delete-orphan")

# Data table for Subject:

class Subject(db.Model):
    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationship with Quiz (one-to-many)
    subject_quiz = db.relationship("Quiz", back_populates="quiz_subject", cascade="all, delete-orphan")

    # Relationship with Chapter (one-to-many)
    subject_chapter = db.relationship("Chapter", back_populates="chapter_subject", cascade="all, delete-orphan")

# Data table for Chapter:

class Chapter(db.Model):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True , unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationship with Subject (many-to-one)
    chapter_subject = db.relationship("Subject", back_populates="subject_chapter")
    # Relationship with Quiz (one-to-many)
    chapter_quiz = db.relationship("Quiz", back_populates="quiz_chapter", cascade="all, delete-orphan")

# Data table for Quiz:

class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)  # Duration in minutes
    topic = db.Column(db.String(100), nullable=False, default="General")
    no_of_questions = db.Column(db.Integer)

    # Relationship with Subject (many-to-one)
    quiz_subject = db.relationship("Subject", back_populates="subject_quiz")

    # Relationship with Chapter (many-to-one)
    quiz_chapter = db.relationship("Chapter", back_populates="chapter_quiz")

    # Relationship with Questions (one-to-many)
    quiz_question = db.relationship("Question", back_populates="question_quiz", cascade="all, delete-orphan")

    # Relationship with Scores (one-to-many)
    quiz_score = db.relationship("Score", back_populates="score_quiz", cascade="all, delete-orphan")

    # Relationship with QuizStatus (one-to-many)
    quiz_quiz_status = db.relationship("QuizStatus", back_populates="quiz_status_quiz", cascade="all, delete-orphan")

    # Relationship with QuizPerformance (one-to-many)
    quiz_quiz_performances = db.relationship("QuizPerformance", back_populates="quiz_performance_quiz", cascade="all, delete-orphan")

# Data table for Question:

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    question_topic = db.Column(db.String(100), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option_1 = db.Column(db.String(200), nullable=False)
    option_2 = db.Column(db.String(200), nullable=False)
    option_3 = db.Column(db.String(200), nullable=False)
    option_4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # Store the index of the correct option (1-4)

    # Relationship to Quiz
    question_quiz = db.relationship("Quiz", back_populates="quiz_question")

    # Relationship with QuizPerformance (one-to-many)
    question_quiz_performance = db.relationship("QuizPerformance", back_populates="quiz_performance_question", cascade="all, delete-orphan")

# Data table for Score:

class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    time_stamp_of_attempt = db.Column(db.Date, default=datetime.date.today())
    total_score = db.Column(db.Float, nullable=False)
    full_score = db.Column(db.Float, nullable=False)

    # Composite unique constraint on user_id and quiz_id
    __table_args__ = (
        db.UniqueConstraint('user_id', 'quiz_id', name='unique_user_quiz'),
    )

    score_quiz = db.relationship("Quiz", back_populates="quiz_score")

    # Relationship with User (many-to-one)
    score_user = db.relationship("User", back_populates="user_score")


#Datatable for Quiz Status for a user

class QuizStatus(db.Model):
    __tablename__ = 'quiz_status'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='unattempted')

    # Relationship with User (many-to-one)
    quiz_status_user = db.relationship("User", back_populates="user_quiz_status")

    # Relationship with Quiz (many-to-one)
    quiz_status_quiz = db.relationship("Quiz", back_populates="quiz_quiz_status")

#Datatable for quiz performance in quizzes by users

class QuizPerformance(db.Model):
    __tablename__ = 'quiz_performance'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    user_answer = db.Column(db.Integer, nullable=False)  # Stores the option selected by the user (1-4)
    question_score = db.Column(db.Integer, nullable=False, default=0)  # 0 or 1 based on correctness

    # Relationships
    
    quiz_performance_user = db.relationship("User", back_populates="user_quiz_performance")
    quiz_performance_quiz = db.relationship("Quiz", back_populates="quiz_quiz_performances")
    quiz_performance_question = db.relationship("Question", back_populates="question_quiz_performance")




















