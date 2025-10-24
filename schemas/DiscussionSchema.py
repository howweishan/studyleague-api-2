from marshmallow import fields, validates, ValidationError
from schemas.BaseSchema import BaseSchema

class DiscussionSchema(BaseSchema):
    """Discussion schema"""
    author = fields.Str(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    
    @validates('title')
    def validate_title(self, value):
        if len(value) > 200:
            raise ValidationError('Title must be 200 characters or less.')
