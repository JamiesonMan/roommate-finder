
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash #for hashing the password for database storage
import csv
import os
from account_creation import AccountCreationForm, username_or_email_exists, get_next_user_id, enter_user_to_database 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey' 

# Dummy user data (In a real application, you'd use a database)
users = {
    "testuser": "password123",  # username: password
    "admin": "adminpass"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            if users[username] == password:
                session["user"] = username  # Store user session
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
        return redirect(url_for('home_page'))  #Redirect after successful creation to homepage, (should take user to login page if thats not the homepage)

    return render_template('account_creation.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

