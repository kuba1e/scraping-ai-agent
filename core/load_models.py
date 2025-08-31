import os
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from core.config import settings

OPEN_AI_MODEL = OpenAIChatModel('gpt-5-mini', provider = OpenAIProvider(base_url=settings.BASE_OPEN_API_URL, api_key=settings.OPEN_API_KEY))

