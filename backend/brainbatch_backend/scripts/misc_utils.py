import quart
import supabase
from headers import *
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY


def affirm_request(http_method="POST") -> quart.Response | None:
    """Generates a response for requests that do not match the canonical HTTP method for the endpoint."""

    # Process OPTIONS and non-POST requests
    if quart.request.method == "OPTIONS":
        resp = quart.make_response("", 204, get_preflight_headers(http_method))
    if quart.request.method != http_method:
        resp = quart.jsonify({"success": False, "error": f"This endpoint only accepts {http_method} requests."})
        resp.status_code = 405
        resp.headers.extend(get_preflight_headers(http_method))
        return resp
    
    return None



async def config_response(response_info: quart.Response) -> quart.Response:
    response = quart.jsonify({"success": True, "data": (await response_info.data)[0]})
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


def make_error(message, code):
    response = quart.jsonify({"success": False, "error": message})
    response.status_code = code
    response.headers.extend(COMMON_HEADERS)
    return response


async def request_shell(action, response_config = config_response) -> quart.Response:
    """Handles the variables and tasks around the specified action.

    Args:
        action (Callable): The functon to call that interfaces with the database.
        The input parameters should include the client and then the data.
        response_config (Callable): The function to call for configuring the final response result.
        Should only be either config_response, or config_user_response. Defaults to the config_response function.
    
    Returns:
        quart.Response: Either the response that was sent by the specified action,
        or a tuple containing error details.
    """
    # Affirm that the request is valid.
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
        return make_error("Unspecified internal server error.", 500)
    
    return response_config(result)
