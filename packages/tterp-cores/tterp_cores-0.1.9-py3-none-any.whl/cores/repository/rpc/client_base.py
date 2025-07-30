from io import BytesIO
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException, status

from cores.config import service_config
from cores.logger.logging import ApiLogger


class ClientBase:
    _app = None
    _base_url: str = ""
    _jwt_token: str = ""
    _headers: Dict[str, str] = {}

    async def set_jwt_token_and_headers(self, target_service_id: str) -> None:
        from cores.depends.authorization import AuthService

        self._jwt_token = AuthService.create_auth_token(
            service_config.AUTH_SECRET_KEY
        )
        self._headers = {
            "service-management-id": service_config.BASE_SERVICE_ID,
            "target-service-id": target_service_id,
            "user-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzY2MTc5MzM1fQ.-yJYMqF6jTC2VA5WC7WYNHwsmZJ1uCDyQYqngxvYSaI",
            # "user-token": await AuthService.create_user_token(
            #     service_config
            # ),
        }
        # ApiLogger.debug(
        #     f"RPCClientBase initialized with _jwt_token: {self._jwt_token}"
        # )
        # ApiLogger.debug(
        #     f"RPCClientBase initialized with _headers: {self._headers}"
        # )

    async def curl_api(
        self,
        method: str = "GET",
        uri: str = "",
        body: Dict = {},
        params: Dict = {},
        response_type: str = "json",
        external_headers: Optional[Dict] = None,
    ) -> Any:
        headers = self._prepare_headers(external_headers)
        url = f"{self._base_url}{uri}"

        async with httpx.AsyncClient(
            timeout=10, headers=headers, app=self._app
        ) as client:
            try:
                response = await self._make_request(
                    client, method, url, body, params
                )
                return await self._handle_response(
                    response, response_type, url, method, params
                )
            except httpx.RequestError as exc:
                await self._log_error(exc, url, method, params, "RequestError")
                raise
            except Exception as exc:
                await self._log_error(exc, url, method, params, "Exception")
                raise

    def _prepare_headers(
        self, external_headers: Optional[Dict]
    ) -> Dict[str, str]:
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if self._jwt_token:
            headers["Authorization"] = f"Bearer {self._jwt_token}"
        headers.update(self._headers)
        if external_headers:
            headers.update(external_headers)
        return headers

    async def _make_request(
        self,
        client: httpx.AsyncClient,
        method: str,
        url: str,
        body: Dict,
        params: Dict,
    ) -> httpx.Response:
        method = method.upper()
        methods = {
            "GET": lambda: client.get(url, params=params),
            "POST": lambda: client.post(url, json=body, params=params),
            "PUT": lambda: client.put(url, json=body, params=params),
            "PATCH": lambda: client.patch(url, json=body, params=params),
            "DELETE": lambda: client.request("DELETE", url, json=body),
        }

        if method not in methods:
            raise ValueError(f"Unsupported HTTP method: {method}")
        return await methods[method]()

    async def _handle_response(
        self,
        response: httpx.Response,
        response_type: str,
        url: str,
        method: str,
        params: Dict,
    ) -> Any:
        if not 200 <= response.status_code <= 202:
            ApiLogger.logging_curl(
                f"{url}, method: {method} failed with status "
                f"{response.status_code}. {response.text}"
            )

        if response_type == "binary":
            if response.status_code == 200:
                return BytesIO(response.content)
            raise HTTPException(
                status_code=response.status_code, detail=response.text
            )
        return self._process_json_response(response)

    def _process_json_response(self, response: httpx.Response) -> Dict:
        try:
            result = response.json()
            if isinstance(result, dict) and "status_code" not in result:
                result["status_code"] = response.status_code
            return result
        except ValueError:
            ApiLogger.logging_curl(
                f"DecodingError for response: {response.text}"
            )
            raise

    async def _log_error(
        self,
        exc: Exception,
        url: str,
        method: str,
        params: Dict,
        error_type: str,
    ) -> None:
        error_message = f"{error_type} for {url}, method: {method},"
        "params: {params} - {str(exc)}"
        ApiLogger.logging_curl(error_message)

    async def multipart_request(
        self, uri: str = "", data: list = [], files: Any = None
    ) -> Dict:
        headers = {
            "Authorization": f"Bearer {self._jwt_token}",
            "X-Requested-With": "XMLHttpRequest",
        }
        url = f"{self._base_url}{uri}"

        async with httpx.AsyncClient(
            timeout=10, headers=headers, app=self._app
        ) as client:
            try:
                response = await client.post(url, data=data, files=files)
                if response.status_code == 502:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Service is unavailable.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                result = response.json()
                result["status_code"] = response.status_code
                return result
            except httpx.HTTPStatusError as exc:
                await self._log_error(exc, url, "POST", {}, "HTTPStatusError")
                raise
            except httpx.RequestError as exc:
                await self._log_error(exc, url, "POST", {}, "RequestError")
                raise

    async def curl_api_with_auth(
        self,
        auth_init,
        method: str = "GET",
        uri: str = "",
        body: Dict = {},
        params: Dict = {},
        response_type: str = "json",
        external_headers: Optional[Dict] = None,
    ) -> Any:
        await auth_init()
        return await self.curl_api(
            method, uri, body, params, response_type, external_headers
        )
