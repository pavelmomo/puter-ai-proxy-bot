import logging

from g4f.client import AsyncClient
from g4f.Provider import ProviderType, ProviderUtils
from g4f.typing import Message

from config import settings

logger = logging.getLogger(__name__)


class ChatClient:
    _client: AsyncClient
    _history: list[Message]
    _provider: ProviderType
    _model: str

    def __init__(self, provider: ProviderType, model: str) -> None:
        self._client = AsyncClient()
        self._history = []
        self._provider = provider
        self._model = model

    def set_history(self, messages: list[Message]):
        _history = messages

    def get_messages_history(self) -> list[Message]:
        return self._history

    async def send_prompt(self, prompt: str) -> str:
        self._history.append({"role": "user", "content": prompt})

        try:
            response = await self._client.chat.completions.create(
                messages=self._history,
                model=self._model,
                provider=self._provider,
                web_search=False,
            )
            response_content: str = response.choices[0].message.content
            self._history.append({"role": "assistant", "content": response_content})

            return response_content
        except Exception:
            self._history.clear()
            logger.exception(f"Произошла ошибка при отправке промпта ({prompt})")

            return "Произошла ошибка"


chat_client = ChatClient(
    ProviderUtils.convert[settings.AI_PROVIDER_NAME], settings.AI_MODEL_NAME
)
