import json
from sqlalchemy.dialects.postgresql import UUID
from app.config.db import db
from datetime import datetime
from uuid import uuid4
from app.util.encoder import AlchemyEncoder

class ReviewModel(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    delay_response = db.Column(db.Interval)
    card_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cards.id'), primary_key=True)
    review_answear_id = db.Column(UUID(as_uuid=True), db.ForeignKey('review_answears.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, card_id, review_answear_id, delay_response):
        self.card_id = card_id
        self.review_answear_id = review_answear_id
        self.delay_response = delay_response

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return json.loads(json.dumps(self, cls=AlchemyEncoder))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def delete(cls, deck):
        db.session.delete(deck)
        db.session.commit()