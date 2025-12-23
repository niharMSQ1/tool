from fastapi import APIRouter, HTTPException, status
from app.schemas.github import GithubComplianceRequest
from app.api.deps import validate_token_with_auth_service
from app.services.github_service import process_github_compliance

router = APIRouter()

@router.post("/compliance")
async def github_compliance(payload: GithubComplianceRequest):
    # Validate the auth token provided in the payload
    user = await validate_token_with_auth_service(payload.auth_token)
    
    # Process GitHub compliance logic
    result = await process_github_compliance(payload, user)
    
    return result
