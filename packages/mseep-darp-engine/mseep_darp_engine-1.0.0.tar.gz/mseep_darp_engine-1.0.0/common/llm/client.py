from logging import Logger
from typing import Type

from httpx import AsyncClient
from openai import APIError
from openai import AsyncOpenAI
from openai import InternalServerError
from openai import NOT_GIVEN
from openai import OpenAIError
from openai.types.chat import ChatCompletion
from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat import ChatCompletionToolParam
from pydantic import BaseModel


class LLMClient:
    def __init__(
        self, logger: Logger, proxy: str | None = None, base_url: str | None = None
    ) -> None:
        self._logger = logger

        if proxy is not None:
            self._logger.info("Enabled proxy %s", proxy)
            http_client = AsyncClient(proxy=proxy)
        else:
            http_client = AsyncClient()

        self.openai_client = AsyncOpenAI(http_client=http_client, base_url=base_url)

    @staticmethod
    def _get_full_messages(
        system_prompt: str | None, messages: list[ChatCompletionMessageParam]
    ) -> list[ChatCompletionMessageParam]:
        system_message: list[dict] = []
        if system_prompt:
            system_message = [
                {
                    "role": "system",
                    "content": system_prompt,
                    # Anthropic prompt caching
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        full_messages = system_message + messages
        return full_messages

    async def request(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
    ) -> ChatCompletion:
        full_messages = self._get_full_messages(
            system_prompt=system_prompt, messages=messages
        )
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=full_messages,
                max_tokens=max_tokens,
                tools=tools or NOT_GIVEN,
                timeout=30,
            )
        except APIError as error:
            self._logger.error(f"{error.code=} {error.body=}")
            raise
        except InternalServerError as error:
            self._logger.error(error.response.json())
            raise
        except OpenAIError as error:
            self._logger.error(
                "Request to Provider failed with the following exception",
                exc_info=error,
            )
            raise
        return response

    async def request_to_beta(
        self,
        model: str,
        messages: list[ChatCompletionMessageParam],
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        tools: list[ChatCompletionToolParam] | None = None,
        response_format: Type[BaseModel] = NOT_GIVEN,
    ) -> ChatCompletion:
        full_messages = self._get_full_messages(
            system_prompt=system_prompt, messages=messages
        )
        try:
            response = await self.openai_client.beta.chat.completions.parse(
                model=model,
                messages=full_messages,
                max_tokens=max_tokens,
                tools=tools or NOT_GIVEN,
                timeout=30,
                response_format=response_format,
            )
        except APIError as error:
            self._logger.error(f"{error.code=} {error.body=}")
            raise
        except InternalServerError as error:
            self._logger.error(error.response.json())
            raise
        except OpenAIError as error:
            self._logger.error(
                "Request to Provider failed with the following exception",
                exc_info=error,
            )
            raise
        return response
