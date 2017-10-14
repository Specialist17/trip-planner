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

    def generateBasicAuthHeader():
        concatString = username + ":" + password
        utf8 = concatString.encode('utf-8')
        base64String = base64.b64encode(utf8)
        finalString = "Basic " + base64String

        return finalString

    # _______________________USER TEST CASES_______________________
    # User tests, fill with test methods
    def test_getting_a_user(self):
        # Post 2 users to database
        self.app.post('/users',
                      headers=None,
                      data=json.dumps(dict(
                                username="Jiripolla",
                                email="jiripolla@example.com",
                                password="password"
                                )),
                      content_type='application/json'
                      )

        # 3 Make a get request to fetch the posted user

        response = self.app.get('/users',
                                query_string=dict(
                                    email="jiripolla@example.com",
                                    password="password"
                                    )
                                )

        response_json = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_fail_post_a_user_with_already_created_email(self):

        post = self.app.post('/users',
                             headers=None,
                             data=json.dumps(dict(
                                username="Antonio",
                                email="antonio@example.com",
                                password="password"
                                )),
                             content_type='application/json')

        self.assertEqual(post.status_code, 201)

        fail_post = self.app.post('/users',
                                  headers=None,
                                  data=json.dumps(dict(
                                    username="Antonio",
                                    email="antonio@example.com",
                                    password="password"
                                  )),
                                  content_type='application/json')

        self.assertEqual(fail_post.status_code, 409)

    def test_post_a_user(self):
        response = self.app.post('/users',
                                 headers=None,
                                 data=json.dumps(dict(
                                    username="el negro",
                                    email="jilipolla@example.com",
                                    password="password"
                                 )),
                                 content_type='application/json'
                                )

        self.assertEqual(response.status_code, 201)

    def test_fail_post_user_missing_fields(self):
        response_validate = self.app.post('/users',
                                          headers=None,
                                          data=json.dumps(dict(
                                            username="Eliel Gordon",
                                          )),
                                          content_type='application/json'
                                          )

        self.assertEqual(response_validate.status_code, 400)
        self.assertEqual(response_validate.data.decode("utf-8"), '{"error": "missing fields"}')

    def test_update_a_user(self):

        post = self.app.post('/users',
                            headers=None,
                            data=json.dumps(dict(
                                username="Papo",
                                email="pipo@example.com",
                                password="password"
                                )),
                            content_type='application/json')

        self.assertEqual(post.status_code, 201)

        put = self.app.put('/users',
                            headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                            data=json.dumps(dict(
                                username="Fabio",
                                email="fabio@example.com",
                                )),
                            query_string=dict(email="pipo@example.com"),
                            content_type='application/json')
        self.assertEqual(put.status_code, 200)

        put = self.app.put('/users',
                            headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                            data=json.dumps(dict(
                                username="Diablo"
                                )),
                            query_string=dict(email="pipo@example.com"),
                            content_type='application/json')
        self.assertEqual(put.status_code, 404)

    def test_fail_get_user(self):
        get_update_user = self.app.get('/users',
                                       headers=None,
                                       query_string=dict(
                                           email="papapapap@example.com",
                                           password="password"
                                           ),
                                       content_type='application/json')
        self.assertEqual(get_update_user.status_code, 404)

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

        self.assertEqual(post.status_code, 201)

        deleted = self.app.delete('/users',
                                  headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                                  query_string=dict(email=email),
                                  content_type='application/json')

        self.assertEqual(deleted.status_code, 200)

        deleted = self.app.delete('/users',
                                  headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                                  query_string=dict(email=email),
                                  content_type='application/json')

        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(
            deleted.data.decode("utf-8"),
            '{"error": "User with email ' + email + ' does not exist"}'
            )

    # _______________________ TRIPS TEST CASES _______________________

    def test_getting_a_trip(self):
        # Post 2 users to database
        post = self.app.post('/trips',
                             headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                             data=json.dumps(dict(
                                destination="London, England",
                                completed=False,
                                start_date="Nov 26, 2017",
                                end_date="December 17, 2017",
                                waypoints=[],
                                isFavorite=False
                              )),

                             content_type='application/json'
                             )

        self.assertEqual(post.status_code, 201)

        response = self.app.get('/trips',
                                headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                                query_string=dict(destination="London, England")
                                )
        self.assertEqual(response.status_code, 200)

    def test_getting_all_trips(self):

        response = self.app.get('/trips',
                                headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='}
                                )
        self.assertEqual(response.status_code, 200)

        boolean = isinstance(json.loads(response.data.decode()), list)
        self.assertTrue(boolean)

    def test_failing_to_get_a_trip(self):
        response = self.app.get('/trips',
                                headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                                query_string=dict(destination="London, Guayanilla")
                                )
        self.assertEqual(response.status_code, 404)

    def test_patching_a_trip(self):

        post = self.app.post('/trips',
                             headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                             data=json.dumps(dict(
                                destination="London, England",
                                completed=False,
                                start_date="Nov 26, 2017",
                                end_date="December 17, 2017",
                                waypoints=[],
                                isFavorite=False
                              )),

                             content_type='application/json'
                             )

        patch = self.app.patch('/trips',
                               headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                               data=json.dumps(dict(
                                waypoints=[
                                    dict(
                                        destination="Spain",
                                        location=[
                                            dict(
                                                longitude="38.9013833",
                                                latitude="-96.6745109"
                                            )
                                        ]
                                    )
                                ]
                               )),
                               query_string=dict(destination="London, England"),
                               content_type='application/json'
                               )

        response = json.loads(patch.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_updating_a_trip(self):

        post = self.app.post('/trips',
                             headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                             data=json.dumps(dict(
                                destination="London, England",
                                completed=False,
                                start_date="Nov 26, 2017",
                                end_date="December 17, 2017",
                                waypoints=[],
                                isFavorite=False
                              )),

                             content_type='application/json'
                             )

        put = self.app.put('/trips',
                           headers={'Authorization': 'Basic cGlwb0BleGFtcGxlLmNvbTpwYXNzd29yZA=='},
                           data=json.dumps(dict(
                                  destination="London, England",
                                  completed=False,
                                  start_date="Nov 26, 2017",
                                  end_date="December 17, 2017",
                                  waypoints=[
                                      dict(
                                          destination="Spain",
                                          location=[
                                              dict(
                                                  longitude="38.9013833",
                                                  latitude="-96.6745109"
                                              )
                                          ]
                                      )
                                  ],
                                  isFavorite=False
                               )),
                           query_string=dict(destination="London, England"),
                           content_type='application/json'
                           )

        # response = json.loads(patch.data.decode())
        self.assertEqual(put.status_code, 200)


    def test_validate_parameters_post_trip(self):
        post = self.app.post('/trips',
                      headers=None,
                      data=json.dumps(dict(
                        destination="Honolulu, Hawaii",
                        waypoints=[],
                        isFavorite=False
                      )),

                      content_type='application/json'
                      )

        self.assertEqual(post.status_code, 400)

    def test_validate_waypoint_parameters(self):
        post = self.app.put('/trips',
                      headers=None,
                      data=json.dumps(dict(
                        waypoints=[
                            dict(
                                location=[
                                    dict(
                                        longitude="38.9013833",
                                        latitude="-96.6745109"
                                    )
                                ]
                            )
                        ],
                      )),

                      content_type='application/json'
                      )

        self.assertEqual(post.status_code, 400)
        self.assertEqual(post.data.decode("utf-8"), '{"error": "missing destination for the waypoint"}')

        post = self.app.put('/trips',
                      headers=None,
                      data=json.dumps(dict(
                        waypoints=[
                            dict(
                                destination="Spain",
                                location=[
                                    dict(
                                        longitude="38.9013833"
                                    )
                                ]
                            )
                        ],
                      )),

                      content_type='application/json'
                      )

        self.assertEqual(post.status_code, 400)
        self.assertEqual(post.data.decode("utf-8"), '{"error": "missing part of the location for the waypoint"}')

    def test_trip_delete(self):
        deleted = self.app.delete('/trips',
                                  headers=None,
                                  query_string=dict(id=""),
                                  content_type='application/json')

        self.assertEqual(deleted.status_code, 200)


    def test_fail_trip_delete(self):
        deleted = self.app.delete('/users',
                                  headers=None,
                                  query_string=dict(id=""),
                                  content_type='application/json')

        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(deleted.data.decode("utf-8"), '{"error": "trip with id ... does not exist"}')


if __name__ == '__main__':
    unittest.main()
