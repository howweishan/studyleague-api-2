from marshmallow import Schema, fields

class BaseSchema(Schema):
    """Base schema for all models"""
    id = fields.Str(required=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)
