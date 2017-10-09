from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from flask.views import MethodView
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
# import User


app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
app.bcrypt_rounds = 12
api = Api(app)


# Write Resources here
class User(Resource):

    def post(self):
        user_col = app.db.users
        json = request.json
        print(json)
        if 'username' in json and 'email' in json and 'password' in json:
            user = user_col.find_one({
                'email': json['email']
            })
            if user:
                return ({'error': 'user already exists'}, 409, None)
            app.db.users.insert_one(json)
            return (json, 201, None)
        elif 'username' in json and 'password' in json:
                return ({'error': 'no email was specified'}, 400, None)
        elif 'username' not in json or 'email' not in json or 'password' not in json:
                return ({'error': 'missing fields'}, 400, None)
        else:
            print("no se posteó ná")
            return (None, 400, "Hola negro que pajó?")

    def get(self):
        """Tamo xoticos"""
        user_email = request.args.get('email')

        if user_email is None:
            return ({'error': 'no email parameter'}, 404, None)

        user_col = app.db.users

        user = user_col.find_one({
            'email': user_email
        })

        if not user:
            return ({'error': 'User with email ' + user_email + " does not exist"}, 404, None)
        else:
            return (user, 200, None)

    def put(self):
        user_email = request.args.get('email')
        username = request.json.get('username')
        json = request.json
        print(user_email)

        if user_email is None:
            return ({'error': 'no specified email for user'}, 404, None)

        user_col = app.db.users

        user = user_col.find_one({
            'email': user_email
        })
        print(user)

        if user is not None:
            if 'username' in json:
                user['username'] = username

            if 'email' in json:
                user['email'] = json['email']

            user_col.save(user)
            return (user, 200, None)

        return ({'error': 'no user with that email found'}, 404, None)

    def delete(self):
        user_col = app.db.users
        email = request.args.get('email')
        user_to_delete = user_col.find_one({
            'email': email
        })
        if user_to_delete is None:
            return ({'error': 'User with email ' + email + " does not exist"}, 404, None)

        user_col.remove(user_to_delete)
        return ({'deleted': 'User with email ' + email + " has been deleted"}, 200, None)


class Trip(Resource):
    def get(self):
        """Get a trip. If no parameter was specified, then get all trips"""
        args = request.args
        trips_col = app.db.trips

        if 'destination' in args or 'start_date' in args:
            trip_destination = args.get('destination')
            trip_start_date = args.get('start_date')
            trip = trips_col.find_one({
                'destination': trip_destination
            })
            if trip is None:
                return ({'error': 'no trip found'}, 404, None)

            return (trip, 200, None)

        trips = trips_col.find()
        trips_arr = []
        for trip in trips:
            trips_arr.append(trip)

        return (trips_arr, 200, None)

    def post(self):
        trips_col = app.db.trips
        json = request.json
        print(json)

        if 'destination' not in json and 'start_date' not in json:
            return ({'error': 'missing required fields'}, 400, None)
        else:
            trips_col.insert_one(json)
            return (json, 201, None)


# Add api routes here
api.add_resource(User, '/users')
api.add_resource(Trip, '/trips')


#  Custom JSON serializer for flask_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request
    # related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
