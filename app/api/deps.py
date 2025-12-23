from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import httpx
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token", auto_error=False)

async def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
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
            # We don't necessarily raise for status code because the API might return 200 with success: false
            # adhering to the user spec, but let's be safe and check json content.
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
