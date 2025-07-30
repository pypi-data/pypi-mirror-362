import logging
from typing import Self

from fastapi import Depends
from openai.types.chat import ChatCompletionSystemMessageParam
from openai.types.chat import ChatCompletionUserMessageParam

from .prompts import SENS_TOPIC_CHECK_SYSTEM_PROMPT
from .prompts import SENS_TOPIC_CHECK_USER_PROMPT
from common.llm.client import LLMClient
from registry.src.servers.repository import ServerRepository
from registry.src.servers.schemas import ServerCreate
from registry.src.servers.schemas import Tool
from registry.src.settings import settings
from registry.src.validator.schemas import ServerNeedsSensitiveDataResponse
from registry.src.validator.schemas import Tools
from registry.src.validator.schemas import ValidationResult
from registry.src.validator.ssl import SSLHelper


class ValidationService:
    def __init__(
        self,
        servers_repo: ServerRepository,
        ssl_helper: SSLHelper,
    ) -> None:
        self._servers_repo = servers_repo
        self._ssl_helper = ssl_helper
        logger = logging.getLogger("LLMClient")
        self._llm_client = LLMClient(
            logger, proxy=settings.llm_proxy, base_url=settings.openai_base_url
        )

    async def _mcp_needs_sensitive_data(
        self,
        data: ServerCreate,
        tools: list[Tool],
    ) -> bool:
        system_message = ChatCompletionSystemMessageParam(
            content=SENS_TOPIC_CHECK_SYSTEM_PROMPT.render(), role="system"
        )

        message = ChatCompletionUserMessageParam(
            content=SENS_TOPIC_CHECK_USER_PROMPT.render(
                server_data=data,
                tools_data=Tools.model_validate(tools),
            ),
            role="user",
        )

        response = await self._llm_client.request_to_beta(
            model=settings.llm_model,
            messages=[system_message, message],
            response_format=ServerNeedsSensitiveDataResponse,
        )

        answer = ServerNeedsSensitiveDataResponse.model_validate_json(
            response.choices[0].message.content,
        )

        return answer.server_needs_sensitive_data

    async def validate_server(
        self, data: ServerCreate, tools: list[Tool]
    ) -> ValidationResult:
        result = ValidationResult()

        result.server_requires_sensitive_data = await self._mcp_needs_sensitive_data(
            data,
            tools,
        )
        result.authority_level = await self._ssl_helper.get_ssl_authority_level(
            data.url,
        )

        return result

    @classmethod
    def get_new_instance(
        cls,
        servers_repo: ServerRepository = Depends(ServerRepository.get_new_instance),
        ssl_helper: SSLHelper = Depends(SSLHelper.get_new_instance),
    ) -> Self:
        return cls(
            servers_repo=servers_repo,
            ssl_helper=ssl_helper,
        )
