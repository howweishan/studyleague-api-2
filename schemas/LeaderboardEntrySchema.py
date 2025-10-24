from marshmallow import fields
from schemas.BaseSchema import BaseSchema

class LeaderboardEntrySchema(BaseSchema):
    """Leaderboard entry schema"""
    user = fields.Str(required=True)
    totalMinutes = fields.Float(required=True)
