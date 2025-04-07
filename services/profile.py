# This file was created with some help from Chat GPT.

class Profile:
    """
    Represents a user's profile in the Roommate Finder App.
    Includes profile details, preferences, and methods for managing profile updates.
    """

    # Constructor
    def __init__(self, name, profile_picture, preferences, dealbreakers, bio, looking_status):
        self.name = name
        self.profile_picture = profile_picture
        self.preferences = preferences
        self.dealbreakers = dealbreakers
        self.bio = bio
        self.looking_status = looking_status

    # Setters
    def update_profile(self, name=None, profile_picture=None, bio=None):
        if name:
            self.name = name
        if profile_picture:
            self.profile_picture = profile_picture
        if bio:
            self.bio = bio
        print("Profile updated successfully.")

    # Setters for the preferences and dealbreakers
    def update_preferences(self, new_preferences, new_dealbreakers=None):
        self.preferences.update(new_preferences)
        if new_dealbreakers:
            self.dealbreakers.update(new_dealbreakers)
        print("Preferences updated successfully.")

    # Make a
    def view_profile(self):
        profile_info = {
            "Name": self.name,
            "Profile Picture": self.profile_picture,
            "Preferences": self.preferences,
            "Dealbreakers": self.dealbreakers,
            "Bio": self.bio,
            "Looking for Roommate": self.looking_status
        }
        return profile_info # returns a dict that we will jsonify

    def update_status(self, new_status):
        if isinstance(new_status, bool):
            self.looking_status = new_status
            print(f"Looking status updated to {self.looking_status}.")
        else:
            print("Invalid status value. Must be a boolean.")
