from pydantic import BaseModel

class ConfigurationData(BaseModel):
    token: str
    bearer: str

class GithubComplianceRequest(BaseModel):
    tool_id: str
    auth_token: str
    configuration_data: ConfigurationData
