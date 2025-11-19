import quart
import supabase
import supabase_auth
from headers import COMMON_HEADERS
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY
from misc_utils import *


user_bp = quart.Blueprint('users', __name__, url_prefix='/users')


@user_bp.route("/get_user", methods=["POST", "OPTIONS"])
async def get_user_full() -> quart.Response | tuple:
    return await request_shell(get_user)


async def get_user(client, data) -> quart.Response | tuple:
    return await client.table("user_data").select("*").eq("id", data["id"]).execute()


@user_bp.route("/login", methods=["POST", "OPTIONS"])
async def authenticate_user_full() -> tuple:
    return await request_shell(authenticate_user, config_user_response)


async def authenticate_user(client, data):
    response = await client.auth.sign_in_with_password({
        "email": data["email"],
        "password": data["password"]
    })
    
    return response.user.id, response.session


@user_bp.route("/new_user", methods=["POST", "OPTIONS"])
async def create_user_full() -> dict | int:
    return await request_shell(create_user, config_user_response)


async def create_user(client: supabase.Client, data: dict) -> dict | int:
    response = await client.auth.sign_up({
        "email": data["email"],
        "password": data["password"]
    })
    
    await client.table("user_data").insert({
        "id": response.user.id,
        "email": data["email"],
        "username": data["username"],
        "password": data["password"]
    }).execute()
    
    return response.user.id, response.session


@user_bp.route("/update_user_settings", methods=["POST", "OPTIONS"])
async def update_user_settings_full():
    return await request_shell(update_user_settings)


async def update_user_settings(client, data):
    await client.table("user_data").update({
        "description": data["description"],
        "tags": data["tags"]
    }).eq("id", data["id"]).execute()

    return None
