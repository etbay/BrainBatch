import quart
import supabase
from headers import *
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY


def affirm_request(req_type="POST") -> tuple | None:
    # Process OPTIONS and non-POST requests
    if quart.request.method == "OPTIONS":
        return make_error("Request method was not of OPTIONS.", 204, POST_PREFLIGHT_HEADERS)
    if quart.request.method != req_type:
        return make_error(f"This endpoint only accepts {req_type} requests.", 405)
    
    return None


def config_response(response_info: quart.Response) -> quart.Response:
    response = quart.jsonify({"success": True, "data": response_info.data[0]})
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response


def config_dict_response(response_info: dict) -> quart.Response:
    response = quart.jsonify({"success": True, "data": response_info})
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


def make_error(message: str, code: int, headers: dict = COMMON_HEADERS):
    response = quart.jsonify({"success": False, "error": message})
    response.headers.extend(headers)
    response.status_code = 200
    return response


async def request_shell(action, response_config = config_response, input_type = "json", req_type = "POST"):
    result = affirm_request(req_type)

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)

    match input_type:
        case "json":
            action_input = await quart.request.json
        case "files":
            action_input = await quart.request.files
        case "args":
            action_input = quart.request.args
        case _:
            return make_error(f"Input type {input_type} was not recognized.", 200)
    
    # Forward authentication to Supabase
    try:
        result = await action(supa, action_input)
    except supa_errors.AuthApiError as e:
        return make_error(e.code, 200)
    except BaseException as e:
        return make_error(str(e), 500)
    
    if response_config is None:
        return result
    else:
        return response_config(result)
