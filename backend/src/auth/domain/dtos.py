from pydantic import BaseModel, EmailStr


class AuthRequest(BaseModel):
    """
    Authentication request model containing user credentials.
    
    Attributes:
        username: User's email address used for authentication
        password: User's password for authentication
    """
    username: EmailStr
    password: str


class AuthResponse(BaseModel):
    """
    Authentication response model containing JWT tokens.
    
    Attributes:
        access_token: JWT access token for authenticated requests
        refresh_token: JWT refresh token for obtaining new access tokens
    """
    access_token: str
    refresh_token: str
