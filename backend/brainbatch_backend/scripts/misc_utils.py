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


def config_response(response_info: quart.Response) -> quart.Response | None:
    if len(response_info.data) > 0:
        response = quart.jsonify({"success": True, "data": response_info.data[0]})
        response.headers.extend(COMMON_HEADERS)
        response.status_code = 200
        return response
    else:
        return make_error("No data returned.", 200)


def config_user_response(response_info: tuple) -> quart.Response:
    response = quart.jsonify({"success": True, "data": {"id": response_info[0]}})
    response.set_cookie("sb-access-token", response_info[1].access_token, max_age= response_info[1].expires_in)
    response.set_cookie("sb-refresh-token",  response_info[1].refresh_token, max_age= response_info[1].expires_in)
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response


def make_error(message, code):
    return quart.jsonify({"success": False, "error": message}), code, COMMON_HEADERS


<<<<<<< Updated upstream:backend/brainbatch_backend/scripts/misc_utils.py
async def request_shell(action, response_config = config_response):
=======
async def request_shell(action: Callable, response_config: Callable = config_response) -> quart.Response | tuple[quart.Response, int, dict[str, str]] | None:
    """Handles the variables and tasks around the specified action.

    Args:
        action (Callable): The functon to call that interfaces with the database.
        The input parameters should include the client and then the data.
        response_config (Callable): The function to call for configuring the final response result.
        Should only be either config_response, or config_user_response. Defaults to the config_response function.
    
    Returns:
        quart.Response | tuple[Response, int, dict[str, str]]: Either the response that was sent by the specified action,
        or a tuple containing error details.
    """
    # Affirm that the request is valid.
>>>>>>> Stashed changes:backend/scripts/misc_utils.py
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        result = await action(supa, data)
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": str(e)}), 500, COMMON_HEADERS
    
    return response_config(result)
