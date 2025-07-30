from typing import List
from pydantic import Field, BaseModel
from ..company.assets.ai_agents.related_asset import RelatedChattyAsset


class RelatedAssetsMixin(BaseModel):
    """Protocol for models that have related chatty assets"""
    related_assets: List[RelatedChattyAsset] = Field(default_factory=list)

    def has_assets_restrictions(self) -> bool:
        """Check if the model has assets restrictions"""
        return self.related_assets is not None and len(self.related_assets) > 0