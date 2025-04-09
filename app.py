
from flask_socketio import SocketIO, emit, join_room, leave_room
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
from services.roommatePreferences import roommatePreferences, preferenceForm
import pickle #using to keep objects across different Pages
from services.Inbox import Message, Chat, load_messages_from_csv
from profile import Profile


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
socketio = SocketIO(app, cors_allowed_origins="*")

csrf = CSRFProtect(app)

chats = {}

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
                    session["user"] = username
                    userID = get_userID(username)
                    userPref = roommatePreferences(userID)
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

@app.route('/inbox')
def inbox():
     if "user" in session:

        user = pickle.loads(session["user"])
        username = user["userName"]

        load_messages_from_csv("messages.csv", chats)

        return render_template('inbox.html', username=username, chats=chats.values())
     else:
        return redirect(url_for("login"))

@app.route('/new_chat', methods=['GET', 'POST'])
def new_chat():
    if "user" in session:

        user = pickle.loads(session["user"])
        username = user["userName"]

        if request.method == 'POST':
            recipient = request.form.get('recipient')
            
            if username_exists(recipient):
                chatID = len(chats) + 1
                new_chat = Chat(chatID=chatID, user1=username, user2=recipient, messages=[])
                chats[chatID] = new_chat

                return redirect(url_for('chat_messages', chatID=chatID))

        return render_template('newChat.html', username=username)
    else:
        return redirect(url_for("login"))

@app.route('/chat_messages/<chatID>', methods = ['GET', 'POST'])
def chat_messages(chatID):
     if "user" in session:
        user = pickle.loads(session["user"])
        username = user["userName"]

        for chat in chats.values():
            if chat.chatID == int(chatID):
               if chat.user1 == username:
                    receiver = chat.user2
                    break
               else:
                   receiver = chat.user1
                   break
               
        messages_dict = [msg.to_dict() for msg in chat.messages]

        return render_template('chat.html', username=username, chatID=chatID, otherUser=receiver, messages=messages_dict)
     else:
        return redirect(url_for("login"))    

@socketio.on('join')
def on_join(data):
    chatID = data['chatID']
    join_room(int(chatID))

@socketio.on('message')
def handle_message(data):

        chatID = int(data['chatID'])
        sender = data['sender']
        receiver = data['receiver']
        messageContents = data['message']

        if chatID not in chats:
            chats[chatID] = Chat(chatID, sender, receiver)

        new_message = chats[chatID].newMessage(messageContents, sender)
        
        with open("messages.csv", mode='a', newline='', encoding='utf-8') as file: 
            fieldnames = ['chatID', 'messageID', 'messageContents', 'sender', 'receiver', 'timeSent']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if os.stat("messages.csv").st_size == 0:
                writer.writeheader()
            writer.writerow({
                            'chatID': new_message.chatID,
                            'messageID': new_message.messageID,
                            'messageContents': new_message.messageContents,
                            'sender': new_message.sender,
                            'receiver': new_message.receiver,  # Fix typo if necessary
                            'timeSent': new_message.timeSent.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
                        })


        emit('receive_message', {
        "chatID": chatID,
        "sender": sender,
        "messageContents": messageContents
        }, room=chatID)      


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

if __name__ == "__main__":
    socketio.run(app)
