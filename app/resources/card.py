from app.config.db import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger
from flask import jsonify, request
from app.models import CardModel, DeckModel

class CardCollection(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self):
        review = request.args.get('review', '').lower()

        user = get_jwt_identity()

        cards = CardModel.get_cards_for_review(user['id']) if review == 'true' else CardModel.find(user['id'])
        return jsonify(cards=[card.serialize({'only': ('id',)}) for card in cards])

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('front', type=str, required=True, help='Front cannot be blank')
        parser.add_argument('back', type=str, required=True, help='Back cannot be blank')
        parser.add_argument('deck_id', type=str, required=True, help='Deck ID cannot be blank')

        data = parser.parse_args()
        user = get_jwt_identity()

        deck = DeckModel.find_by_id(data['deck_id'], user['id'])

        if deck is None:
            return {'message': 'Deck not found'}, 404

        card = CardModel(**data)
        card.save_to_db()
        return card.serialize(), 201

class Card(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, card_id):
        user = get_jwt_identity()

        card = CardModel.find_by_id(card_id, user['id'])
        if not card:
            return {'message': 'Card not found'}, 404
        return jsonify(card.serialize())

    @jwt_required()
    def put(self, card_id):
        parser = reqparse.RequestParser()
        parser.add_argument('front', type=str, required=True, help='Front cannot be blank')
        parser.add_argument('back', type=str, required=True, help='Back cannot be blank')
        parser.add_argument('due', type=str, default=None)

        user = get_jwt_identity()
        data = parser.parse_args()
        card = CardModel.find_by_id(card_id, user['id'])
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
        user = get_jwt_identity()

        card = CardModel.find_by_id(card_id, user['id'])
        if not card:
            return {'message': 'Card not found'}, 404
        CardModel.delete(card)
        return {'message': 'Card deleted'}
