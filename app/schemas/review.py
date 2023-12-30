from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.review import ReviewModel

class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ReviewModel
        include_relationships = False
        load_instance = False
