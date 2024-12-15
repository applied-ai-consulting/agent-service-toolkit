from typing import Any

from langchain_core.callbacks import adispatch_custom_event
from langchain_core.messages import ChatMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.config import merge_configs
from pydantic import BaseModel, Field


class CustomData(BaseModel):
    "Custom data being sent by an agent"

    type: str = Field(
        description="The type of custom data, used in dispatch events",
        default="custom_data",
    )
    data: dict[str, Any] = Field(description="The custom data")

    def to_langchain(self) -> ChatMessage:
        return ChatMessage(content=[self.data], role="custom")

    async def adispatch(self, config: RunnableConfig | None = None) -> None:
        dispatch_config = RunnableConfig(
            tags=["custom_data_dispatch"],
        )
        await adispatch_custom_event(
            name=self.type,
            data=self.to_langchain(),
            config=merge_configs(config, dispatch_config),
        )

def validate_and_clean_json(response: str, default_value: str = "unknown") -> dict:
    """
    Validates and cleans up JSON response from LLM.
    Args:
        response: The raw response string from LLM
        default_value: Default value to use if JSON parsing fails
    Returns:
        A dictionary with market_segment key
    """
    try:
        # Clean up the response to ensure it's valid JSON
        json_str = response.strip()

        if not json_str.startswith('{'):
            json_str = json_str[json_str.find('{'):]
        if not json_str.endswith('}'):
            json_str = json_str[:json_str.rfind('}')+1]

        return json.loads(json_str)

    except (json.JSONDecodeError, ValueError):
        # If JSON parsing fails, return a default dictionary
        return {"result": default_value}

