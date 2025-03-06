from flask import Flask, render_template, request
from services.roommatePreferences import roommatePreferences, preferenceForm
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

app=Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'

csrf = CSRFProtect(app)

@app.route('/')
def home_page():
    return render_template('index.html')

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

