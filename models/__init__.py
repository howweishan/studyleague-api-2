from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BaseModel:
    """Base model class for all PocketBase records"""
    id: str
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create instance from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

@dataclass
class User(BaseModel):
    """User model"""
    email: str
    emailVisibility: bool = False
    verified: bool = False
    name: Optional[str] = None
    avatar: Optional[str] = None

@dataclass
class StudySession(BaseModel):
    """Study session model"""
    user: str  # User ID
    durationMinutes: int = 0
    active: bool = True
    room: Optional[str] = None  # Room ID
    startedAt: Optional[datetime] = None
    endedAt: Optional[datetime] = None
    integrityScore: Optional[float] = None

@dataclass
class StudyRoom(BaseModel):
    """Study room model"""
    roomName: str
    host: str  # User ID
    maxParticipants: int
    isPublic: bool = True
    thumbnail: Optional[str] = None
    webrtcSessionId: Optional[str] = None

@dataclass
class Achievement(BaseModel):
    """Achievement model"""
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None
    requiredHours: Optional[float] = None

@dataclass
class UserAchievement(BaseModel):
    """User achievement model"""
    user: str  # User ID
    achievement: str  # Achievement ID
    unlockedAt: Optional[datetime] = None

@dataclass
class Discussion(BaseModel):
    """Discussion model"""
    author: str  # User ID
    title: str
    content: str

@dataclass
class DiscussionReply(BaseModel):
    """Discussion reply model"""
    author: str  # User ID
    discussion: str  # Discussion ID
    body: str

@dataclass
class LeaderboardEntry(BaseModel):
    """Leaderboard entry model"""
    user: str  # User ID
    totalMinutes: float
