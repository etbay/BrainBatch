import quart
import supabase
import supabase_auth
from headers import COMMON_HEADERS
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY
from misc_utils import affirm_request, config_response


user_bp = quart.Blueprint('users', __name__, url_prefix='/users')


@user_bp.route("/get_user", methods=["POST", "OPTIONS"])
async def get_user() -> tuple:
    result = affirm_request()

    if result is not None:
        return result
    
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        response = await supa.table("user_data").select("*").eq("id", data["id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS
    
    user_data = response.data[0]
    response = quart.jsonify({
        "success": True,
        "username": user_data["username"],
        "password": user_data["password"],
        "description": user_data["description"],
        "tags": user_data["tags"],
        "created_at": user_data["created_at"]
    })

    return config_response(response)


@user_bp.route("/login", methods=["POST", "OPTIONS"])
async def authenticate_user() -> tuple:
    result = affirm_request()

    if result is not None:
        return result
    
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json

    # Forward authentication to Supabase
    try:
        supa_response = await supa.auth.sign_in_with_password({
            "email": data["email"],
            "password": data["password"]
        })
        
        user_id = supa_response.user.id
        user_session: supabase_auth.Session = supa_response.session

        response = await supa.table("user_data").insert({
            "id": user_id,
            "email": data["email"],
            "password": data["password"]
        }).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS
    
    response = quart.jsonify({"success": True, "user_id": user_id})
    # Set cookies for auth session
    response.set_cookie("sb-access-token", user_session.access_token, max_age=user_session.expires_in)
    response.set_cookie("sb-refresh-token", user_session.refresh_token, max_age=user_session.expires_in)
    return config_response(response)


@user_bp.route("/new_user", methods=["POST", "OPTIONS"])
async def create_user() -> dict | int:
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json

    # Forward authentication to Supabase
    try:
        supa_response = await supa.auth.sign_up({
            "email": data["username"],
            "password": data["password"]
        })

        user_id = supa_response.user.id
        user_session: supabase_auth.Session = supa_response.session
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    response = quart.jsonify({"success": True, "user_id": user_id})
    # Set cookies for auth session
    response.set_cookie("sb-access-token", user_session.access_token, max_age=user_session.expires_in)
    response.set_cookie("sb-refresh-token", user_session.refresh_token, max_age=user_session.expires_in)
    return config_response(response)


@user_bp.route("/update_user_settings", methods=["POST", "OPTIONS"])
async def update_user_settings() -> dict | None:
    result = affirm_request()

    if result is not None:
        return result
    
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json

    # Forward authentication to Supabase
    try:
        response = supa.table("user_data").update({
            "description": data["description"],
            "tags": data["tags"]
        }).eq("id", data["id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    response = quart.jsonify({"success": True})
    return config_response(response)
