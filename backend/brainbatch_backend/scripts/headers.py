# This file contains headers used for Quart responses.

# Headers used in all non-OPTIONS responses (e.g. for CORS)
COMMON_HEADERS = {
    "Access-Control-Allow-Origin": "*",
}

# Common headers for preflight OPTIONS requests.
PREFLIGHT_HEADERS = {
    "Allow": "POST, OPTIONS",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "*"
}

# Headers for preflight OPTIONS requests for most POST endpoints.
POST_PREFLIGHT_HEADERS = {
    "Allow": "POST, OPTIONS",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "*"
}

def get_preflight_headers(http_method="POST"):
    """Returns the headers to be returned for preflight OPTIONS requests.
    http_method is the normal HTTP method this endpoint accepts (e.g. GET, POST)."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
    }
    headers["Allow"] = f"{http_method}, OPTIONS"
    headers["Access-Control-Allow-Methods"] = f"{http_method}, OPTIONS"
    return headers
