from fastapi import HTTPException, status
from app.schemas.integration import ComplianceRequest
from app.services.github.service import process_github_compliance
from app.services.zoho.service import process_zoho_compliance
from app.services.azure.service import process_azure_compliance
from app.services.slack.service import process_slack_compliance
from app.services.linear.service import process_linear_compliance

async def dispatch_compliance_request(integration_type: str, request: ComplianceRequest, user: dict):
    # Normalize integration type
    service_map = {
        "github": process_github_compliance,
        "zoho": process_zoho_compliance,
        "azure": process_azure_compliance,
        "slack": process_slack_compliance,
        "linear": process_linear_compliance
    }
    
    handler = service_map.get(integration_type.lower())
    
    if not handler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration type '{integration_type}' not supported. Supported: {list(service_map.keys())}"
        )
        
    return await handler(request=request, user=user)
