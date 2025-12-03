import quart
import supabase
import supabase_auth.errors as supa_errors
from app_globals import *


def affirm_request(http_method="POST") -> quart.Response | None:
    """Generates a response for requests that do not match the canonical HTTP method for the endpoint."""

    if quart.request.method == "OPTIONS":
        return quart.Response(status=204)
    if quart.request.method != http_method:
        resp = quart.jsonify({"success": False, "error": f"This endpoint only accepts {http_method} requests."})
        resp.status_code = 405
        return resp
    
    return None


async def config_response(response_info: quart.Response) -> quart.Response:
    # `response_info.data` can be an awaitable in some contexts or a plain
    # object (list/bytes). Avoid awaiting a list (TypeError). Handle both
    # awaitable and non-awaitable values, parse bytes/JSON when appropriate,
    # and return the first element if the data is a sequence.
    data_attr = getattr(response_info, "data", None)

    if data_attr is not None and hasattr(data_attr, "__await__"):
        data_content = await data_attr
    elif data_attr is not None:
        data_content = data_attr
    else:
        data_content = None

    # If bytes, try to decode + parse JSON; otherwise leave as-is.
    if isinstance(data_content, (bytes, bytearray)):
        try:
            import json

            data_parsed = json.loads(data_content)
        except Exception:
            try:
                data_parsed = data_content.decode("utf-8")
            except Exception:
                data_parsed = data_content
    else:
        data_parsed = data_content

    # If the parsed data is a sequence, return its first element (if present).
    if isinstance(data_parsed, (list, tuple)) and data_parsed:
        data_to_return = data_parsed[0]
    else:
        data_to_return = data_parsed

    response = quart.jsonify({"success": True, "data": data_to_return})
    response.status_code = 200
    return response

async def config_dict_response(response_info: dict) -> quart.Response:
    response = quart.jsonify({"success": True, "data": response_info})
    response.status_code = 200
    return response

async def config_user_response(response_info: tuple) -> quart.Response:
    response = quart.jsonify({"success": True, "data": {"id": response_info[0]}})
    response.set_cookie("sb-access-token", response_info[1].access_token, max_age= response_info[1].expires_in)
    response.set_cookie("sb-refresh-token",  response_info[1].refresh_token, max_age= response_info[1].expires_in)
    response.status_code = 200
    return response


def make_error(message: str, code: int) -> quart.Response:
    """Return an error response with the given HTTP status code.
    The given message is included in the response JSON."""
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
        return await response_config(result)
