from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash #for hashing the password for database storage
import csv
import os
from account_creation import AccountCreationForm, username_or_email_exists, get_next_user_id, enter_user_to_database 
from login import username_exists, get_userID, checkPassword
from services.roommatePreferences import roommatePreferences, preferenceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey' 

# Dummy user data (In a real application, you'd use a database)
users = {
    "testuser": "password123",  # username: password
    "admin": "adminpass"
}

app.config['SECRET_KEY'] = 'secretkey'

csrf = CSRFProtect(app)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username_exists(username):
            if checkPassword(get_userID(username), password):
                session["user"] = username
                return redirect(url_for("dashboard"))
            else:
                flash("Password incorrect", "error")
        else:
            flash("Unregistered user", "error")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", username=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = AccountCreationForm()

    if form.validate_on_submit():
        username = form.username.data
        if form.email.data:
            email = form.email.data
        else:
            email = "" #store as empty string in DB if user doesnt provide email
        password = form.password.data


        #Making sure new account user/email doesnt already exist
        if username_or_email_exists(username, email):
            flash("Username or email already registered, please choose another.", "error")
            return redirect(url_for('create_account'))

        #Hash password for non plaintext storage
        hashed_password = generate_password_hash(password)

        #Assign successfully created account a user ID
        user_id = get_next_user_id()

        #Append the new account to the database
        enter_user_to_database(user_id, username, email, hashed_password)

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))  #Redirect after successful creation to homepage, (should take user to login page if thats not the homepage)

    return render_template('account_creation.html', form=form)

  @app.route('/preferences', methods = ['GET', 'POST'])
def prefPage():
        form = preferenceForm()

        if form.validate_on_submit():
            bed_time = form.bed_time.data
            visitor_status = form.visitor_status.data
            drinking_status = form.drinking_status.data
            smoking_status = form.smoking_status.data
            animal_status = form.animal_status.data
            dorm_status = form.dorm_status.data
            location_status = form.location_status.data
            cleanliness_score = form.cleanliness_score.data
            bedtime_score = form.bedtime_score.data
            visitor_score = form.visitor_score.data
            quiet_score = form.quiet_score.data
            drinking_score = form.drinking_score.data
            smoking_score = form.smoking_score.data
            animal_score = form.animal_score.data
            dorm_score = form.dorm_score.data
            location_score = form.location_score.data
            allergy_status = form.allergy_status.data
            allergy_score = form.allergy_score.data
            user = roommatePreferences()
            print(user.__dict__)
            user.updatePreferences(quiet_score, location_status, location_score, dorm_status, dorm_score, 
                                    animal_status, animal_score, visitor_status, 
                                    cleanliness_score, bed_time, drinking_status, smoking_status, 
                                    smoking_score, drinking_score, visitor_score, bedtime_score, 
                                    allergy_status, allergy_score)
            print(user.__dict__)
        return render_template('/roommatePreferences.html', form=form)


if __name__ == "__main__":
    app.run()

