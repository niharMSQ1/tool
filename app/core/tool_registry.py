from fastapi import HTTPException, status


def get_integration_type_by_tool_id(tool_id: str) -> str:
    """
    Look up the integration type for a given tool ID.
    """
    integration_type = ""
    
    if not integration_type:
        # For development/skeletal purposes, if not found, we might want to default or error.
        # Strict validation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or unregistered Tool ID: {tool_id}"
        )
    
    return integration_type
