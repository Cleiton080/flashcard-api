from flask_restful import Resource, reqparse
from app.models.card import CardModel
from flask_jwt_extended import jwt_required
from app.config.db import db
from app.util.logz import create_logger
from flask import jsonify

class CardCollection(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self):
        cards = CardModel.query.all()
        return jsonify(cards=[card.serialize() for card in cards])

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('front', type=str, required=True, help='Front cannot be blank')
        parser.add_argument('back', type=str, required=True, help='Back cannot be blank')
        parser.add_argument('deck_id', type=str, required=True, help='Deck ID cannot be blank')

        data = parser.parse_args()
        card = CardModel(**data)
        card.save_to_db()
        return {'message': 'Card created successfully.'}, 201

class Card(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, card_id):
        card = CardModel.find_by_id(card_id)
        if not card:
            return {'message': 'Card not found'}, 404
        return jsonify(card.serialize())

    @jwt_required()
    def put(self, card_id):
        parser = reqparse.RequestParser()
        parser.add_argument('front', type=str, required=True, help='Front cannot be blank')
        parser.add_argument('back', type=str, required=True, help='Back cannot be blank')
        parser.add_argument('due', type=str, default=None)

        data = parser.parse_args()
        card = CardModel.find_by_id(card_id)
        if not card:
            return {'message': 'Card not found'}, 404
        card.front = data['front']
        card.back = data['back']

        if data['due'] is not None:
           card.due = data['due']

        db.session.commit()
        return {'message': 'Card updated successfully.'}

    @jwt_required()
    def delete(self, card_id):
        card = CardModel.find_by_id(card_id)
        if not card:
            return {'message': 'Card not found'}, 404
        CardModel.delete(card)
        return {'message': 'Card deleted'}
