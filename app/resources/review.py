from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.util.logz import create_logger
from app.models import ReviewModel, CardModel
from app.services.card import CardService
from app.enum import ReviewAnswerEnum
from app.exceptions import CannotReviewCard

def validate_enum(enum_class):
    return lambda value: value if value in [e.value for e in enum_class] else abort(400, message='Invalid value')


class ReviewCollection(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self):
        user = get_jwt_identity()

        reviews = ReviewModel.find(user['id'])
        return jsonify(reviews=[review.serialize() for review in reviews])

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('delay_response', type=str, required=True, help='Delay response cannot be blank')
        parser.add_argument('card_id', type=str, required=True, help='Card ID cannot be blank')
        parser.add_argument('review_answer', type=validate_enum(ReviewAnswerEnum), required=True, help='Review Answer needs to be a valid value')

        data = parser.parse_args()
        user = get_jwt_identity()

        card = CardModel.find_by_id(data['card_id'], user['id'])

        if card is None:
            return {'message': 'Card not found'}, 404

        review_answer = ReviewAnswerEnum[data['review_answer']]

        try:
            CardService.process_review(data['card_id'], review_answer, user['id'])
        except CannotReviewCard:
            return {'message': 'You cannot review this card right now'}, 400

        review = ReviewModel(**data)
        review.save_to_db()

        return review.serialize(), 201

class Review(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, review_id):
        user = get_jwt_identity()

        review = ReviewModel.find_by_id(review_id, user['id'])
        if not review:
            return {'message': 'Review not found'}, 404
        return jsonify(review.serialize())

