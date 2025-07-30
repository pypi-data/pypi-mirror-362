"""
Echo Sync Protocol Authentication Middleware

This module provides authentication middleware for the Echo Sync Protocol API.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..exceptions import AuthenticationError, AuthorizationError

# Configuration
import os
SECRET_KEY = os.getenv("ECHO_SYNC_SECRET_KEY", "test-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User:
    """Represents an authenticated user."""
    def __init__(self, username: str, permissions: list[str]):
        self.username = username
        self.permissions = permissions

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time delta
    
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user from the JWT token.
    
    Args:
        token: The JWT token from the request
    
    Returns:
        User: The authenticated user
    
    Raises:
        AuthenticationError: If the token is invalid
        AuthorizationError: If the user lacks required permissions
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthenticationError("Invalid authentication token")
        
        # TODO: Replace with actual user lookup from database
        # This is a placeholder implementation
        permissions = ["read", "write"]  # Example permissions
        return User(username=username, permissions=permissions)
    except JWTError:
        raise AuthenticationError("Invalid authentication token")

def require_permission(permission: str):
    """
    Decorator to require a specific permission for an endpoint.
    
    Args:
        permission: The required permission
    
    Returns:
        Callable: The decorated function
    """
    async def permission_dependency(current_user: User = Depends(get_current_user)):
        if permission not in current_user.permissions:
            raise AuthorizationError(f"User lacks required permission: {permission}")
        return current_user
    return permission_dependency 
