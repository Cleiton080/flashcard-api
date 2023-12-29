from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger
from app.models import ReviewModel

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
        parser.add_argument('review_answear_id', type=str, required=True, help='Review Answear cannot be blank')

        data = parser.parse_args()
        review = ReviewModel(**data)
        review.save_to_db()
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

