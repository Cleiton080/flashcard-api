from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.card import CardModel

class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CardModel
        include_relationships = False
        load_instance = False
