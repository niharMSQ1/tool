from typing import Optional
from pydantic import BaseModel

class IntegrationConfig(BaseModel):
    token: Optional[str] = None
    bearer: Optional[str] = None

class ComplianceRequest(BaseModel):
    tool_id: str
    auth_token: str
    configuration_data: IntegrationConfig
