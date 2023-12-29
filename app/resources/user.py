import json
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from app.util.encoder import AlchemyEncoder
from app.util.logz import create_logger
from app.config.db import db
from app.models import UserModel


class UserLogin(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser() 
    parser.add_argument('username', type=str, required=True,
                        help='Not Blank')
    parser.add_argument('password', type=str, required=True,
                        help='Not Blank')

    def post(self):
        data = UserLogin.parser.parse_args()
        username = data['username']
        password = data['password']

        user = db.session.query(UserModel).filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {'status': 'Login failed.'}, 401
        access_token = create_access_token(identity=json.dumps(user, cls=AlchemyEncoder))
        return jsonify(
            token=access_token,
        )


class UserRegister(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()  
    parser.add_argument('username', type=str, required=True,
                        help='Not Blank')
    parser.add_argument('password', type=str, required=True,
                        help='Not Blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'user has already been created.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'user has been created successfully.'}, 201
