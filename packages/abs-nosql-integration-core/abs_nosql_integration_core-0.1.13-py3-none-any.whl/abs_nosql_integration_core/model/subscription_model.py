from abs_nosql_repository_core.document.base_document import BaseDraftDocument
from pydantic import Field
from typing import List


class SubscriptionDocument(BaseDraftDocument):
    target_url: str = Field(..., description="The target URL to subscribe to")
    site_id: str = Field(..., description="The ID of the site")
    resource_id: str = Field(..., description="The ID of the resource")
    target_path: str = Field(..., description="The target path to subscribe to")
    event_types: List[str] = Field(..., description="The types of events to subscribe to")
    provider_name: str = Field(..., description="The name of the provider")

    user_id: int = Field(..., description="The ID of the user")
    integration_id: str = Field(..., description="The ID of the integration")

    class Settings:
        name = "subscriptions"
