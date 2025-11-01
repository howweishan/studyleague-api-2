from marshmallow import fields
from schemas.BaseSchema import BaseSchema

class StudyTargetSchema(BaseSchema):
	"""Study target schema"""
	user = fields.Str(required=True)
	record_id = fields.Str(allow_none=True)
	daily_target = fields.Int(load_default=60)
	weekly_target = fields.Int(load_default=300)
	monthly_target = fields.Int(load_default=1200)
