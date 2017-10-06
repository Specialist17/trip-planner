import server
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient


class TripPlannerTestCase(unittest.TestCase):
    def setUp(self):

        self.app = server.app.test_client()
        # Run app in testing mode to retrieve exceptions and stack traces
        server.app.config['TESTING'] = True

        mongo = MongoClient('localhost', 27017)
        global db

        # Reduce encryption workloads for tests
        server.app.bcrypt_rounds = 4

        db = mongo.trip_planner_test
        server.app.db = db

        db.drop_collection('users')
        db.drop_collection('trips')

    # User tests, fill with test methods
    def test_getting_a_user(self):
        # Post 2 users to database
        self.app.post('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Eliel Gordon",
                                email="eliel@example.com",
                                password="password"
                                )),
                            content_type='application/json')

        # 3 Make a get request to fetch the posted user

        response = self.app.get('/users',
                                query_string=dict(email="eliel@example.com")
                                )

        # Decode reponse
        response_json = json.loads(response.data.decode())

        # Actual test to see if GET request was succesful
        # Here we check the status code
        self.assertEqual(response.status_code, 200)

    def test_post_a_user(self):
        response = self.app.post('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Eliel Gordon",
                                email="eliel@example.com",
                                password="password"
                                )),
                            content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response_validate = self.app.post('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Eliel Gordon",
                                )),
                            content_type='application/json')

        self.assertEqual(response_validate.status_code, 400)
        # self.assertEqual(response_validate.data, {"error": "missing fields"})

    def test_update_a_user(self):
        

if __name__ == '__main__':
    unittest.main()
