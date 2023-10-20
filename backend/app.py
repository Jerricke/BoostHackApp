#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource, Api
from datetime import datetime

# Local imports
from config import app, api, db

# Add your model imports
from models import User, Connection

api = Api(app)


# Views go here!
class Index(Resource):
    def get(self):
        return {"msg": "This is the Index"}, 200


api.add_resource(Index, "/", endpoint="index")


class Users(Resource):
    def get(self):
        users = [u.to_dict(rules=("-_password_hash",)) for u in User.query.all()]
        return users, 200

    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        dob = datetime.strptime(data["dob"], "%Y-%m-%dT%H:%M:%S")
        email = data["email"]
        pfp = data["pfp"]
        if data and username and password and dob and email and pfp:
            newUser = User(username=username, dob=dob, email=email, pfp=pfp)
            newUser.password_hash = password
            db.session.add(newUser)
            db.session.commit()
            return newUser.to_dict(rules=("-_password_hash",)), 201
        else:
            return {"error": "Could not create new user"}, 422


api.add_resource(Users, "/users", endpoint="users")


class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return user.to_dict(rules=("-_password_hash",)), 200

    def delete(self, id):
        pass

    def patch(self, id):
        pass


api.add_resource(UserById, "/users/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
