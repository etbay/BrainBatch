import quart
import supabase
from misc_utils import *
import multidict


user_bp = quart.Blueprint('users', __name__, url_prefix='/users')


"""Note that a full user object is a row of data from the user_data table.
To see the columns/elements of said row/object, go onto the supabase Brain Batch project.
"""

@user_bp.route("/test")
def test():
    return "Hello World!"


@user_bp.route("/get_user", methods=["POST", "OPTIONS"])
async def get_user_full() -> quart.Response | tuple:
    """Gets the user of the specified id. Use "id" to specify the id of the user.
    Returns a full user object.
    """
    return await request_shell(get_user)


async def get_user(client: supabase.Client, data) -> quart.Response | tuple:
    return await client.table("user_data").select("*").eq("id", data["id"]).execute()


@user_bp.route("/login", methods=["POST", "OPTIONS"])
async def authenticate_user_full() -> tuple:
    """Authenticates the user with their email and password. Use "email" to specify the user's email
    and "password" to specify the user's password. Returns the user's id and sign up session.
    """
    return await request_shell(authenticate_user, config_user_response)


async def authenticate_user(client, data):
    response = await client.auth.sign_in_with_password({
        "email": data["email"],
        "password": data["password"]
    })

    return response.user.id, response.session


@user_bp.route("/new_user", methods=["POST", "OPTIONS"])
async def create_user_full() -> dict | int:
    """Creates a new user. Use "username" to specify the username, "email" to specify the email,
    and "password" to specify the password. Returns the user's id and sign up session.
    """
    return await request_shell(create_user, config_user_response)


async def create_user(client: supabase.Client, data: dict) -> tuple:
    sign_up_response = await client.auth.sign_up({
        "email": data["email"],
        "password": data["password"]
    })
    
    name_response = await client.table("user_data").select("*").eq("username", data["username"]).execute()
    if len(name_response.data) > 0:
        raise ValueError("Username already exists.")

    await client.table("user_data").insert({
        "id": sign_up_response.user.id,
        "email": data["email"],
        "username": data["username"]
    }).execute()
    
    return sign_up_response.user.id, sign_up_response.session


@user_bp.route("/update_user_settings", methods=["POST", "OPTIONS"])
async def update_user_settings_full():
    """Updates the settings of the specified user. Use "description" to specify the user's description
    and "tags" to specify the user's tags. Returns a full user object.
    """
    return await request_shell(update_user_settings)


async def update_user_settings(client, data):
    return await client.table("user_data").update({
        "description": data["description"],
        "tags": data["tags"]
    }).eq("id", data["id"]).execute()


@user_bp.route("/email_code", methods=["GET", "OPTIONS"])
async def email_code_full():
    """Sends a reset password code to the user's email. This is a GET request, so specify the email like so:
    backend_url/users/email_code?email=<user_email>
    """
    return await request_shell(email_code, config_dict_response, input_type="args", req_type="GET")


async def email_code(client: supabase.Client, data: multidict.MultiDict):
    email = data.get("email", type=str)
    await client.auth.sign_in_with_otp({"email": email})


@user_bp.route("/reset_password", methods=["POST", "OPTIONS"])
async def reset_password_full():
    """Resets the user password with the given email and token/code.
    Use email and token to specify the values.
    """
    return await request_shell(reset_password, config_dict_response)


async def reset_password(client: supabase.Client, data: dict):
    await client.auth.verify_otp({
        "email": data["email"],
        "token": data["token"],
        "type": "email"
    })
    await client.auth.update_user({"password": data["new_password"]})
