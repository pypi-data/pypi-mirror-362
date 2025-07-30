from pydantic import Field
from letschatty.models.base_models.related_asset_mixin import RelatedAssetsMixin

class FAQ(RelatedAssetsMixin):
    """FAQ item with question and answer"""
    question: str = Field(..., description="The question")
    answer: str = Field(..., description="The answer to the question")
