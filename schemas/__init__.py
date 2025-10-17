from marshmallow import Schema, fields, post_load, validates, ValidationError
from typing import Dict, Any

class BaseSchema(Schema):
    """Base schema for all models"""
    id = fields.Str(required=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)

class UserSchema(BaseSchema):
    """User schema"""
    email = fields.Email(required=True)
    name = fields.Str(allow_none=True)
    avatar = fields.Str(allow_none=True)
    emailVisibility = fields.Bool(load_default=False)
    verified = fields.Bool(load_default=False)

class StudySessionSchema(BaseSchema):
    """Study session schema"""
    user = fields.Str(required=True)
    room = fields.Str(allow_none=True)
    durationMinutes = fields.Int(load_default=0)
    active = fields.Bool(load_default=True)
    startedAt = fields.DateTime(allow_none=True)
    endedAt = fields.DateTime(allow_none=True)
    integrityScore = fields.Float(allow_none=True)

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

class AchievementSchema(BaseSchema):
    """Achievement schema"""
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    icon = fields.Str(allow_none=True)
    requiredHours = fields.Float(allow_none=True)
    
    @validates('title')
    def validate_title(self, value):
        if len(value) > 100:
            raise ValidationError('Title must be 100 characters or less.')
    
    @validates('description')
    def validate_description(self, value):
        if value and len(value) > 500:
            raise ValidationError('Description must be 500 characters or less.')

class UserAchievementSchema(BaseSchema):
    """User achievement schema"""
    user = fields.Str(required=True)
    achievement = fields.Str(required=True)
    unlockedAt = fields.DateTime(allow_none=True)

class DiscussionSchema(BaseSchema):
    """Discussion schema"""
    author = fields.Str(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    
    @validates('title')
    def validate_title(self, value):
        if len(value) > 200:
            raise ValidationError('Title must be 200 characters or less.')

class DiscussionReplySchema(BaseSchema):
    """Discussion reply schema"""
    author = fields.Str(required=True)
    discussion = fields.Str(required=True)
    body = fields.Str(required=True)
    
    @validates('body')
    def validate_body(self, value):
        if len(value) > 1000:
            raise ValidationError('Body must be 1000 characters or less.')

class LeaderboardEntrySchema(BaseSchema):
    """Leaderboard entry schema"""
    user = fields.Str(required=True)
    totalMinutes = fields.Float(required=True)
