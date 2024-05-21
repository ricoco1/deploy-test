from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
import hashlib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

@app.route('/', methods=['GET'])
def home():
    return render_template('home/index.html')

@app.route('/rooms', methods=['GET'])
def rooms():
    return render_template('room/rooms.html')

@app.route('/rooms/deluxe', methods=['GET'])
def deluxe_room():
    return render_template('room/rooms.html')

@app.route('/rooms/deluxe_family', methods=['GET'])
def deluxe_family():
    return render_template('room/deluxe_family.html')

@app.route('/facilities', methods=['GET'])
def facilities():
    return render_template('facilities/facilities.html')

@app.route('/gallery', methods=['GET'])
def gallery():
    return render_template('gallery/gallery.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact/contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register/register.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    return render_template('book/book.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
