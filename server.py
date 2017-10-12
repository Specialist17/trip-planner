from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient, ReturnDocument
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
import pdb
# import User


app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
app.bcrypt_rounds = 12
api = Api(app)


def auth_validation(email, user_password):
    # Find user by email
    user_col = app.db.users
    database_user = user_col.find_one({'email': email})
    db_password = database_user['password']
    password = user_password.encode('utf-8')
    # pdb.set_trace()
    # Check if client password from login matches database password
    if bcrypt.hashpw(password, db_password) == db_password:
        # Let them in
        return True
    return False


def auth_function(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth_validation(auth.username, auth.password):
            return (
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                   )
        return func(*args, **kwargs)
    return wrapper

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

            encoded_password = json['password'].encode('utf-8')
            app.bcrypt_rounds = 12

            hashed = bcrypt.hashpw(
                encoded_password, bcrypt.gensalt(app.bcrypt_rounds)
            )

            json['password'] = hashed
            app.db.users.insert_one(json)
            json.pop('password')
            return (json, 201, None)
        elif 'username' in json and 'password' in json:
                return ({'error': 'no email was specified'}, 400, None)
        elif 'username' not in json or 'email' not in json or 'password' not in json:
                return ({'error': 'missing fields'}, 400, None)
        else:
            print("no se posteó ná")
            return (None, 400, "Hola negro que pajó?")

    def get(self):
        user_email = request.args.get('email')
        user_collection = app.db.users
        json_user = request.args
        jsonPassword = json_user.get('password')
        if user_email is None:
            return("no parameter in url", 404, None)
        user = user_collection.find_one({"email": user_email})
        # pdb.set_trace()
        if user is None:
            print('no user exists')
            return None
        else:
            encodedPassword = jsonPassword.encode('utf-8')
            if bcrypt.hashpw(encodedPassword, user['password']) == user['password']:
                user.pop('password')

                return(user, 200, None)
            else:
                return('login failed', 404, None)

    @auth_function
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

            user.pop('password')
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
        print("trips: " + str(isinstance(trips_arr, list)))
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

    def put(self):
        args = request.args
        trips_col = app.db.trips


        trip_destination = args.get('destination') if args.get('destination') else None
        trip_start_date = args.get('start_date') if args.get('start_date') else None

        trip = trips_col.find_one({
            'destination': trip_destination
        })

        if trip is not None:
            if 'destination' in json:
                trip['destination'] = json['destination']

            if 'start_date' in json:
                trip['start_date'] = json['start_date']

            trips_col.save(trip)
            return (trip, 200, None)

        return ({'error': 'no user with that email found'}, 404, None)

    def patch(self):
        destination = request.args.get('destination')
        waypoints = request.json.get('waypoints')

        trips_col = app.db.trips

        updated_trip = trips_col.find_one_and_update(
            {'destination': destination},
            {'$destination': destination,
             '$waypoints': waypoints},
            return_document=ReturnDocument.AFTER)

        return(updated_trip, 200, None)


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
