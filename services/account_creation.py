from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash #for hashing the password for database storage
import csv
import os



CSV_FILE = "csv_database.csv"  #currently using csv database for sprint 1

#im starting with csv file as database, hardcoded first row headers
#appends created account to account database
def enter_user_to_database(user_id, username, email, hashed_password):

    

    with open(CSV_FILE, mode='a', newline='', encoding="utf-8-sig") as file: #had to change encoding due to flash decoding error
        writer = csv.writer(file)
        #just including what I need for account_creation, will need preferences dict,etc...
        writer.writerow([user_id, username, email, hashed_password]) 

#getting users and data from database to list in case of validating or future deleting/editing maybe
def get_existing_users():
    """ Reads the CSV file and returns a list of existing users. """
    users = []
    with open(CSV_FILE, mode='r', newline='', encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if any(row.values()): #filtering out any empty rows in case DB is empty or a user gets deleted or something
                users.append(row) #going to append entire row vs just username in case adding email paswd recovery later
    return users

#for validating if new accounts match existing password/email
def username_or_email_exists(username, email):
    users = get_existing_users()
    for user in users:
        if (user["username"] == username) or (email and user["email"] == email): #include 'email' incase its blank
            return True
    return False


#pretty sure a user ID will come in handy, so +1 to highest/last ID in database
def get_next_user_id():
    users = get_existing_users()
    if users:
       #convert str to int, find the highest ID and +1 for next ID to be assigned
       max_id = max(int(user["id"]) for user in users) 
       return max_id + 1

    return 1  #If empty database, first ID will be 1


# Flask form
class AccountCreationForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),  
        Length(min=3, max=30, message="Between 3 and 30 characters.")
    ])
    email = StringField('email', validators=[Optional()])  #email is for password recovery and optional at this time
    password = PasswordField('password', validators=[
        DataRequired(), #user and password is required, else page will refresh and alert user
        Length(min=6, max=25, message="Between 6 and 25 characters long.")
    ])
    submit = SubmitField('Create Account')
