from letschatty.models.company.assets.ai_agents.chatty_ai_agent import ChattyAIAgent
from letschatty.models.company.assets.ai_agents.chatty_ai_mode import ChattyAIMode
from letschatty.models.company.assets.ai_agents.context_item import ContextItem
from letschatty.models.company.assets.ai_agents.faq import FAQ
from letschatty.models.company.assets.ai_agents.chat_example import ChatExample
from letschatty.models.company.assets.ai_agents.related_asset import RelatedChattyAsset
from letschatty.models.company.assets.company_assets import CompanyAssetType
from letschatty.models.chat.chat import Chat
from typing import List, Type
from letschatty.models.base_models.related_asset_mixin import RelatedAssetsMixin

class RelevantContextPicker:

    @staticmethod
    def should_be_used(ai_agent_item : RelatedAssetsMixin, chat:Chat) -> bool:
        if ai_agent_item.has_assets_restrictions():
            return RelevantContextPicker.is_related_to_chat(ai_agent_item, chat)
        return True

    @staticmethod
    def is_related_to_chat(ai_agent_item : RelatedAssetsMixin, chat:Chat) -> bool:
        for related_asset in ai_agent_item.related_assets:
            if related_asset.asset_Type == CompanyAssetType.TAGS:
                return related_asset.asset_id in chat.assigned_tag_ids
            if related_asset.asset_Type == CompanyAssetType.PRODUCTS:
                return related_asset.asset_id in chat.assigned_product_ids or related_asset.asset_id in chat.bought_product_ids
            if related_asset.asset_Type == CompanyAssetType.SOURCES:
                return related_asset.asset_id in chat.assigned_source_ids
            if related_asset.asset_Type == CompanyAssetType.BUSINESS_AREAS:
                raise NotImplementedError("Business areas are not supported yet")
            if related_asset.asset_Type == CompanyAssetType.FUNNELS:
                raise NotImplementedError("Funnels are not supported yet")
        return False