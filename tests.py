import server
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient


class TripPlannerUserTestCase(unittest.TestCase):
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

    # _______________________USER TEST CASES_______________________
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
        self.assertEqual(response_validate.data.decode("utf-8"), '{"error": "missing fields"}')

    def test_update_a_user(self):

        post = self.app.post('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Eliel Gordon",
                                email="eliel@example.com",
                                password="password"
                                )),
                            content_type='application/json')

        self.assertEqual(post.status_code, 200)
        put = self.app.put('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Fabio",
                                email="fabio@example.com",
                                password="password"
                                )),
                            query_string=dict(email="eliel@example.com"),
                            content_type='application/json')
        self.assertEqual(put.status_code, 200)


        put = self.app.put('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Fabio"
                                )),
                            query_string=dict(email="elie@example.com"),
                            content_type='application/json')
        self.assertEqual(put.status_code, 404)

    def test_user_delete(self):
        email = "eliel@example.com"
        post = self.app.post('/users',
                              headers=None,
                              data=json.dumps(dict(
                                username="Eliel Gordon",
                                email="eliel@example.com",
                                password="password"
                                )),
                              content_type='application/json')

        self.assertEqual(post.status_code, 200)

        deleted = self.app.delete('/users',
                                  headers=None,
                                  query_string=dict(email=email),
                                  content_type='application/json')

        self.assertEqual(deleted.status_code, 200)

        deleted = self.app.delete('/users',
                                  headers=None,
                                  query_string=dict(email=email),
                                  content_type='application/json')

        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(deleted.data.decode("utf-8"), '{"error": "User with email ' + email + ' does not exist"}')

    # _______________________ TRIPS TEST CASES _______________________

    def test_getting_a_trip(self):
        # Post 2 users to database
        self.app.post('/trips',
                      headers=None,
                      data=json.dumps(dict(
                        destination="London, England",
                        completed=False,
                        start_date="Nov 26, 2017",
                        end_date="December 17, 2017",
                        waypoints=[
                            dict(
                                longitude="38.9013833",
                                latitude="-96.6745109"
                            )
                        ],
                        isFavorite=False
                      )),

                      content_type='application/json'
                      )

        response = self.app.get('/trips',
                                query_string=dict(destination="London, England")
                                )
        response = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
