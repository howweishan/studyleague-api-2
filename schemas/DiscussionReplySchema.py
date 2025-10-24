from marshmallow import fields, validates, ValidationError
from schemas.BaseSchema import BaseSchema

class DiscussionReplySchema(BaseSchema):
    """Discussion reply schema"""
    author = fields.Str(required=True)
    discussion = fields.Str(required=True)
    body = fields.Str(required=True)
    
    @validates('body')
    def validate_body(self, value):
        if len(value) > 1000:
            raise ValidationError('Body must be 1000 characters or less.')
