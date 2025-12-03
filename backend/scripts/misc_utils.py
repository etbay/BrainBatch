import quart
import supabase
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY


def affirm_request(http_method="POST") -> quart.Response | None:
    """Generates a response for requests that do not match the canonical HTTP method for the endpoint."""

    # Process OPTIONS and non-POST requests
    if quart.request.method == "OPTIONS":
        resp = quart.make_response("", 204)
    if quart.request.method != http_method:
        resp = quart.jsonify({"success": False, "error": f"This endpoint only accepts {http_method} requests."})
        resp.status_code = 405
        return resp
    
    return None


async def config_response(response_info: quart.Response) -> quart.Response:
    response = quart.jsonify({"success": True, "data": (await response_info.data)[0]})
    response.status_code = 200
    return response


def config_user_response(response_info: tuple) -> quart.Response:
    response = quart.jsonify({"success": True, "data": {"id": response_info[0]}})
    response.set_cookie("sb-access-token", response_info[1].access_token, max_age= response_info[1].expires_in)
    response.set_cookie("sb-refresh-token",  response_info[1].refresh_token, max_age= response_info[1].expires_in)
    response.status_code = 200
    return response


def make_error(message, code):
    response = quart.jsonify({"success": False, "error": message})
    response.status_code = code
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
            action_input = {
                "json": await quart.request.form,
                "files": await quart.request.files
            }
        case "args":
            action_input = quart.request.args
        case _:
            raise ValueError(f"Input type {input_type} was not recognized.")
    
    try:
        result = await action(supa, action_input)
    except supa_errors.AuthApiError as e:
        return make_error(e.code, 400)
    except BaseException as e:
        return make_error(str(e), 500)
    
    if response_config is None:
        return result
    else:
        return response_config(result)
