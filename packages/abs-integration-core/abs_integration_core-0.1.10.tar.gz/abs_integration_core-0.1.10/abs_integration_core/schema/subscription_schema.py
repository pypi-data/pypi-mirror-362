from pydantic import BaseModel, Field
from typing import Optional, List


class Subscription(BaseModel):
    target_url: str
    site_id: str
    resource_id: str
    target_path: str
    event_types: List[str]
    provider_name: str
    user_id: int
    integration_id: str

    class Config:
        extra = "allow"


class SubscribeRequestSchema(BaseModel):
    target_url: str = Field(..., description="Target URL to subscribe to")
    site_id: Optional[str] = Field(None, description="SharePoint site ID")
    resource_id: Optional[str] = Field(None, description="List or Drive ID")
    target_path: str = Field("", description="Target path to subscribe to")
    event_types: List[str] = Field(["updated"], description="Change types to subscribe to")
    expiration_days: int = Field(15, description="Subscription expiration in days (max 30)")
