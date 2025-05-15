from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '12345678qwert')  # Use environment variable for secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///video-meeting.db')  # Use environment variable for database URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"  # Use blueprint name

from app import models  # Import models here

@login_manager.user_loader
def load_user(user_id):
    return models.Register.query.get(int(user_id))

from app.routes import main, chat, video  # Import blueprints

app.register_blueprint(main.bp)
app.register_blueprint(chat.bp)
app.register_blueprint(video.bp)

from app import socket_events # Import socket events
