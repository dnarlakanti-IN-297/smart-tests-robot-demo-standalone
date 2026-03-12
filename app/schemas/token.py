"""Token schemas for JWT authentication"""

from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for JWT token response"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""

    username: Optional[str] = None
    user_id: Optional[int] = None
