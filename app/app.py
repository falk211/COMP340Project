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




@app.route('/signuppage', methods=['GET'])
def signuppage():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")
    is_handicap = request.form.get("is_handicap")
    print(first_name, last_name, email, password, user_type, is_handicap)

    uid = user_funcs.add_user(first_name, last_name, email, password, user_type, is_handicap)

    valid = user_funcs.check_user_exists(uid)
    if not valid:
        return redirect(url_for("signuppage", error="Unable to create account. Please try again."))

    return redirect(url_for("homepage", uid=uid))

@app.route('/homepage/<uid>')
def homepage(uid):
    valid = user_funcs.check_user_exists(uid)
    if not valid:
        return render_template('login.html', error="Unable to find account. Please login again.")

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

@app.route("/add_college_page/<uid>")
def add_college_page(uid):
    all_colleges = user_funcs.get_all_colleges()
    print(all_colleges)
    return render_template("add_college.html", college_list = all_colleges, uid=uid)

@app.route("/add_college/<uid>", methods=["POST"])
def add_college(uid):
    college = request.form.get("college_name")
    city = request.form.get("city_name")
    state = request.form.get("state_name")

    result = user_funcs.add_college(uid, college, city, state)

    print(f"Added college {college} for user {uid}")

@app.route("/remove_college/<uid>")
def remove_college(uid):
    return f"Remove college for user {uid}"





if __name__ == '__main__':
    app.run(use_reloader = False, debug=True)

