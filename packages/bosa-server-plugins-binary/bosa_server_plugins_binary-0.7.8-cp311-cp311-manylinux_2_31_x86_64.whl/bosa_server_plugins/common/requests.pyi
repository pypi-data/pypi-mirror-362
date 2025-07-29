from pydantic import BaseModel

class AuthorizationCallbackRequest(BaseModel):
    """Request model for authorization callback."""
    callback_url: str
