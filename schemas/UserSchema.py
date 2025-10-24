from marshmallow import fields, validate
from schemas.BaseSchema import BaseSchema

class UserSchema(BaseSchema):
    """User schema"""
    id = fields.Str(required=False)
    email = fields.Email(required=True, validate=validate.Length(min=5, max=100))
    role = fields.Str(allow_none=False, load_default='user')
    username = fields.Str(required=True, validate=validate.Length(min=5, max=50))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=8))
    passwordConfirm = fields.Str(load_only=True, required=True, validate=validate.Length(min=8))
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    dob = fields.Date(allow_none=True)
    gender = fields.Str(allow_none=True)
    avatar = fields.Str(allow_none=True)
    emailVisibility = fields.Bool(load_default=False)
    verified = fields.Bool(load_default=False)
