from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from kosmoy_sdk.models import (
    GatewayConfig,
    BaseResponseModel,
    CodedAppDetail
)
from kosmoy_sdk.environment import KOSMOY_URL 


class KosmoyBase:
    def __init__(
        self,
        app_id: str,
        api_key: str,
        base_url: Optional[str],
        timeout: int = 30,
        max_retries: int = 3
    ):
        if not base_url:
            base_url = KOSMOY_URL
        if not app_id or not api_key:
            raise ValueError("Both app_id and api_key are required")

        self.gateway_config = GatewayConfig(
            app_id=app_id,
            api_key=api_key,
            timeout=timeout,
            max_retries=max_retries,
            base_url= base_url
        )
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=self.gateway_config.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set authentication headers
        session.headers.update({
            "app-id": self.gateway_config.app_id,
            "api-key": self.gateway_config.api_key,
            "Content-Type": "application/json"
        })
        return session

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.gateway_config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.gateway_config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> BaseResponseModel:
        return BaseResponseModel(
            status="success",
            data=self._make_request("GET", endpoint, params=params, headers=headers)
        )

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> BaseResponseModel:
        return BaseResponseModel(
            status="success",
            data=self._make_request("POST", endpoint, data=data, headers=headers)
        )

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None
    ) -> BaseResponseModel:
        return BaseResponseModel(
            status="success",
            data=self._make_request("PUT", endpoint, data=data, headers=headers)
        )

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> BaseResponseModel:
        return BaseResponseModel(
            status="success",
            data=self._make_request("DELETE", endpoint, headers=headers)
        )

    def get_gateway(self) -> CodedAppDetail:
        """
        Get the gateway details including models and configuration.
        
        Returns:
            CodedAppDetail: Detailed information about the coded app and its associated gateway
        """
        response = self._make_request("GET", "/apps/get")
        return CodedAppDetail.model_validate(response)
