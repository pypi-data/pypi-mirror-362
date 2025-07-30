from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass, field
from enum import Enum
import requests

from titan_mind.networking import get_titan_engage_headers, get_titan_engage_url, print_request_and_response
from titan_mind.utils.app_specific.utils import to_run_mcp_in_server_mode_or_std_io


# Enums for HTTP methods
class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


# Base response dataclasses
@dataclass
class BaseResponse:
    """Base response structure"""
    status: bool
    message: str
    result: Union[dict[str, Any], list[dict[str, Any]]] = field(default_factory=dict)


class TitanMindAPINetworking:
    def __init__(self):
        self.base_headers = get_titan_engage_headers()

    def make_request(
            self,
            endpoint: str,
            payload: Dict[str, Any],
            success_message: str,
            method: HTTPMethod = HTTPMethod.POST,
            response_processor: Optional[Callable[[Dict[str, Any]], BaseResponse]] = None
    ) -> BaseResponse:
        """Internal method to handle all API requests"""
        response = None
        try:
            url = get_titan_engage_url(endpoint)

            # Use enum for method selection
            if method == HTTPMethod.POST:
                response = requests.post(url, headers=self.base_headers, json=payload)
            elif method == HTTPMethod.GET:
                response = requests.get(url, headers=self.base_headers, params=payload)
            elif method == HTTPMethod.PUT:
                response = requests.put(url, headers=self.base_headers, json=payload)
            elif method == HTTPMethod.DELETE:
                response = requests.delete(url, headers=self.base_headers, json=payload)
            elif method == HTTPMethod.PATCH:
                response = requests.patch(url, headers=self.base_headers, json=payload)
            else:
                return BaseResponse(
                    status=False,
                    message=f"Unsupported HTTP method: {method.value}",
                )

            if to_run_mcp_in_server_mode_or_std_io():
                # for some reason in stdio mode the printing json for a specific api is breaking the whole tool call, for so now disabling it for this mode
                print_request_and_response(response)
            response.raise_for_status()

            response_data = response.json()

            # Apply custom response processing if provided
            if response_processor:
                return response_processor(response_data)

            # Default response
            return BaseResponse(
                status=True,
                message=success_message,
                result=self.get_result_dict(response_data),
            )

        except requests.exceptions.HTTPError as e:
            error_json = {}
            if response is not None:
                try:
                    error_json = response.json()
                except:
                    error_json = {"error": "Could not parse error response", "status_code": response.status_code}

            return BaseResponse(
                status=False,
                message=f"HTTP Error: {str(e)}",
                result=error_json
            )
        except requests.exceptions.RequestException as e:
            return BaseResponse(
                status=False,
                message=f"Request Error: {str(e)}",
                result={"error_type": "RequestException"}
            )
        except Exception as e:
            error_json = {}
            if response is not None:
                try:
                    error_json = response.json()
                except:
                    error_json = {"error": "Could not parse response"}

            return BaseResponse(
                status=False,
                message=f"Unexpected Error: {str(e)}",
                result=error_json
            )

    def get_result_dict(self, response_data):
        return response_data.get("result", response_data)
