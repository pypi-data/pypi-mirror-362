from pydantic import Field
from letschatty.models.base_models.related_asset_mixin import RelatedAssetsMixin

class ContextItem(RelatedAssetsMixin):
    """Individual context item with title and content"""
    title: str = Field(..., description="Title of the context section")
    content: str = Field(..., description="Content of the context section")
    order: int = Field(default=0, description="Order for displaying contexts")
    is_active: bool = Field(default=True, description="Whether the context item is active")