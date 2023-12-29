import json

from app.util.encoder import AlchemyEncoder
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.db import db

from datetime import datetime
from uuid import uuid4
from app.enum import CardStageEnum

class CardModel(db.Model):
    __tablename__ = 'cards'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    front = db.Column(db.String(200), nullable=False)
    back = db.Column(db.String(200), nullable=False)
    ease = db.Column(db.Float, default=2.5)
    learning_step = db.Column(db.Integer, default=0)
    re_learning_step = db.Column(db.Integer, default=0)
    current_interval = db.Column(db.Integer, default=1)
    stage = db.Column(db.Enum(CardStageEnum), default=CardStageEnum.LEARNING)
    due = db.Column(db.TIMESTAMP, nullable=True)
    deck_id = db.Column(UUID(as_uuid=True), db.ForeignKey('decks.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)

    deck = relationship("DeckModel", back_populates="cards")
    
    def __init__(self, front, back, deck_id, due = None):
        self.front = front
        self.back = back
        self.deck_id = deck_id
        self.due = due

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return json.loads(json.dumps(self, cls=AlchemyEncoder))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_cards_for_review(cls):
        current_date = datetime.utcnow()
        return CardModel.query.filter(
                (
                    (CardModel.due <= current_date) |
                    (CardModel.due == None)
                )
            ).all()

    @classmethod
    def delete(cls, deck):
        db.session.delete(deck)
        db.session.commit()