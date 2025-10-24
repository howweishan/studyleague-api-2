from marshmallow import fields, validates, ValidationError
from schemas.BaseSchema import BaseSchema

class StudyRoomSchema(BaseSchema):
    """Study room schema"""
    roomName = fields.Str(required=True)
    host = fields.Str(required=True)
    participants = fields.Int(allow_none=True)
    maxParticipants = fields.Int(required=True)
    isPublic = fields.Bool(load_default=True)
    thumbnail = fields.Str(allow_none=True)
    webrtcSessionId = fields.Str(allow_none=True)
    
    @validates('roomName')
    def validate_room_name(self, value):
        if len(value) > 100:
            raise ValidationError('Room name must be 100 characters or less.')
    
    @validates('maxParticipants')
    def validate_max_participants(self, value):
        if not 1 <= value <= 50:
            raise ValidationError('Max participants must be between 1 and 50.')
    
    @validates('webrtcSessionId')
    def validate_webrtc_session_id(self, value):
        if value and len(value) > 100:
            raise ValidationError('WebRTC session ID must be 100 characters or less.')
