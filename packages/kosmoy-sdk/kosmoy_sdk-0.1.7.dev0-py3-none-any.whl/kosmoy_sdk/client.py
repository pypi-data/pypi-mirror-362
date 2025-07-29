from openai import OpenAI
from kosmoy_sdk._kosmoy_base import KosmoyBase
from kosmoy_sdk.exceptions import FunctionalityNotImplemented
from typing import Optional


class CustomChatCompletions:
    def __init__(self, client):
        self.client = client
        self._completions = CustomCompletions(client)

    @property
    def completions(self):
        return self._completions

class CustomCompletions:
    def __init__(self, client):
        self.client = client

    def create(self,
               model,
               use_guardrails: bool = False,
               *args, **kwargs):
        if kwargs.get('streaming'):
            raise FunctionalityNotImplemented("This functionality is not implemented in this version")
        kwargs["metadata"] = {
            "use_guardrails": use_guardrails
        }
        return self.client._client.chat.completions.create(model=model, *args, **kwargs)


class CustomEmbeddings:
    def __init__(self, client):
        self.client = client

    def create(self,
               input,
               model,
               use_guardrails: bool = False,
               *args, **kwargs):
        """
        Create embeddings for the given input.

        Args:
            input: The text(s) to embed
            model: The embedding model to use
            use_guardrails: Whether to apply guardrails to the embeddings
            *args, **kwargs: Additional arguments passed to OpenAI embeddings.create

        Returns:
            Embedding response from OpenAI
        """
        return self.client._client.embeddings.create(
            input=input,
            model=model,
            *args,
            **kwargs
        )


class CustomOpenAI:
    def __init__(self, *args, **kwargs):
        self._client = OpenAI(*args, **kwargs)
        self._chat = CustomChatCompletions(client=self)
        self._embeddings = CustomEmbeddings(client=self)

    @property
    def chat(self) -> CustomChatCompletions:
        return self._chat

    @property
    def embeddings(self) -> CustomEmbeddings:
        return self._embeddings

    @property
    def beta(self):
        return self._client.beta


class GatewayClient(KosmoyBase):
    def __init__(
            self,
            app_id: str,
            api_key: str,
            base_url: Optional[str] ,
            timeout: int = 30,
            max_retries: int = 3
    ):
        super().__init__(app_id=app_id, api_key=api_key,base_url=base_url,timeout=timeout,
                         max_retries=max_retries)

        self.client = CustomOpenAI(
            base_url=f"{self.gateway_config.base_url}/gateway/invoke",
            api_key=api_key,
            default_headers={
                "app-id": app_id,
                "api-key": api_key,
                "Content-Type": "application/json"
            }
        )
