from flask import Flask, render_template, jsonify, request
import os
import psycopg
from flask import redirect, url_for, flash
from user_funcs import UserFuncs
from car_funcs import CarFuncs

user_funcs = UserFuncs()
car_funcs = CarFuncs()

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
    lots = car_funcs.get_lots(uid)
    return render_template("reserve_space.html", lot_list=lots, uid=uid)


@app.route("/reserve_confirm/<uid>", methods=["POST"])
def reserve_confirm(uid):
    selected_lot = request.form.get("lot")
    success = car_funcs.reserve_space(uid, selected_lot)
    if not success:
        return render_template("reserve_space.html", lot_list=[], uid=uid, error="Unable to reserve space. Please try again.")
    return redirect(url_for("homepage", uid=uid))


@app.route("/check_in_page/<uid>", methods=["GET"])
def check_in_page(uid):
    print("test")
    reservations = user_funcs.get_reservations(uid)
    print("test2")
    print(reservations)
    return render_template("check_in_page.html", reservations=reservations, uid=uid)


@app.route("/check_in/<uid>", methods=["POST"])
def check_in(uid):
    lot = request.form.get("lot_name")
    space = request.form.get("snum")
    print(lot, space)
    success = user_funcs.check_in(uid, lot, space)
    if not success:
        return render_template("check_in_page.html", reservations=[], uid=uid, error="Unable to check in. Please try again.")
    return redirect(url_for("homepage", uid=uid))


@app.route("/check_out_page/<uid>", methods=["GET"])
def check_out_page(uid):
    reservations = user_funcs.get_parked_reservations(uid)
    print(reservations)
    return render_template("check_out_page.html", reservations=reservations, uid=uid)


@app.route("/check_out/<uid>", methods=["POST"])
def check_out(uid):
    lot = request.form.get("lot_name")
    space = request.form.get("snum")
    print(lot, space)
    success = user_funcs.check_out(uid, lot, space)
    if not success:
        return render_template("check_out_page.html", reservations=[], uid=uid, error="Unable to check in. Please try again.")
    return redirect(url_for("homepage", uid=uid))





@app.route("/add_car/<uid>", methods=["GET", "POST"])
def add_car(uid):
    if request.method == 'POST':
        year = request.form.get("year")
        make = request.form.get("make")
        model = request.form.get("model")
        lplate = request.form.get("lplate")
        lstate = request.form.get("lstate")
        
        car_funcs.add_car(uid, year, make, model, lplate, lstate)
        flash("Car added successfully!", "success")
        return redirect(url_for("add_car", uid=uid))
    try:
        cars = car_funcs.get_cars(uid)
    except Exception as e:
        print(f"Error fetching cars: {e}")
        cars = []
    return render_template("add_car.html", uid=uid, cars=cars)
        


@app.route("/add_college_page/<uid>")
def add_college_page(uid):
    all_colleges = user_funcs.get_user_noncolleges(uid)
    print(all_colleges)
    return render_template("add_college.html", college_list = all_colleges, uid=uid)

@app.route("/add_college/<uid>", methods=["POST"])
def add_college(uid):
    colname = request.form.get("college_name")
    city = request.form.get("city_name")
    state = request.form.get("state")
    print(colname, city, state)
    success_msg = f"Successfully added {colname} ({city}, {state})"
    result = user_funcs.add_college(uid, colname, city, state)
    print(f"Added college {colname} for user {uid}")
    all_colleges = user_funcs.get_all_colleges()
    if result:
        return redirect(url_for("homepage", uid=uid))




@app.route("/remove_college_page/<uid>")
def remove_college_page(uid):
    colleges = user_funcs.get_user_colleges(uid)
    return render_template("remove_college.html", college_list = colleges, uid=uid)

@app.route("/remove_college/<uid>", methods=["POST"])
def remove_college(uid):
    colname = request.form.get("college_name")
    city = request.form.get("city_name")
    state = request.form.get("state")
    print(colname, city, state)
    success_msg = f"Successfully added {colname} ({city}, {state})"
    result = user_funcs.remove_college(uid, colname, city, state)
    print(f"Added college {colname} for user {uid}")
    all_colleges = user_funcs.get_all_colleges()
    if result:
        return redirect(url_for("homepage", uid=uid))



if __name__ == '__main__':
    app.run(use_reloader = False, debug=True)

