from pydantic import Field, BaseModel
from letschatty.models.base_models.related_asset_mixin import RelatedAssetsMixin

class FAQ(RelatedAssetsMixin, BaseModel):
    """FAQ item with question and answer"""
    question: str = Field(..., description="The question")
    answer: str = Field(..., description="The answer to the question")
