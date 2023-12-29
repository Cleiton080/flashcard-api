import json
from uuid import uuid4
from app.config.db import db
from app.util.encoder import AlchemyEncoder
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class LearningStepModel(db.Model):
    __tablename__ = 'learning_steps'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    interval_time = db.Column(db.Interval)
    ordering = db.Column(db.Integer, autoincrement=True)
    deck_id = db.Column(UUID(as_uuid=True), db.ForeignKey('decks.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, nullable=True)

    deck = relationship("DeckModel", back_populates="learning_steps")

    def __init__(self, interval_time):
        self.interval_time = interval_time

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return json.loads(json.dumps(self, cls=AlchemyEncoder))

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def delete(cls, learning_step):
        db.session.delete(learning_step)
        db.session.commit()