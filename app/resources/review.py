from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger
from app.models import ReviewModel
from app.services.card import CardService
from app.enum import ReviewAnswerEnum

def validate_enum(enum_class):
    return lambda value: value if value in [e.value for e in enum_class] else abort(400, message='Invalid value')


class ReviewCollection(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self):
        reviews = ReviewModel.query.all()
        return jsonify(reviews=[review.serialize() for review in reviews])

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('delay_response', type=str, required=True, help='Delay response cannot be blank')
        parser.add_argument('card_id', type=str, required=True, help='Card ID cannot be blank')
        parser.add_argument('review_answer', type=validate_enum(ReviewAnswerEnum), required=True, help='Review Answer needs to be a valid value')

        data = parser.parse_args()

        review_answer = ReviewAnswerEnum[data['review_answer']]
        CardService.process_review(data['card_id'], review_answer)

        # review = ReviewModel(**data)
        # review.save_to_db()
        return {'message': 'Review created successfully.'}, 201

class Review(Resource):
    def __init__(self):
        self.logger = create_logger()

    @jwt_required()
    def get(self, review_id):
        review = ReviewModel.query.filter_by(id=review_id).first()
        if not review:
            return {'message': 'Review not found'}, 404
        return jsonify(review.serialize())

