from flask_restful import Resource
from flask.views import MethodView


# Write Resources here
class User(Resource):

    def post(self):

        json = request.json
        print(json)
        if 'username' in json and 'email' in json and 'password' in json:
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
            return (None, 404, None)
        else:
            return (user, 200, None)

    def put(self):
        user_email = request.args.get('email')
        username = request.json.get('username')
        print(user_email)

        if user_email is None:
            return ({'error': 'no specified email for user'}, 404, None)

        user_col = app.db.users

        user = user_col.find_one({
            'email': user_email
        })

        if user is not None:
            user['username'] = username
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
