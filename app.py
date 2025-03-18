from flask import Flask 
from application.database import db
from application.models import *
import secrets

# Generate a secure secret key
secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string used as secret key for app session


# #Creating an app object
# app=None

# #Assigning object "app" within create app function
# def create_app():
#     app = Flask(__name__) #Creating a Flask application
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///qmsdata.sqlite3"
#     db.init_app(app) # Application configured with object db
#     app.app_context().push() # Allows whatever code written in app.py to work as sever code
 
#     return app

# app=create_app()

# from application.controllers import *

# if __name__ == "__main__":
#     app.run()


# Creating an app object
app = None

# Assigning object "app" within create app function
def create_app():
    app = Flask(__name__)  # Creating a Flask application
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///qmsdata.sqlite3"
    
    # Set the secret key for session management
    app.secret_key = 'your_generated_secret_key_here'
    # app.secret_key = 'supersecretkey12345!@#$%'  # Replace with a secure secret key
    
    db.init_app(app)  # Application configured with object db
    app.app_context().push()  # Allows whatever code written in app.py to work as server code

    return app

app = create_app()

from application.controllers import *

if __name__ == "__main__":
    app.run()