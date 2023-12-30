from app.config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))

    decks = relationship("DeckModel", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def serialize(self):
        from app.schemas import UserSchema
        return UserSchema().dump(self)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

