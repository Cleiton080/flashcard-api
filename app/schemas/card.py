from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.card import CardModel

class CustomEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value.value)

class CardSchema(SQLAlchemyAutoSchema):
    stage = CustomEnumField(attribute="stage")

    class Meta:
        model = CardModel
        include_relationships = False
        load_instance = False
