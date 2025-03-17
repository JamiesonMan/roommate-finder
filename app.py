from flask import Flask, render_template, request, jsonify
from profile import Profile
import os

app = Flask(__name__)

# Ensure static directory exists for profile pictures
os.makedirs("static/profile_pictures", exist_ok=True)

# Example data
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

@app.route('/profile_page')
def profile_page():
    return render_template('profile-page.html')

@app.route('/update_profile', methods=['POST'])
def update_profile():
    name = request.form.get('name')
    bio = request.form.get('bio')
    looking_status = request.form.get('lookingStatus') == 'true'

    # Handle profile picture upload
    profile_picture = request.files.get('profilePicture')
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
    profile_data = profile.view_profile()  # Uses the `view_profile()` method in Profile class
    return jsonify(profile_data)

if __name__ == "__main__":
    app.run(debug=True)
