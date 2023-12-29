import json

from app.util.encoder import AlchemyEncoder

from sqlalchemy.dialects.postgresql import UUID
from app.config.db import db

from datetime import datetime
from uuid import uuid4

class ReviewAnswearModel(db.Model):
    __tablename__ = 'review_answears'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)

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