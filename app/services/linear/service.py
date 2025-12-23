from app.schemas.integration import ComplianceRequest
from app.services.base_service import process_service_compliance

async def process_linear_compliance(request: ComplianceRequest, user: dict):
     return await process_service_compliance("linear", request, user)
