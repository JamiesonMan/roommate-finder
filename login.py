from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash #for hashing the password for database storage
import csv
import os
from account_creation import get_existing_users

def username_exists(username):
    users = get_existing_users()
    for user in users:
        if (user["username"] == username):
            return True
    return False

def get_userID(username):
    users = get_existing_users()
    for user in users:
        if(user["username"] == username):
            return user["id"]

def checkPassword(user_id, password):
    users = get_existing_users()
    for user in users:
        if(user["id"] == user_id):
            return check_password_hash(user["password"], password)