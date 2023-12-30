from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.learning_step import LearningStepModel

class LearningStepSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LearningStepModel
        include_relationships = False
        load_instance = False
