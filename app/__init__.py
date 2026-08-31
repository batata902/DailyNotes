from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'token'

jwt = JWTManager(app)

def seed_database():
    with app.app_context():
        conn = sqlite3.connect('database.db')
        conn.executescript(
            open('schema.sql', 'r', encoding='utf-8').read()
        )

        conn.close()
        
from app.views import *
