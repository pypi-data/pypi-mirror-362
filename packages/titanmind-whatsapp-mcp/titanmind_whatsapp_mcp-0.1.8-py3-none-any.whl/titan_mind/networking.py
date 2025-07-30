import json

from titan_mind.utils.app_specific.mcp import get_the_api_key, get_the_business_code

_titan_engage_base_base_url = 'https://api.titanmind.so'
_titan_engage_base_url = f'{_titan_engage_base_base_url}/api/'


def get_titan_engage_headers() -> dict:
    return {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'authorization': f'API-Key {get_the_api_key()}',
        'x-business-code': f'{get_the_business_code()}',
    }


def get_titan_engage_url(endpoint: str):
    return f"{_titan_engage_base_url}{endpoint}"


def print_request_and_response(response):
    """
    Accepts a requests.Response object and prints details of both the
    request that generated it and the response itself.
    Then, it returns the original response object.

    Args:
        response: The requests.Response object to print details for.

    Returns:
        The original requests.Response object.
    """
    # --- Print Request Details ---
    print("-" * 30)
    print("REQUEST SENT:")
    print("-" * 30)
    print(f"Method: {response.request.method}")
    print(f"URL: {response.request.url}")
    print("Headers:")
    for header, value in response.request.headers.items():
        print(f"  {header}: {value}")
    if response.request.body:
        # Decode body for readability if it's bytes (e.g., from POST requests)
        try:
            print(f"Body: {response.request.body.decode('utf-8')}")
        except AttributeError:
            print(f"Body: {response.request.body}")  # Already string or None
    else:
        print("Body: (No body for GET request)")
    print("\n")

    # --- Print Response Details ---
    print("-" * 30)
    print("RESPONSE RECEIVED:")
    print("-" * 30)
    print(f"Status Code: {response.status_code}")
    print(f"Reason: {response.reason}")  # e.g., "OK", "Not Found"
    print("Headers:")
    for header, value in response.headers.items():
        print(f"  {header}: {value}")

    print("\nBody (JSON/Text):")
    try:
        response_json = response.json()
        print(json.dumps(response_json, indent=2))
    except json.JSONDecodeError:
        print(response.text)
    print("\n")

    return response
