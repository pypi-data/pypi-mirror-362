from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request as StarletteRequest

def get_the_headers_from_the_current_mcp_request():
    request: StarletteRequest = get_http_request()
    return request.headers