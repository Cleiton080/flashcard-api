from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.deck import DeckModel

class DeckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DeckModel
        include_relationships = False
        load_instance = False
