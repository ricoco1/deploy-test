from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv
import hashlib
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = 'static/img/uploads/profile'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Max Upload 16mb
app.secret_key = 'supersecretkey'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")
SECRET_KEY = 'MYSECRETKEY'

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def get_user_info():
    if 'logged_in' in session:
        email = session['email']
        user_info = db.users.find_one({'email': email})
        return user_info
    return None

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

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')

    user = db.users.find_one({'email': email})

    if user:
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user['password'] == hashed_password:
            session['logged_in'] = True
            session['email'] = email
            session['full_name'] = user['full_name']
            return jsonify({'result': 'success', 'msg': 'Login berhasil'})
        else:
            return jsonify({'result': 'fail', 'msg': 'Password Salah!!!'})

@app.route('/book', methods=['GET'])
def book():
    return render_template('book/book.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        phone_number = request.form.get('phoneNumber')
        birth_date = request.form.get('birthDate')
        gender = request.form.get('gender')
        address = request.form.get('address')
        city = request.form.get('city')
        region = request.form.get('region')
        postal_code = request.form.get('postalCode')

        if not full_name or not email or not password or not confirm_password or not phone_number or not birth_date or not gender or not address or not city or not region or not postal_code:
            return jsonify({'error': 'Semua field yang diberi tanda * harus diisi.'}), 400

        if password != confirm_password:
            return jsonify({'error': 'Kata sandi dan konfirmasi kata sandi tidak cocok.'}), 400

        if db.users.find_one({'email': email}):
            return jsonify({'error': 'Email sudah digunakan.'}), 400

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        profile_picture_url = url_for('static', filename='img/uploads/profile/profile_placeholder.png')

        user_data = {
            'full_name': full_name,
            'email': email,
            'password': hashed_password,
            'phone_number': phone_number,
            'birth_date': birth_date,
            'gender': gender,
            'address': address,
            'city': city,
            'region': region,
            'postal_code': postal_code,
            'profile_picture_url': profile_picture_url
            
        }

        db.users.insert_one(user_data)
        return jsonify({'success': 'Pendaftaran berhasil!'}), 200

    return render_template('register/register.html')

@app.route("/login")
def login():
    msg = request.args.get("msg")
    return render_template("login/login.html", msg=msg)

@app.route("/user/index")
def user_index():
    user_info = get_user_info()
    if user_info:
        return render_template('user/home/index.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

# khusus user login yang bisa akses
@app.route('/user/rooms', methods=['GET'])
def user_rooms():
    user_info = get_user_info()
    if user_info:
        return render_template('user/room/rooms.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/rooms/deluxe', methods=['GET'])
def user_deluxe_room():
    user_info = get_user_info()
    if user_info:
        return render_template('user/room/deluxe.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/rooms/deluxe_family', methods=['GET'])
def user_deluxe_family():
    user_info = get_user_info()
    if user_info:
        return render_template('user/room/deluxe_family.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/facilities', methods=['GET'])
def user_facilities():
    user_info = get_user_info()
    if user_info:
        return render_template('user/facilities/facilities.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/gallery', methods=['GET'])
def user_gallery():
    user_info = get_user_info()
    if user_info:
        return render_template('user/gallery/gallery.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/contact', methods=['GET'])
def user_contact():
    user_info = get_user_info()
    if user_info:
        return render_template('user/contact/contact.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/profile', methods=['GET'])
def user_profile():
    user_info = get_user_info()
    if user_info:
        return render_template('user/profile/profile.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' in session:
        email = session['email']
        user_info = db.users.find_one({'email': email})

        if request.method == 'POST':
            full_name = request.form.get('fullName')
            phone_number = request.form.get('phoneNumber')
            birth_date = request.form.get('birthDate')
            gender = request.form.get('gender')
            address = request.form.get('address')
            city = request.form.get('city')
            region = request.form.get('region')
            postal_code = request.form.get('postalCode')

            db.users.update_one(
                {'email': email},
                {'$set': {
                    'full_name': full_name,
                    'phone_number': phone_number,
                    'birth_date': birth_date,
                    'gender': gender,
                    'address': address,
                    'city': city,
                    'region': region,
                    'postal_code': postal_code
                }}
            )
            return redirect(url_for('user_profile'))
        
        return render_template('user/profile/edit_profile.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/profile/upload_photo', methods=['POST'])
def upload_photo():
    if 'logged_in' in session:
        email = session['email']
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture:
                filename = secure_filename(profile_picture.filename)
                profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                profile_picture.save(profile_picture_path)
                
                profile_picture_url = url_for('static', filename='img/uploads/profile/' + filename)
                db.users.update_one(
                    {'email': email},
                    {'$set': {'profile_picture_url': profile_picture_url}}
                )
        return redirect(url_for('user_profile'))
    else:
        return redirect(url_for('login'))


@app.route('/user/reservasi', methods=['GET'])
def user_reservasi():
    if 'logged_in' in session:
        email = session['email']
        user_info = db.users.find_one({'email': email})
        return render_template('user/reservasi/reservasi.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/user/book', methods=['GET'])
def user_book():
    user_info = get_user_info()
    if user_info:
        return render_template('user/book/book.html', user_info=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
