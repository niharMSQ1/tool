from app.schemas.integration import ComplianceRequest
from app.services.base_service import process_service_compliance

async def process_github_compliance(request: ComplianceRequest, user: dict):
    """
    Process the GitHub compliance request.
    This uses the generic ComplianceRequest schema now.
    """
    # We can eventually customize this, but for now reuse the base structure or custom logic
    # Reuse base for consistency in the skeleton phase
    return await process_service_compliance("github", request, user)
