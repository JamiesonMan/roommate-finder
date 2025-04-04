from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from werkzeug.security import generate_password_hash, check_password_hash #for hashing the password for database storage
import csv
import os
from services.account_creation import AccountCreationForm, username_or_email_exists, get_next_user_id, enter_user_to_database 
from services.login import username_exists, get_userID, checkPassword
from services.roommatePreferences import roommatePreferences, preferenceForm, load_preferences
import pickle #using to keep objects across different Pages
from profile import Profile
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

csrf = CSRFProtect(app)

# Ensure static directory exists for profile pictures
    # Eventually should be localized data or stored in db
os.makedirs("static/profile_pictures", exist_ok=True)

# Example data that we can plug in.
profile = Profile(
    name="Jamieson Mansker",
    profile_picture="",
    preferences={},
    dealbreakers={},
    bio="",
    looking_status=True
)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if username_exists(username):
                if checkPassword(get_userID(username), password):
                    userID = get_userID(username)
                    userPref = roommatePreferences(userID=userID, username=username)
                    session["user"] = pickle.dumps({
                    "userPref": userPref,
                    "userName": username
                    })
                    print(userPref.__dict__)
                    return redirect(url_for("dashboard"))
                else:
                    flash("Password incorrect", "error")
            else:
                flash("Unregistered user", "error")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:

        user = pickle.loads(session["user"])
        username = user["userName"]

        return render_template("dashboard.html", username=username)
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
        return redirect(url_for('login'))  #Redirect after successful creation to homepage, (should take user to login page if thats not the homepage)(decided to redirect them to preference page so that they would have to fill that out once they create an account can change later)

    return render_template('account_creation.html', form=form)

@app.route('/preferences', methods = ['GET', 'POST'])
def prefPage():
        form = preferenceForm()

        if "user"in session: 

            user = pickle.loads(session["user"])
            userPref = user["userPref"]

            if form.validate_on_submit():
                print("Allergy score:", form.allergy_score.data)
                print("Allergy status:", form.allergy_status.data)
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
                print(userPref.__dict__)
                userPref.updatePreferences(quiet_score, location_status, location_score, dorm_status, dorm_score, 
                                        animal_status, animal_score, visitor_status, 
                                        cleanliness_score, bed_time, drinking_status, smoking_status, 
                                        smoking_score, drinking_score, visitor_score, bedtime_score, 
                                        allergy_status, allergy_score)
                print(userPref.__dict__)
                return redirect(url_for("dashboard"))
            return render_template('roommatePreferences.html', form=form)
        else:
            return render_template('login.html')


@app.route('/profile_page')
def profile_page():
    return render_template('profile-page.html')

# /update_profile, you can only POST to not fetch.
@app.route('/update_profile', methods=['POST'])
def update_profile():
    name = request.form.get('name')
    bio = request.form.get('bio')
    looking_status = request.form.get('lookingStatus') == 'true'

    profile_picture = request.files.get('profilePicture')
    # Uses OS library to create a static folder and put a copy of the selected profile picture in.
    if profile_picture:
        image_path = os.path.join('static', 'profile_pictures', profile_picture.filename)
        profile_picture.save(image_path)
        profile.update_profile(name=name, profile_picture=image_path, bio=bio)
    else:
        profile.update_profile(name=name, bio=bio)

    profile.update_status(looking_status)

    return jsonify({"message": "Profile updated successfully!"})

@app.route('/profile_info')
def profile_info():
    return render_template('profile-display.html')

@app.route('/view_profile')
def view_profile():
    profile_data = profile.view_profile()  # Uses the view_profile() method in Profile class
    return jsonify(profile_data) # Turns the profile_data into JSON format.

@app.route('/profile_feed')
def view_feed():
    user = pickle.loads(session["user"])
    current_user_pref = user["userPref"]
    dict_all_users_prefs = load_preferences("userPreferences.csv") #a list of dictionaries
    profile_feed = [] #list that will act as feed list of profiles

    for person in dict_all_users_prefs:
        if person["userID"] != str(current_user_pref.userID):
            other_user = roommatePreferences(userID=person["userID"])
            compatability_score = current_user_pref.compute_compatability(other_user)
            profile_feed.append({
                "userID": person["userID"],
                "score": compatability_score,
                "username": person["username"],
                "preferences": other_user,
                #stopping here for now, will add profile pics/user bios next sprint
            })

    sort_by = request.args.get("sort", "score")  #grabs sort type from URL, score is default if user doesnt specify

    if sort_by == "score":
        feed = sorted(profile_feed, key=lambda x: x["score"], reverse=True) #sorts pref dict by compute compatability descending
    elif sort_by == "newest":
        feed = sorted(profile_feed, key=lambda x: int(x["userID"]), reverse=True) #sorts dict by ID descending, IDs are given incrementally so it = newest profiles 1st
    elif sort_by == "random":
        feed = profile_feed.copy()
        random.shuffle(feed)

    index = int(request.args.get("index", 0)) #for URL indexing for arrow key buttons to go next/prev profile
    num_profiles = len(feed)

    #limiting URL index between 0 and total profiles minus self
    index = max(0, min(index, num_profiles - 1))

    current_profile = feed[index]

    return render_template("profile_feed.html", user=current_profile, index=index, total=len(feed)) #jinja

       

if __name__ == "__main__":
    app.run()
    