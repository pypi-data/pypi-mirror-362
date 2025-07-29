from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from kosmoy_sdk.environment import KOSMOY_URL

class BaseResponseModel(BaseModel):
    """Base response model that contains common fields for API responses"""
    status: str = Field(default="success")
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class CreatedByResponse(BaseModel):
    id: int
    first_name: Optional[str] = Field(None, alias='first_name')
    last_name: Optional[str] = Field(None, alias='last_name')
    email: str
    role: str

class ModelsSimpleResponse(BaseModel):
    id: int
    service_config_id: int
    name: str
    cost_input_token: float
    cost_output_token: float
    model_display_name: str
    model_input: Optional[list[str]] = Field(None, alias='model_input')
    model_output: Optional[list[str]] = Field(None, alias='model_output')
    description: Optional[str] = Field(None, alias='description')
    config_params: Optional[dict] = Field(None, alias='config_params')

class GatewayBase(BaseModel):
    name: str
    description: Optional[str] = None

class Gateway(GatewayBase):
    id: int
    created_at: datetime
    created_by_user: Optional[CreatedByResponse] = Field(None, alias='created_by_user')


class GuardrailBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None, alias='description')


class RouterSimpleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = Field(None, alias='description')
    error_message: Optional[str] = Field(None, alias='error_message')
    primary_model_id: int
    secondary_model_id: int
    router_type: str
    created_by_user: Optional[CreatedByResponse] = Field(None, alias='created_by_user')

class GatewayDetail(Gateway):
    models: List[ModelsSimpleResponse]
    guardrails: Optional[List[GuardrailBase]] = Field(None, alias='guardrails')
    routers: Optional[List[RouterSimpleResponse]] = Field(None, alias="routers")

class CodedAppBase(BaseModel):
    name: str
    description: Optional[str] = None
    gateway_id: int

class CodedApp(CodedAppBase):
    id: int
    created_at: datetime
    created_by_user: CreatedByResponse

class CodedAppDetail(CodedApp):
    gateway: GatewayDetail

class GatewayConfig(BaseModel):
    """Configuration model for the Gateway client"""
    app_id: str
    api_key: str
    environment: str = KOSMOY_URL
    timeout: int = 30
    max_retries: int = 3
    base_url: str
