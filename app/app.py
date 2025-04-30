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

    if not email:
        return jsonify({'error': 'Email is required'})
    if not password:
        return jsonify({'error': 'Password is required'})

    uid = user_funcs.get_user_by_credentials(email, password)
    
    if uid == -1:
        return jsonify({'error': 'Email not found'})
    if uid == 0:
        return render_template("login.html", error="Invalid password")

    admin_status = user_funcs.check_is_admin(uid)
    print(f"Admin status for user {uid}: {admin_status}")

    if admin_status == True:
        return redirect(url_for("adminpage", uid=uid))
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
    return f"Reserved {selected_lot} for user {uid}"

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
<<<<<<< HEAD
    return render_template("remove_college.html", uid=uid)


@app.route("/adminpage/<uid>")
def adminpage(uid):
    valid = user_funcs.check_user_exists(uid)
    if not valid:
        return render_template('login.html', error="Unable to find account. Please login again.")

    stats = user_funcs.get_user_statistics()

    # Extract datasets for charts
    user_type_data = stats["user_types"]
    handicap_data = stats["handicap_status"]
    college_data = stats["colleges"]
    admin_data = stats["admin_status"]
    car_make_data = stats["car_makes"]

    return render_template(
        'admin.html',
        uid=uid,
        user_type_data=user_type_data,
        handicap_data=handicap_data,
        college_data=college_data,
        admin_data=admin_data,
        car_make_data=car_make_data
    )

@app.route("/adminpage/<uid>/users")
def admin_users(uid):
    valid = user_funcs.check_user_exists(uid)
    if not valid:
        return render_template('login.html', error="Unable to find account. Please login again.")

    # Fetch all users from the database
    users = user_funcs.get_users()
    return render_template("admin_users.html", uid=uid, users=users)
=======
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
>>>>>>> refs/remotes/origin/main



if __name__ == '__main__':
    app.run(use_reloader = False, debug=True)

