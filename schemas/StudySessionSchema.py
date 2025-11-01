from marshmallow import fields, validate
from schemas.BaseSchema import BaseSchema

class StudySessionSchema(BaseSchema):
    """Study session schema"""
    user = fields.Str(required=True)
    room = fields.Str(allow_none=True)
    active_duration = fields.Int(required=True, validate=validate.Range(min=1, max=1440000))
    active = fields.Bool(load_default=True)
    started_at = fields.DateTime(allow_none=True)
    ended_at = fields.DateTime(allow_none=True)
    integrity_score = fields.Float(allow_none=True, validate=validate.Range(min=0, max=100))
