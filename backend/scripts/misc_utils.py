import quart
import supabase
from headers import *
from app_globals import *
from collections.abc import Callable
import supabase_auth.errors as supa_errors


def affirm_request() -> tuple[str | quart.Response, int, dict[str, str]] | None:
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


def make_error(message: str, code: int) -> tuple[quart.Response, int, dict[str, str]]:
    return quart.jsonify({"success": False, "error": message}), code, COMMON_HEADERS


async def request_shell(action: Callable, response_config: Callable = config_response) -> quart.Response | tuple[quart.Response, int, dict[str, str]]:
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
    result = affirm_request()

    if result is not None:
        return result

    # Create the client, and acquire the data.
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward database interfacing to Supabase.
    try:
        result = await action(supa, data)
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": str(e)}), 500, COMMON_HEADERS
    
    # Configure the final result of the request.
    return response_config(result)
