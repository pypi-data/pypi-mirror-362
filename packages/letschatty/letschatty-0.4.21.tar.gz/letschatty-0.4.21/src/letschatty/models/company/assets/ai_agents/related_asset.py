from pydantic import BaseModel, Field, ConfigDict
from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.company.assets.company_assets import CompanyAssetType

class RelatedChattyAsset(BaseModel):
    asset_id: StrObjectId = Field(frozen=True)
    asset_type : CompanyAssetType = Field(frozen=True)

    model_config = ConfigDict(
        extra = "ignore"
    )