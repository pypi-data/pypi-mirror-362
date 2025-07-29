from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from kosmoy_sdk import GatewayConfig
from kosmoy_sdk._kosmoy_base import KosmoyBase
from typing import Optional, Any
from pydantic import Field


class CustomChatOpenAI(ChatOpenAI):
    """Extended ChatOpenAI that allows for additional configuration"""
    gateway_config: Optional[GatewayConfig] = Field(default=None, exclude=True)
    session: Optional[Any] = Field(default=None, exclude=True)


class CustomOpenAIEmbeddings(OpenAIEmbeddings):
    """Extended OpenAIEmbeddings that allows for additional configuration"""
    gateway_config: Optional[GatewayConfig] = Field(default=None, exclude=True)
    session: Optional[Any] = Field(default=None, exclude=True)




class KosmoyGatewayLangchain(CustomChatOpenAI, KosmoyBase):

    def __init__(
            self,
            app_id: str,
            api_key: str,
            model: str,
            use_guardrails: bool = False,
            base_url: Optional[str] = None,
            timeout: int = 30,
            max_retries: int = 3,
            **kwargs
    ):
        KosmoyBase.__init__(self, app_id=app_id, api_key=api_key,base_url=base_url,timeout=timeout,
                            max_retries=max_retries)

        kwargs["metadata"] = {
            "use_guardrails": use_guardrails
        }

        CustomChatOpenAI.__init__(
            self,
            base_url=f"{self.gateway_config.base_url}/gateway/invoke",
            api_key=api_key,
            model=model,
            default_headers={
                "app-id": app_id,
                "api-key": api_key,
                "use_guardrails": str(use_guardrails), # langchain is not passing it as metadata the way they claim
                "Content-Type": "application/json",
            },
            **kwargs
        )

        
class KosmoyGatewayEmbeddings(CustomOpenAIEmbeddings, KosmoyBase):
    """Kosmoy Gateway integration for Langchain Embeddings"""

    def __init__(
            self,
            app_id: str,
            api_key: str,
            model: str = "text-embedding-3-small",  # Default embeddings model
            use_guardrails: bool = False,
            base_url: Optional[str] = None,
            timeout: int = 30,
            max_retries: int = 3,
            **kwargs
    ):
        KosmoyBase.__init__(self, app_id=app_id, api_key=api_key,base_url=base_url,timeout=timeout,
                            max_retries=max_retries)

        CustomOpenAIEmbeddings.__init__(
            self,
            base_url=f"{self.gateway_config.base_url}/gateway/invoke",
            api_key=api_key,
            model=model,
            check_embedding_ctx_length=False,  # Disable context length check for embeddings
            default_headers={
                "app-id": app_id,
                "api-key": api_key,
                "use_guardrails": str(use_guardrails),
                "Content-Type": "application/json",
            },
            **kwargs
        )

        
