from flask import Flask, render_template, request, redirect, url_for, session, send_file
import string
import random
import os
import hashlib
import shutil

app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))

USERS_FOLDER = 'users'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(USERS_FOLDER, exist_ok=True)


@app.route('/')
def main():
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for('notes'))

    if request.method == 'GET':
        return render_template('login.html', error=request.args.get('error', default = ''))

    if 'username' not in request.form or 'password' not in request.form or not request.form['username'] or not request.form['password']:
        return redirect(url_for('login', error='No credentials provided'))
    
    username_hash = hashlib.sha256(request.form['username'].encode()).hexdigest()
    password_hash = hashlib.sha256(request.form['password'].encode()).hexdigest()

    if username_hash not in os.listdir(USERS_FOLDER):
        return redirect(url_for('login', error='User doesn\'t exists'))
    
    real_passwd = open(os.path.join(USERS_FOLDER, username_hash)).read()

    if real_passwd != password_hash:
        return redirect(url_for('login', error='Invalid credentials'))
    
    session["username_hash"] = username_hash
    return redirect(url_for("upload_file"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session and "user_id" in session:
        return redirect(url_for('notes'))

    if request.method == 'GET':
        return render_template('register.html', error=request.args.get('error', default = ''))

    if 'username' not in request.form or 'password' not in request.form or not request.form['username'] or not request.form['password']:
        return redirect(url_for('register', error='No credentials provided'))

    username_hash = hashlib.sha256(request.form['username'].encode()).hexdigest()
    password_hash = hashlib.sha256(request.form['password'].encode()).hexdigest()
    
    if username_hash in os.listdir(USERS_FOLDER):
        return redirect(url_for('register', error='User already exists'))
    
    with open(os.path.join(USERS_FOLDER, username_hash), 'w') as f:
        f.write(password_hash)
    
    os.makedirs(os.path.join(UPLOAD_FOLDER, username_hash), exist_ok=True)
    shutil.copy2("burger.jpg", os.path.join(UPLOAD_FOLDER, username_hash))

    return redirect(url_for("login"))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if "username_hash" not in session:
        return redirect(url_for("login"))

    if request.method == 'GET':
        return render_template('upload.html', error=request.args.get('error', default = ''))
    
    if 'file' not in request.files:
        return redirect(url_for("upload_file", error="Failed to upload"))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for("upload_file", error="Failed to upload"))
    
    if not file:
        return redirect(url_for("upload_file", error="Failed to upload"))
    
    filename = os.path.join(UPLOAD_FOLDER, session["username_hash"], file.filename)

    if not os.path.normpath(filename).startswith(os.path.join(UPLOAD_FOLDER, session["username_hash"])):
        return redirect(url_for("upload_file", error="Failed to upload"))

    file.save(filename)
    return redirect(url_for("download_file"))


@app.route('/download', methods=['GET'])
def download_file():
    if "username_hash" not in session:
        return redirect(url_for("login"))

    filename = request.args.get('filename')
    
    if not filename:
        return render_template('download.html', error=request.args.get('error', default = ''))
    
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, session["username_hash"], filename)):
        return redirect(url_for("download_file", error="No such file"))

    return send_file(os.path.join(UPLOAD_FOLDER, session["username_hash"], filename))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=41337, debug=False)
