import json

from app.util.encoder import AlchemyEncoder
from sqlalchemy.dialects.postgresql import UUID

from app.config.db import db

from datetime import datetime
from uuid import uuid4

class DeckModel(db.Model):
    __tablename__ = 'decks'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    learning_step_again = db.Column(db.Integer, default=1)
    learning_step_good = db.Column(db.Integer, default=10)
    graduating_interval = db.Column(db.Integer, default=1)
    easy_interval = db.Column(db.Integer, default=4)
    interval_modifier = db.Column(db.Float, default=1.0)
    easy_bonus = db.Column(db.Float, default=2.5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        self.name = name

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