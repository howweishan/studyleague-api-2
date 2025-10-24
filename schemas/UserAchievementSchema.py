from marshmallow import fields
from schemas.BaseSchema import BaseSchema

class UserAchievementSchema(BaseSchema):
    """User achievement schema"""
    user = fields.Str(required=True)
    achievement = fields.Str(required=True)
    unlockedAt = fields.DateTime(allow_none=True)
