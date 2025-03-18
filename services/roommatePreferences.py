from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import TimeField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

#class to hold user preference information while logged in for easy acess and calculations
class roommatePreferences:
    #iconstructor for the Preferences Class. Will add userID attribute once account creation is done
    def __init__(self, userID = "0000", quiet_score=0, location_status="empty", location_score=0, dorm_status="empty", dorm_score=0, animal_status="empty", animal_score=0, visitor_status="empty", cleanliness_score="empty", bed_time="0:00", drinking_status="no", smoking_status="no", smoking_score=0, drinking_score=0, visitor_score=0, bedtime_score=0, allergy_status="no", allergy_score=0):
        self.userID = userID
        self.cleanliness_score = cleanliness_score
        self.bed_time = bed_time
        self.drinking_status = drinking_status
        self.smoking_status = smoking_status
        self.smoking_score = smoking_score
        self.drinking_score = drinking_score
        self.visitor_status = visitor_status
        self.visitor_score = visitor_score
        self.bedtime_score = bedtime_score
        self.allergy_status = allergy_status
        self.allergy_score = allergy_score
        self.animal_status = animal_status
        self.animal_score = animal_score
        self.dorm_status = dorm_status
        self.dorm_score = dorm_score
        self.location_status = location_status
        self.location_score = location_score
        self.quiet_score = quiet_score

    def updatePreferences(self, quiet_score, location_status, location_score, dorm_status, dorm_score, animal_status, animal_score, visitor_status, cleanliness_score, bed_time, drinking_status, smoking_status, smoking_score, drinking_score, visitor_score, bedtime_score, allergy_status, allergy_score):
            self.cleanliness_score = cleanliness_score
            self.bed_time = bed_time
            self.drinking_status = drinking_status
            self.smoking_status = smoking_status
            self.smoking_score = smoking_score
            self.drinking_score = drinking_score
            self.visitor_status = visitor_status
            self.visitor_score = visitor_score
            self.bedtime_score = bedtime_score
            self.allergy_status = allergy_status
            self.allergy_score = allergy_score
            self.animal_status = animal_status
            self.animal_score = animal_score
            self.dorm_status = dorm_status
            self.dorm_score = dorm_score
            self.location_status = location_status
            self.location_score = location_score
            self.quiet_score = quiet_score

    #computes two users compatability
    def compute_compatability(self, user2):
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
      if(self.allergy_comparison(user2) == 0):
          compatability_score = 0
      elif():
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
        self_bed_time = datetime.combine(today, self.bed_time.time())
        user2_bed_time = datetime.combine(today, user2.bed_time.time())
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
        compatability_score = 0
        if((self.allergy_status == user2.allergy_score) or (user2.allergy_status == self.allergy_score)):
            compatability_score += 5
        return compatability_score

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
        location_status = SelectField('Which location do you prefer to live in?', choices=[("", "Select an option"), ('northside', 'Northside'), ('southside', 'Southside')], validators=[DataRequired()])
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