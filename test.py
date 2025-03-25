import unittest
from services.roommatePreferences import roommatePreferences
from datetime import datetime, timedelta

class TestRoommatePreferences(unittest.TestCase):
    

    def setUp(self):
        self.user1 = roommatePreferences(quiet_score=3, location_status='near', location_score=2, dorm_status='yes', dorm_score=3,
            animal_status='yes', animal_score=4, visitor_status='no', cleanliness_score=2, 
            bed_time=datetime(2023, 1, 1, 22, 0), drinking_status='no', smoking_status='no', smoking_score=3,
            drinking_score=2, visitor_score=1, bedtime_score=4, allergy_status='yes', allergy_score='yes')
        
        self.user2 = roommatePreferences(quiet_score=4, location_status='near', location_score=2, dorm_status='yes', dorm_score=2,
            animal_status='no', animal_score=1, visitor_status='yes', cleanliness_score=3, 
            bed_time=datetime(2023, 1, 1, 23, 0), drinking_status='yes', smoking_status='yes', smoking_score=5,
            drinking_score=0, visitor_score=3, bedtime_score=3, allergy_status='no', allergy_score='yes')
        
        self.user3 = roommatePreferences(quiet_score=4, location_status='near', location_score=2, dorm_status='yes', dorm_score=2,
            animal_status='no', animal_score=1, visitor_status='yes', cleanliness_score=3, 
            bed_time=datetime(2023, 1, 1, 23, 0), drinking_status='yes', smoking_status='yes', smoking_score=5,
            drinking_score=0, visitor_score=3, bedtime_score=3, allergy_status='no', allergy_score='no')
        
    def test_compute_compatibility(self):
        self.assertEqual((self.user1.compute_compatability(self.user2)), 72)

    def test_compute_compatibility_no_allergy_match(self):
        self.assertEqual((self.user1.compute_compatability(self.user3)), 0)

if __name__ == "__main__":
    unittest.main()