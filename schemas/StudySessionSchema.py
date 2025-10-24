from marshmallow import fields
from schemas.BaseSchema import BaseSchema

class StudySessionSchema(BaseSchema):
    """Study session schema"""
    user = fields.Str(required=True)
    room = fields.Str(allow_none=True)
    durationMinutes = fields.Int(load_default=0)
    active = fields.Bool(load_default=True)
    startedAt = fields.DateTime(allow_none=True)
    endedAt = fields.DateTime(allow_none=True)
    integrityScore = fields.Float(allow_none=True)
