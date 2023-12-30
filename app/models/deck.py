from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.db import db

from datetime import datetime
from uuid import uuid4

class DeckModel(db.Model):
    __tablename__ = 'decks'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    graduating_interval = db.Column(db.Integer, default=1)
    easy_interval = db.Column(db.Integer, default=4)
    interval_modifier = db.Column(db.Float, default=1.0)
    easy_bonus = db.Column(db.Float, default=2.5)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cards = relationship("CardModel", back_populates="deck")
    learning_steps = relationship("LearningStepModel", back_populates="deck")
    user = relationship("UserModel", back_populates="decks")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        from app.schemas import DeckSchema
        return DeckSchema().dump(self)

    @classmethod
    def find(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()


    @classmethod
    def find_by_id(cls, _id, user_id):
        return cls.query.filter_by(id=_id, user_id=user_id).first()

    @classmethod
    def delete(cls, deck):
        db.session.delete(deck)
        db.session.commit()