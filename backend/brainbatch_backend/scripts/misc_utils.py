import quart
import supabase
from headers import *
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY


def affirm_request() -> tuple | None:
    # Process OPTIONS and non-POST requests
    if quart.request.method == "OPTIONS":
        return "", 204, POST_PREFLIGHT_HEADERS
    if quart.request.method != "POST":
        return quart.jsonify({"error": "This endpoint only accepts POST requests."}), 405, COMMON_HEADERS
    
    return None


def config_response(response_data: quart.Response) -> quart.Response:
    response = quart.jsonify(response_data.data[0])
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response


def make_error(message, code):
    return quart.jsonify({"success": False, "error": message}), code, COMMON_HEADERS


async def request_shell(action):
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        response = await action(supa, data)
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS
    
    return config_response(response)
