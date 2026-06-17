from __future__ import annotations

import threading

from domain_discovery_engine.core.config import AppConfig


class LLMProvider:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig()
        self._local = threading.local()

    def invoke(self, system_prompt: str, user_prompt: str) -> str:
        client = self._get_client()
        from langchain_core.messages import HumanMessage, SystemMessage

        response = client.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )
        content = response.content
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "".join(
                part.get("text", "") if isinstance(part, dict) else str(part) for part in content
            )
        return str(content)

    def _get_client(self):
        client = getattr(self._local, "client", None)
        if client is None:
            client = self._create_client()
            self._local.client = client
        return client

    def _create_client(self):
        from langchain_openai import AzureChatOpenAI

        model_kwargs = {}
        if self.config.llm_reasoning_effort:
            model_kwargs["reasoning_effort"] = self.config.llm_reasoning_effort

        return AzureChatOpenAI(
            api_key=self.config.azure_openai_api_key,
            azure_endpoint=self.config.azure_openai_endpoint,
            api_version=self.config.azure_openai_api_version,
            azure_deployment=self.config.azure_openai_deployment,
            model=self.config.azure_openai_model or None,
            temperature=self.config.llm_temperature,
            model_kwargs=model_kwargs,
        )
