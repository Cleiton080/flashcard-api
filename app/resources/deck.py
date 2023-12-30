from app.config.db import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger
from app.models import DeckModel

from flask import jsonify

class DeckCollection(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self):
        user = get_jwt_identity()

        decks = DeckModel.find(user['id'])
        return jsonify(decks=[deck.serialize() for deck in decks])

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')

        user = get_jwt_identity()

        data = parser.parse_args()
        data['user_id'] = user['id']

        deck = DeckModel(**data)
        deck.save_to_db()
        return deck.serialize(), 201

class Deck(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, deck_id):
        user = get_jwt_identity()

        deck = DeckModel.find_by_id(deck_id, user['id'])
        if not deck:
            return {'message': 'Deck not found'}, 404
        return jsonify(deck.serialize())

    @jwt_required()
    def put(self, deck_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name cannot be blank')

        data = parser.parse_args()
        user = get_jwt_identity()

        deck = DeckModel.find_by_id(deck_id, user['id'])
        if not deck:
            return {'message': 'Deck not found'}, 404
        deck.name = data['name']
        db.session.commit()
        return {'message': 'Deck updated successfully.'}

    @jwt_required()
    def delete(self, deck_id):
        user = get_jwt_identity()

        deck = DeckModel.find_by_id(deck_id, user['id'])
        if not deck:
            return {'message': 'Deck not found'}, 404
        DeckModel.delete(deck)
        return {'message': 'Deck deleted'}

