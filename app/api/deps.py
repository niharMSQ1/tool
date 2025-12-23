from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import httpx
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token", auto_error=False)

async def validate_token_with_auth_service(token: str) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.AUTH_VERIFY_URL,
                json={"jwtToken": token}
            )
        except httpx.RequestError as exc:
             raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Authentication service unavailable: {exc}",
            )

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response from authentication service",
        )

    if not data.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=data.get("message", "Unauthorized"),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return data.get("data", {}).get("user")

async def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    return await validate_token_with_auth_service(token)
