from flask import Flask

# New imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# force loading of environment variables
load_dotenv('.flaskenv')

# Get the environment variables from .flaskenv
# Google Cloud SQL (change this accordingly)
# Get the environment variables from .flaskenv
USERNAME="root"
PASSWORD="csc400dcdgjc22"
PROJECT_ID ="CSC400-CFIT"
INSTANCE_NAME ="csc400-cfit"
DB_IP="34.122.98.59"
DB_NAME="SCSU_CFIT"

app = Flask(__name__)

app.secret_key = "scsu_cfit"
app.config["SECRET_KEY"] = "scsu_cfit"

# SQL Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{DB_IP}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

# Create database connection and associate it with the Flask application
db = SQLAlchemy(app)

login = LoginManager(app)

# enables @login_required
login.login_view = 'login'

# Add models
from app import routes, models
from app.models import user


# Create admin and basic user account on application deployment
user = user.query.filter_by(username='admin').first()
if user is None:
    user_admin = user(username='admin', role='admin')
    user_admin.set_password('csc400sum22')
    db.session.add(user_admin)
    db.session.commit()


