import quart
import supabase
import supabase_auth
from headers import COMMON_HEADERS
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY
from misc_utils import *


user_bp = quart.Blueprint('users', __name__, url_prefix='/users')


"""Note that a full user object is a row of data from the user_data table.
To see the columns/elements of said row/object, go onto the supabase Brain Batch project.
"""


@user_bp.route("/get_user", methods=["POST", "OPTIONS"])
async def get_user_full() -> quart.Response | tuple:
    """Gets the user of the specified id. Use "id" to specify the user id.
    Returns a full user object.
    """
    return await request_shell(_get_user)


async def _get_user(client, data) -> quart.Response | tuple:
    return await client.table("user_data").select("*").eq("id", data["id"]).execute()


@user_bp.route("/login", methods=["POST", "OPTIONS"])
async def authenticate_user_full():
    """Authenticates a user with their email and passsword.
    Use "email" to specify the email, and "password" to specify the password.
    Returns a user id.
    """
    return await request_shell(_authenticate_user, config_user_response)


async def _authenticate_user(client, data):
    response = await client.auth.sign_in_with_password({
        "email": data["email"],
        "password": data["password"]
    })
    
    return response.user.id, response.session


@user_bp.route("/new_user", methods=["POST", "OPTIONS"])
async def create_user_full():
    """Creates a brand new user. Use "email" to specify the user email,
    "username" to specify the user username, and "password" to specify the password.
    Returns a user id.
    """
    return await request_shell(_create_user, config_user_response)


async def _create_user(client: supabase.Client, data: dict):
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
    """Updates the settings of a user. Use "id" to specify the user's id,
    "description" to specify the user's description, and "tags" to specify the user's tags.
    Returns nothing.
    """
    return await request_shell(_update_user_settings)


async def _update_user_settings(client, data):
    await client.table("user_data").update({
        "description": data["description"],
        "tags": data["tags"]
    }).eq("id", data["id"]).execute()

    return None
