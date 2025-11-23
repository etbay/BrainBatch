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
        return quart.jsonify({"success": False, "error": "This endpoint only accepts POST requests."}), 405, COMMON_HEADERS
    
    return None


def config_response(response_info: quart.Response) -> quart.Response:
    response = quart.jsonify({"success": True, "data": response_info.data[0]})
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response


def config_user_response(response_info: tuple) -> quart.Response:
    response = quart.jsonify({"success": True, "data": {"id": response_info[0]}})
    response.set_cookie("sb-access-token", response_info[1].access_token, max_age= response_info[1].expires_in)
    response.set_cookie("sb-refresh-token",  response_info[1].refresh_token, max_age= response_info[1].expires_in)
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response


def make_error(message: str, code: int):
    response = quart.jsonify({"success": False, "error": message})
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response


async def request_shell(action, response_config = config_response):
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        result = await action(supa, data)
    except supa_errors.AuthApiError as e:
        return make_error(e.code, 200)
    except BaseException as e:
        return make_error(str(e), 500)
    
    return response_config(result)
