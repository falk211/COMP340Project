from flask import Flask, render_template, jsonify, request
import os
import psycopg

from flask import redirect, url_for, flash

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "your-very-secret-key"
@app.route('/')
def loginpage():
    return render_template('login.html')



@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    print(username, password)


    if username == "admin" and password == "pass123":
        return redirect(url_for("homepage"))
    else:
        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route('/signup')
def signuppage():
    return render_template('signup.html')

@app.route('/homepage')
def homepage():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(use_reloader = False, debug=True)

