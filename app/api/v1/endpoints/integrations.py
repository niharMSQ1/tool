from fastapi import APIRouter
from app.schemas.integration import ComplianceRequest
from app.api.deps import validate_token_with_auth_service
from app.services.dispatcher import dispatch_compliance_request
from app.core.tool_registry import get_integration_type_by_tool_id

router = APIRouter()

@router.post("/")
async def integrate_compliance(payload: ComplianceRequest):
    # 1. Validate Auth
    user = await validate_token_with_auth_service(payload.auth_token)
    
    # 2. Determine Integration Type from Tool ID
    integration_type = get_integration_type_by_tool_id(payload.tool_id)
    
    # 3. Dispatch to appropriate service
    result = await dispatch_compliance_request(integration_type, payload, user)
    
    return result
