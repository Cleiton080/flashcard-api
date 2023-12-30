from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.review import ReviewModel

class CustomEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value.value)


class ReviewSchema(SQLAlchemyAutoSchema):
    review_answer = CustomEnumField(attribute="stage")
    class Meta:
        model = ReviewModel
        include_relationships = False
        load_instance = False
