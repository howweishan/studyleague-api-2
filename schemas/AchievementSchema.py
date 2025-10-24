from marshmallow import fields, validates, ValidationError
from schemas.BaseSchema import BaseSchema

class AchievementSchema(BaseSchema):
    """Achievement schema"""
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    icon = fields.Str(allow_none=True)
    requiredHours = fields.Float(allow_none=True)
    
    @validates('title')
    def validate_title(self, value):
        if len(value) > 100:
            raise ValidationError('Title must be 100 characters or less.')
    
    @validates('description')
    def validate_description(self, value):
        if value and len(value) > 500:
            raise ValidationError('Description must be 500 characters or less.')
