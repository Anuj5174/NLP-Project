"""
User schemas for validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    full_name: Optional[str] = Field(None, description="Full name of user")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "secretpassword",
                "full_name": "John Doe"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "secretpassword"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    user_id: int
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "recruiter",
                "is_active": True,
                "created_at": "2026-02-24T10:00:00"
            }
        }


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "user_id": 1,
                    "email": "user@example.com",
                    "full_name": "John Doe",
                    "role": "recruiter",
                    "is_active": True,
                    "created_at": "2026-02-24T10:00:00"
                }
            }
        }


class TokenData(BaseModel):
    """Schema for token payload data"""
    email: Optional[str] = None