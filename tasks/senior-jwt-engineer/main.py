from flask import Flask, redirect, url_for, request, render_template, make_response
import os
import random
import string

from jwtutil import gen_jwt, decode_jwt

app = Flask(__name__)
users = {"admin": "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))}

@app.route("/")
def main():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", error=request.args.get("error", default = ""))
    
    username = request.form['username']
    password = request.form['password']

    if username in users:
        return redirect(url_for("register", error="User already exists"))

    users[username] = password
    return redirect(url_for("login", error="Successfully registered"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=request.args.get("error", default = ""))
    
    username = request.form['username']
    password = request.form['password']

    if username not in users:
        return redirect(url_for("login", error="User doesn't exists"))
    
    if password != users[username]:
        return redirect(url_for("login", error="Wrong credentials"))

    resp = make_response(redirect("/flag"))
    resp.set_cookie('flag_token', gen_jwt(username))
    return resp 

@app.route("/flag", methods=["GET"])
def flag():
    if "flag_token" not in request.cookies:
        return redirect(url_for("login"))
    
    try:
        payload = decode_jwt(request.cookies["flag_token"])
    except:
        return redirect(url_for("login"))

    if "username" not in payload:
        return redirect(url_for("login"))
    
    if payload["username"] != "admin":
        return "You are not an admin bebebe!"

    return os.getenv("FLAG")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=21337, debug=False)
