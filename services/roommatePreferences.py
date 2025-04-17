from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import TimeField, SelectField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange
import csv

#class to hold user preference information while logged in for easy acess and calculations
class roommatePreferences:
    #constructor for the Preferences Class.
    def __init__(self, userID=0, username=None, quiet_score=0, location_status="empty", location_score=0, 
             dorm_status="empty", dorm_score=0, animal_status="empty", animal_score=0, 
             visitor_status="empty", cleanliness_score="empty", bed_time="0:00", 
             drinking_status="no", smoking_status="no", smoking_score=0, 
             drinking_score=0, visitor_score=0, bedtime_score=0, 
             allergy_status="no", allergy_score="no"):

        self.userID = userID
        self.username = username
        userPref = load_preferences("userPreferences.csv")

        found = self.find_user(userPref)
        if found:
            self.updatePreferences(
                int(found["quiet_score"]),
                found["location_status"],
                int(found["location_score"]),
                found["dorm_status"],
                int(found["dorm_score"]),
                found["animal_status"],
                int(found["animal_score"]),
                found["visitor_status"],
                int(found["cleanliness_score"]),
                datetime.strptime(found["bed_time"], "%H:%M:%S").time(),
                found["drinking_status"],
                found["smoking_status"],
                int(found["smoking_score"]),
                int(found["drinking_score"]),
                int(found["visitor_score"]),
                int(found["bedtime_score"]),
                found["allergy_status"],
                found["allergy_score"],
                found["username"] )
        
        elif cleanliness_score != "empty":
            self.updatePreferences(int(quiet_score), location_status, int(location_score),
                dorm_status, int(dorm_score), animal_status, int(animal_score),
                visitor_status, int(cleanliness_score), bed_time,
                drinking_status, smoking_status, int(smoking_score),
                int(drinking_score), int(visitor_score), int(bedtime_score),
                allergy_status, allergy_score, username)
        else:
            #default values to prevent crashing
            self.quiet_score = 0
            self.location_status = location_status
            self.location_score = 0
            self.dorm_status = dorm_status
            self.dorm_score = 0
            self.animal_status = animal_status
            self.animal_score = 0
            self.visitor_status = visitor_status
            self.visitor_score = 0
            self.cleanliness_score = 0
            self.bed_time = bed_time
            self.drinking_status = drinking_status
            self.drinking_score = 0
            self.smoking_status = smoking_status
            self.smoking_score = 0
            self.bedtime_score = 0
            self.allergy_status = allergy_status
            self.allergy_score = allergy_score




    #The old constructor was messing stuff up with func/database integration and was writting even when reading from db was desired
    def load_pref_data(self):
        userPref = load_preferences("userPreferences.csv")
        for pref in userPref:
            if str(pref.get("userID")) == str(self.userID):
                self.quiet_score = int(pref["quiet_score"])
                self.location_status = pref["location_status"]
                self.location_score = int(pref["location_score"])
                self.dorm_status = pref["dorm_status"]
                self.dorm_score = int(pref["dorm_score"])
                self.animal_status = pref["animal_status"]
                self.animal_score = int(pref["animal_score"])
                self.visitor_status = pref["visitor_status"]
                self.cleanliness_score = int(pref["cleanliness_score"])
                self.bed_time = datetime.strptime(pref["bed_time"], "%H:%M:%S").time()
                self.drinking_status = pref["drinking_status"]
                self.smoking_status = pref["smoking_status"]
                self.smoking_score = int(pref["smoking_score"])
                self.drinking_score = int(pref["drinking_score"])
                self.visitor_score = int(pref["visitor_score"])
                self.bedtime_score = int(pref["bedtime_score"])
                self.allergy_status = pref["allergy_status"]
                self.allergy_score = pref["allergy_score"]
                return

        #No user found, use default values
        self.quiet_score = 0
        self.location_status = "empty"
        self.location_score = 0
        self.dorm_status = "empty"
        self.dorm_score = 0
        self.animal_status = "empty"
        self.animal_score = 0
        self.visitor_status = "empty"
        self.cleanliness_score = 0
        self.bed_time = datetime.strptime("00:00:00", "%H:%M:%S").time()
        self.drinking_status = "no"
        self.smoking_status = "no"
        self.smoking_score = 0
        self.drinking_score = 0
        self.visitor_score = 0
        self.bedtime_score = 0
        self.allergy_status = "no"
        self.allergy_score = "no"

        


    def updatePreferences(self, quiet_score, location_status, location_score, dorm_status, dorm_score, animal_status, animal_score, visitor_status, cleanliness_score, bed_time, drinking_status, smoking_status, smoking_score, drinking_score, visitor_score, bedtime_score, allergy_status, allergy_score, username=None):
            userPref = load_preferences("userPreferences.csv")
            self.cleanliness_score = int(cleanliness_score)
            self.bed_time = bed_time
            self.drinking_status = drinking_status
            self.smoking_status = smoking_status
            self.smoking_score = int(smoking_score)
            self.drinking_score = int(drinking_score)
            self.visitor_status = visitor_status
            self.visitor_score = int(visitor_score)
            self.bedtime_score = int(bedtime_score)
            self.allergy_status = allergy_status
            self.allergy_score = allergy_score
            self.animal_status = animal_status
            self.animal_score = int(animal_score)
            self.dorm_status = dorm_status
            self.dorm_score = int(dorm_score)
            self.location_status = location_status
            self.location_score = int(location_score)
            self.quiet_score = int(quiet_score)
            self.username = username
            self.update_user(userPref)

    #computes two users compatability
    def compute_compatability(self, user2):
        #dealbreaker if allergies dont match
        if self.allergy_comparison(user2) == 0:
            return 0  
    
        compatability_score = 0
        compatability_score += self.quiet_comparison(user2)
        compatability_score += self.location_comparison(user2)
        compatability_score += self.dorm_comparison(user2)
        compatability_score += self.animal_comparison(user2)
        compatability_score += self.bedtime_comparison(user2)
        compatability_score += self.visitor_comparison(user2)
        compatability_score += self.smoking_comparison(user2)
        compatability_score += self.drinking_comparison(user2)
        compatability_score += self.cleanliness_comparison(user2)
        compatability_score += 5  

        compatability_score = (compatability_score/50) * 100 
        return compatability_score


    # all of the following methods are used to compare two users answers to each preference
    def quiet_comparison(self, user2):
        compatability_score = 0
        if(self.quiet_score == user2.quiet_score):
            compatability_score += 5
        elif(abs(self.quiet_score - user2.quiet_score) == 5):
            compatability_score +=0
        elif(abs(self.quiet_score - user2.quiet_score) == 4):
            compatability_score +=1
        elif(abs(self.quiet_score - user2.quiet_score) == 3):
            compatability_score +=2
        elif(abs(self.quiet_score - user2.quiet_score) == 3):
            compatability_score +=2
        elif(abs(self.quiet_score - user2.quiet_score) == 1):
            compatability_score +=4
        return compatability_score

    def location_comparison(self, user2):
        compatability_score = 0
        if(self.location_status == user2.location_status):
            compatability_score += 5
        elif((user2.location_score == 5) or (self.location_score == 5)):
            compatability_score +=0
        elif((user2.location_score == 4) or (self.location_score == 4)):
            compatability_score +=1
        elif((user2.location_score == 3) or (self.location_score == 3)):
            compatability_score +=2
        elif((user2.location_score == 2) or (self.location_score == 2)):
            compatability_score +=3
        elif((user2.location_score == 1) or (self.location_score == 1)):
            compatability_score +=4
        elif((user2.location_score == 0) or (self.location_score == 0)):
            compatability_score +=5
        return compatability_score

    def dorm_comparison(self, user2):
        compatability_score = 0
        if(self.dorm_status == user2.dorm_status):
            compatability_score += 5
        elif((user2.dorm_score == 5) or (self.dorm_score == 5)):
            compatability_score +=0
        elif((user2.dorm_score == 4) or (self.dorm_score == 4)):
            compatability_score +=1
        elif((user2.dorm_score == 3) or (self.dorm_score == 3)):
            compatability_score +=2
        elif((user2.dorm_score == 2) or (self.dorm_score == 2)):
            compatability_score +=3
        elif((user2.dorm_score == 1) or (self.dorm_score == 1)):
            compatability_score +=4
        elif((user2.dorm_score == 0) or (self.dorm_score == 0)):
            compatbality_score +=5
        return compatability_score

    def animal_comparison(self, user2):
        compatability_score = 0
        if(self.animal_status == user2.animal_status):
            compatability_score += 5
        elif((self.animal_status == 'yes' and user2.animal_score == 5) or (user2.animal_status == 'yes' and self.animal_score == 5)):
            compatability_score +=0
        elif((self.animal_status == 'yes' and user2.animal_score == 4) or (user2.animal_status == 'yes' and self.animal_score == 4)):
            compatability_score +=1
        elif((self.animal_status == 'yes' and user2.animal_score == 3) or (user2.animal_status == 'yes' and self.animal_score == 3)):
            compatability_score +=2
        elif((self.animal_status == 'yes' and user2.animal_score == 2) or (user2.animal_status == 'yes' and self.animal_score == 2)):
            compatability_score +=3
        elif((self.animal_status == 'yes' and user2.animal_score == 1) or (user2.animal_status == 'yes' and self.animal_score == 1)):
            compatability_score +=4
        elif((self.animal_status == 'yes' and user2.animal_score == 0) or (user2.animal_status== 'yes' and self.animal_score == 0)):
            compatability_score +=5
        return compatability_score
        
    def bedtime_comparison(self, user2):
        today = datetime.today()
        #Changing time for string in CSV to datetime 
        if isinstance(self.bed_time, str):
            self.bed_time = datetime.strptime(self.bed_time.strip(), "%H:%M:%S").time()
        if isinstance(user2.bed_time, str):
            user2.bed_time = datetime.strptime(user2.bed_time.strip(), "%H:%M:%S").time()

        self_bed_time = datetime.combine(today, self.bed_time)
        user2_bed_time = datetime.combine(today, user2.bed_time)

        compatability_score = 0
        if(abs(self_bed_time - user2_bed_time) <= timedelta(hours=1)):
            compatability_score += 5
        elif((abs(self_bed_time - user2_bed_time)  >= timedelta(hours = 1))) and (self.bedtime_score == 5 or user2.bedtime_score == 5):
            compatability_score += 0
        elif((abs(self_bed_time - user2_bed_time)  >= timedelta(hours = 1))) and (self.bedtime_score == 4 or user2.bedtime_score == 4):
            compatability_score += 1
        elif((abs(self_bed_time - user2_bed_time)  >= timedelta(hours = 1))) and (self.bedtime_score == 3 or user2.bedtime_score == 3):
            compatability_score += 2
        elif((abs(self_bed_time - user2_bed_time)  >= timedelta(hours = 1))) and (self.bedtime_score == 2 or user2.bedtime_score == 2):
            compatability_score += 3
        elif((abs(self_bed_time - user2_bed_time)  >= timedelta(hours = 1))) and (self.bedtime_score == 1 or user2.bedtime_score == 1):
            compatability_score += 4
        elif((abs(self_bed_time - user2_bed_time)  >= timedelta(hours = 1))) and (self.bedtime_score == 0 or user2.bedtime_score == 0):
            compatability_score += 5
        return compatability_score 

    def allergy_comparison(self, user2):
    #If allergy info doesnt match/wont accommodate return 0, else return 5
        if (self.allergy_status == "yes" and user2.allergy_score == "no") or (user2.allergy_status == "yes" and self.allergy_score == "no"):
            return 0
        return 5

    def visitor_comparison(self, user2):
        compatability_score = 0
        if(self.visitor_status == user2.visitor_status):
            compatability_score += 5
        elif((self.visitor_status == 'yes' and user2.visitor_score == 5) or (user2.visitor_status == 'yes' and self.visitor_score == 5)):
            compatability_score +=0
        elif((self.visitor_status == 'yes' and user2.visitor_score == 4) or (user2.visitor_status == 'yes' and self.visitor_score == 4)):
            compatability_score +=1
        elif((self.visitor_status == 'yes' and user2.visitor_score == 3) or (user2.visitor_status == 'yes' and self.visitor_score == 3)):
            compatability_score +=2
        elif((self.visitor_status == 'yes' and user2.visitor_score == 2) or (user2.visitor_status == 'yes' and self.visitor_score == 2)):
            compatability_score +=3
        elif((self.visitor_status == 'yes' and user2.visitor_score == 1) or (user2.visitor_status == 'yes' and self.visitor_score == 1)):
            compatability_score +=4
        elif((self.visitor_status == 'yes' and user2.visitor_score == 0) or (user2.visitor_status == 'yes' and self.visitor_score == 0)):
            compatability_score +=5
        return compatability_score

    def smoking_comparison(self, user2):
        compatability_score = 0
        if(self.smoking_status == user2.smoking_status):
            compatability_score += 5
        elif((self.smoking_status == 'yes' and user2.smoking_score == 5) or (user2.smoking_status == 'yes' and self.smoking_score == 5)):
            compatability_score +=0
        elif((self.smoking_status == 'yes' and user2.smoking_score == 4) or (user2.smoking_status == 'yes' and self.smoking_score == 4)):
            compatability_score +=1
        elif((self.smoking_status == 'yes' and user2.smoking_score == 3) or (user2.smoking_status == 'yes' and self.smoking_score == 3)):
            compatability_score +=2
        elif((self.smoking_status == 'yes' and user2.smoking_score == 2) or (user2.smoking_status == 'yes' and self.smoking_score == 2)):
            compatability_score +=3
        elif((self.smoking_status == 'yes' and user2.smoking_score == 1) or (user2.smoking_status == 'yes' and self.smoking_score == 1)):
            compatability_score +=4
        elif((self.smoking_status == 'yes' and user2.smoking_score == 0) or (user2.smoking_status== 'yes' and self.smoking_score == 0)):
            compatability_score +=5
        return compatability_score

    def drinking_comparison(self, user2):
        compatability_score = 0
        if(self.drinking_status == user2.drinking_status):
            compatability_score += 5
        elif((self.drinking_status == 'yes' and user2.drinking_score == 5) or (user2.drinking_status == 'yes' and self.drinking_score == 5)):
            compatability_score +=0
        elif((self.drinking_status == 'yes' and user2.drinking_score == 4) or (user2.drinking_status == 'yes' and self.drinking_score == 4)):
            compatability_score +=1
        elif((self.drinking_status == 'yes' and user2.drinking_score == 3) or (user2.drinking_status == 'yes' and self.drinking_score == 3)):
            compatability_score +=2
        elif((self.drinking_status == 'yes' and user2.drinking_score == 2) or (user2.drinking_status == 'yes' and self.drinking_score == 2)):
            compatability_score +=3
        elif((self.drinking_status == 'yes' and user2.drinking_score == 1) or (user2.drinking_status == 'yes' and self.drinking_score == 1)):
            compatability_score +=4
        elif((self.drinking_status == 'yes' and user2.drinking_score == 0) or (user2.drinking_status == 'yes' and self.drinking_score == 0)):
            compatability_score +=5
        return compatability_score
        
    def cleanliness_comparison(self, user2):
        compatability_score = 0
        if(self.cleanliness_score == user2.cleanliness_score):
            compatability_score += 5
        elif(abs(self.cleanliness_score - user2.cleanliness_score) == 1):
            compatability_score +=4
        elif(abs(self.cleanliness_score - user2.cleanliness_score) == 2):
            compatability_score +=3
        elif(abs(self.cleanliness_score - user2.cleanliness_score) == 3):
            compatability_score +=2
        elif(abs(self.cleanliness_score - user2.cleanliness_score) == 4):
            compatability_score +=1
        elif(abs(self.cleanliness_score - user2.cleanliness_score) == 5):
            compatability_score +=0
        return compatability_score

    def find_user(self, userPreferences):
        for pref in userPreferences:
            if pref.get("userID") == self.userID:
                return pref
        return None
    
    def update_user(self, userPreferences):
        user_found = False
        # if user in database already, update row if prefernces change, else append new user's prefs to new row in db
        for pref in userPreferences:
            if str(pref.get("userID")) == str(self.userID):
                user_found = True
                pref["username"] = self.username
                pref["quiet_score"] = int(self.quiet_score)
                pref["location_status"] = self.location_status
                pref["location_score"] = int(self.location_score)
                pref["dorm_status"] = self.dorm_status
                pref["dorm_score"] = int(self.dorm_score)
                pref["animal_status"] = self.animal_status
                pref["animal_score"] = int(self.animal_score)
                pref["visitor_status"] = self.visitor_status
                pref["cleanliness_score"] = int(self.cleanliness_score)
                pref["bed_time"] = self.bed_time
                pref["drinking_status"] = self.drinking_status
                pref["smoking_status"] = self.smoking_status
                pref["smoking_score"] = int(self.smoking_score)
                pref["drinking_score"] = int(self.drinking_score)
                pref["visitor_score"] = int(self.visitor_score)
                pref["bedtime_score"] = int(self.bedtime_score)
                pref["allergy_status"] = self.allergy_status
                pref["allergy_score"] = self.allergy_score
                break

        if not user_found:
            userPreferences.append({
                "userID": self.userID,
                "username": self.username,
                "quiet_score": int(self.quiet_score),
                "location_status": self.location_status,
                "location_score": int(self.location_score),
                "dorm_status": self.dorm_status,
                "dorm_score": int(self.dorm_score),
                "animal_status": self.animal_status,
                "animal_score": int(self.animal_score),
                "visitor_status": self.visitor_status,
                "cleanliness_score": int(self.cleanliness_score),
                "bed_time": self.bed_time,
                "drinking_status": self.drinking_status,
                "smoking_status": self.smoking_status,
                "smoking_score": int(self.smoking_score),
                "drinking_score": int(self.drinking_score),
                "visitor_score": int(self.visitor_score),
                "bedtime_score": int(self.bedtime_score),
                "allergy_status": self.allergy_status,
                "allergy_score": self.allergy_score
            })

        self.save_preferences(userPreferences, "userPreferences.csv")



    def save_preferences(self, userPreferences, file):
        with open(file, mode='w', newline='') as csvfile:
            fieldnames = [
            "userID", "username", "quiet_score", "location_status", "location_score",
            "dorm_status", "dorm_score", "animal_status", "animal_score", "visitor_status",
            "cleanliness_score", "bed_time", "drinking_status", "smoking_status",
            "smoking_score", "drinking_score", "visitor_score", "bedtime_score",
            "allergy_status", "allergy_score" ]
            writer= csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(userPreferences)

    
def load_preferences(filename):
        userPreferences= []
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if any(row.values()):
                    #CSV automatically reads all as string so converting str to int here
                    int_fields = [
                    "quiet_score", "location_score", "dorm_score", "animal_score",
                    "visitor_score", "cleanliness_score", "smoking_score",
                    "drinking_score", "bedtime_score" ]
                
                    for field in int_fields:
                        #check that field exists and is formatted properly (in case someone manually edits csv)
                        if field in row and row[field].strip() != "":
                            row[field] = int(row[field])
                        else:
                            row[field] = 0  #If a field with a score is blank, default to 0 (dont care)

                    userPreferences.append(row)
        return userPreferences

#class for the preferences form to validate form entries uses flask-WTF use pip install Flask-WTF
class preferenceForm(FlaskForm):
        bed_time = TimeField('What time do you plan to go to bed?', validators=[DataRequired()])
        visitor_status = SelectField('Do you plan on having visitors?', choices=[("", "Select an option"), ('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
        drinking_status = SelectField('Do you drink?', choices=[("", "Select an option"), ('yes', 'Yes'), ('no', 'No')])
        smoking_status = SelectField('Do you smoke?', choices=[('yes', 'Yes'), ('no', 'No')])
        animal_status = SelectField('Do you have a pet/service animal?', choices=[("", "Select an option"), ('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
        dorm_status = SelectField('What dorm do you prefer to live in?', choices=
                                  [("", "Select an option"),
                                   ('duncan', 'Community/Duncan Dunn'), 
                                   ('honors', 'Elmina White Honors Hall'),
                                   ('gannon', 'Gannon/Goldsworthy'),
                                   ('global', 'Global Scholars Hall'),
                                   ('mccroskey', 'McCroskey'),
                                   ('northisde', 'Northside'),
                                   ('olympia', 'Olympia'),
                                   ('orton', 'Orton'),
                                   ('regents', 'Regents'),
                                   ('rogers', 'Rogers'),
                                   ('scott', 'Scott/Coman'),
                                   ('stephenson', 'Stephenson Complex'),
                                   ('stimson', 'Stimson'),
                                   ('streit' , 'Streit Perham')],
                                   validators=[DataRequired()])
        location_status = SelectField('Which location do you prefer to live in?', choices=[("", "Select an option"), ('northside', 'Northside'), ('southside', 'Southside'), ('hillside', 'Hillside')], validators=[DataRequired()])
        cleanliness_score = IntegerField('How much do you care about cleanliness?', validators=[NumberRange(min= 0, max= 5)])
        bedtime_score = IntegerField('How much do you care about your rommate going to bed around the same time?', validators=[NumberRange(min= 0, max= 5)])
        visitor_score = IntegerField('Do you care if your roommate has visitors?', validators=[NumberRange(min= 0, max= 5)])
        quiet_score = IntegerField('How much do you care about the room being quiet?', validators=[NumberRange(min= 0, max= 5)])
        drinking_score = IntegerField('How much do you care if your roommate drinks?', validators=[NumberRange(min= 0, max= 5)])
        smoking_score = IntegerField('How much do you care if your roommate smokes?', validators=[NumberRange(min= 0, max= 5)])
        animal_score = IntegerField('How much do you care if your roommate has a pet/service animal?(0 being you are fine with it, 5 you are not fine with it)', validators=[NumberRange(min= 0, max= 5)])
        dorm_score = IntegerField('How much do you care about living in the dorm you prefer?', validators=[NumberRange(min= 0, max= 5)])
        location_score = IntegerField('How much do you care about living in the location you selected?', validators=[NumberRange(min= 0, max= 5)])
        allergy_status = SelectField('Do you have any allergies?', choices=[("", "Select an option"), ('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
        allergy_score = SelectField('Are you ok changing eating or lifestyle habits to accomadate rommates with allergies? e.g. Not eating peanuts for students with peanut allergy.', choices=[("", "Select an option"), ('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
        submit = SubmitField('Submit')

class dealBreakers(FlaskForm):
    bedDealbreaker = BooleanField('Bed Time')
    visDealbreaker = BooleanField('Visitors')
    drinkDealbreaker = BooleanField('Drinking')
    smokeDealbreaker = BooleanField('Smoking')
    aniDealbreaker = BooleanField('Animal')
    dormDealbreaker = BooleanField('Dorm Choice')
    locDealbreaker = BooleanField('Location Choice')
    cleanDealbreaker = BooleanField('Cleanliness')
    quietDealbreaker = BooleanField('Noise')
