from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import UserModel

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = False
        load_instance = False
