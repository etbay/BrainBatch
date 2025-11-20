# This file contains headers used for Flaks responses.

# Headers used in all non-OPTIONS responses (e.g. for CORS)
COMMON_HEADERS = {
    "Access-Control-Allow-Origin": "*",
}

# Headers for preflight OPTIONS requests for most POST endpoints.
POST_PREFLIGHT_HEADERS = {
    "Allow": "POST, OPTIONS",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "*"
}
