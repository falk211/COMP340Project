from flask import Flask, render_template, jsonify, request
import os
import psycopg
from flask import redirect, url_for, flash
from user_funcs import UserFuncs


user_funcs = UserFuncs()

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "your-very-secret-key"
@app.route('/')
def loginpage():
    return render_template('login.html')



@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    print(email, password)

    if email is None:
        return jsonify({'error': 'Email is required'})
    if password is None:
        return jsonify({'error': 'Password is required'})


    uid = user_funcs.get_user_by_credentials(email, password)

    if uid == -1:
        return jsonify({'error': 'Email not found'})
    if uid == 0:
        return render_template("login.html", error="Invalid password")

    else:
        return redirect(url_for("homepage", uid=uid))




@app.route('/signup')
def signuppage():
    return render_template('signup.html')

@app.route('/homepage/<uid>')
def homepage(uid):
    return render_template('index.html', uid=uid)


@app.route("/reserve/<uid>", methods=["GET"])
def reserve_space(uid):
    return render_template("reserve_space.html", uid=uid)


@app.route("/reserve_confirm/<uid>", methods=["POST"])
def reserve_confirm(uid):
    selected_lot = request.form.get("lot")
    return f"Reserved {selected_lot} for user {uid}"

@app.route("/add_car/<uid>")
def add_car(uid):
    return f"Add car for user {uid}"

@app.route("/add_college/<uid>")
def add_college(uid):
    return f"Add college for user {uid}"

@app.route("/remove_college/<uid>")
def remove_college(uid):
    return f"Remove college for user {uid}"





if __name__ == '__main__':
    app.run(use_reloader = False, debug=True)

