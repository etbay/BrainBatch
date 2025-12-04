import quart
import supabase
from headers import COMMON_HEADERS
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY
from misc_utils import *


group_bp = quart.Blueprint('groups', __name__, url_prefix='/groups')


def chat_area_base(name: str) -> dict:
    return {
        "name": name,
        "messages": []
    }


@group_bp.route("/get_group", methods=["POST", "OPTIONS"])
async def get_group_full() -> quart.Response | tuple:
    """Gets the group of the specified id. Use "id" to specify the group id to search for.
    Returns a full group object.
    """
    return await request_shell(get_group)

async def get_group(client, data) -> quart.Response | tuple:
    return await client.table("group_data").select("*").eq("id", data["id"]).execute()

@group_bp.route("/get_all_groups", methods=["POST", "OPTIONS"])
async def get_all_groups_full() -> quart.Response | tuple:
    """Gets all groups that a user has access to. Returns a list of group objects."""
    return await request_shell(get_all_groups)

async def get_all_groups(client, data) -> quart.Response | tuple:
    try:
        user_id = data.get("user_id")
        print("Querying group_data table")
        response = await client.table("group_data").select("*").contains("members", [user_id]).execute()
        print("Query result:", response.data)
        return response
    except Exception as e:
        print(f"Database query failed: {e}")
        raise

@group_bp.route("/get_joinable_groups", methods=["POST", "OPTIONS"])
async def get_joinable_groups_full() -> quart.Response | tuple:
    """Gets all groups that the user is not a member of and have an empty password."""
    return await request_shell(get_joinable_groups)

async def get_joinable_groups(client, data) -> quart.Response | tuple:
    try:
        user_id = data.get("user_id")
        print(f"Received user_id: {user_id}")

        response = await client.table("group_data").select("*").execute()
        groups = response.data or []

        joinable = []
        for g in groups:
            members = g.get("members") or []
            password = g.get("password")
            if user_id not in members and (password is None or password == ""):
                joinable.append(g)

        response.data = joinable
        return response
    except Exception as e:
        print(f"Error in get_joinable_groups: {e}")
        raise

@group_bp.route("/new_group", methods=["POST", "OPTIONS"])
async def create_group_full() -> quart.Response | tuple:
    """Creates a new group. Use "group_name" to specify the name and "creator_id" to specify the id of the creator.
    Returns a full group object.
    """
    return await request_shell(create_group)


async def create_group(client, data) -> quart.Response | tuple:
    return await client.table("group_data").insert({
        "name": data["group_name"],
        "moderators": [data["creator_id"]],
        "members": [data["creator_id"]],
        "chat_areas": [chat_area_base("General")]
    }).execute()


@group_bp.route("/add_member", methods=["POST", "OPTIONS"])
async def add_member_full() -> quart.Response | tuple:
    """Adds a member to the specified group. Note that if the new member is a moderator,
    then they will be removed from the moderators list. Use "group_id" to specify the id of the group
    and "user_id" to specify the id of the new member. Returns a full group object.
    """
    return await request_shell(add_member)


async def add_member(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]
    moderators: list = group_data["moderators"]

    if data["user_id"] in members:
        raise ValueError("User was already a member.")

    if data["user_id"] in moderators:
        moderators.remove(data["user_id"])

    members.append(data["user_id"])

    return await client.table("group_data").update({
        "members": members,
        "moderators": moderators
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/remove_member", methods=["POST", "OPTIONS"])
async def remove_member_full() -> quart.Response | tuple:
    """Removes a member from the specified group. Use "group_id" to specify the id of the group
    and "user_id" to specify the id of the user to remove. Returns a full group object.
    """
    return await request_shell(remove_member)


async def remove_member(client, data):
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]

    if data["user_id"] not in members:
        raise ValueError("User was already not a member")
    
    members.remove(data["user_id"])

    return await client.table("group_data").update({
        "members": members
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/add_moderator", methods=["POST", "OPTIONS"])
async def add_moderator_full() -> quart.Response | tuple:
    """Adds a moderator to the specified group. Note that if the new moderator is already a member,
    then they will be removed from the members list. Use "group_id" to specify the id of the group
    and "user_id" to specify the id of the new moderator. Returns a full group object.
    """
    return await request_shell(add_moderator)


async def add_moderator(client, data):
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]
    moderators: list = group_data["moderators"]

    if data["user_id"] in moderators:
        raise ValueError("User was already a moderator.")

    if data["user_id"] in members:
        members.remove(data["user_id"])

    moderators.append(data["user_id"])

    return await client.table("group_data").update({
        "members": members,
        "moderators": moderators
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/remove_moderator", methods=["POST", "OPTIONS"])
async def remove_moderator_full() -> quart.Response | tuple:
    """Remove the moderator from the specified group. Use "group_id" to specify the group
    and "user_id" to specify the moderator to remove. Returns a full group object.
    """
    return await request_shell(remove_moderator)


async def remove_moderator(client, data):
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    moderators: list = group_data["moderators"]

    if data["user_id"] not in moderators:
        raise ValueError("User was already not a moderator.")
    
    moderators.remove(data["user_id"])

    return await client.table("group_data").update({
        "moderators": moderators
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/add_chat_area", methods=["POST", "OPTIONS"])
async def add_chat_area_full() -> quart.Response | tuple:
    """Adds a chat area to the specifie group. Note that two chat areas cannot be of the same name.
    Use "group_id" to specify the group and "chat_area_name" to specify the name of the new area.
    Returns a full group object.
    """
    return await request_shell(add_chat_area)


async def add_chat_area(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]

    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            return ValueError("Chat area already existed")
    
    chat_areas.append(chat_area_base(data["chat_area_name"]))
    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/remove_chat_area", methods=["POST", "OPTIONS"])
async def remove_chat_area_full() -> quart.Response | tuple:
    """Removes the chat area from the specified group. Use "group_id" to specify the group
    and "chat_area_name" to specify the area's name to remove.
    Returns a full group object.
    """
    return await request_shell(remove_chat_area)


async def remove_chat_area(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True

    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            chat_areas.remove(chat_area)
            area_missing = False
            break
    
    if area_missing:
        return ValueError("Chat area already doesn't exist")
    
    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/send_message", methods=["POST", "OPTIONS"])
async def send_message_full() -> quart.Response | tuple:
    """Sends a message in the specified chat area of the specified group. Use "group_id" to specify the group,
    "chat_area_name" to specify the name of the chat area, "message" to specify the message text,
    and "sender_id" to specify the user sending the message.
    Returns a full group object.
    """
    return await request_shell(send_message)


async def send_message(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True

    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            chat_area["messages"].append({
                "sender_id": data["sender_id"],
                "contents": data["message"]
            })

            area_missing = False
            break
    
    if area_missing:
        return ValueError("Chat area does not exist")

    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/delete_message", methods=["POST", "OPTIONS"])
async def delete_message_full() -> quart.Response | tuple:
    """Deletes a message from the specified group. Use "group_id" to specify the group,
    "chat_area_name" to specify the name of the area to remove from,
    and "message_index" to specify the index of the message to remove.
    Returns a full group object.
    """
    return await request_shell(delete_message)


async def delete_message(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True
    
    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            if data["message_index"] < 0 and data["message_index"] >= len(chat_area["messages"]):
                return IndexError("Message index out of range.")

            del chat_area["messages"][data["message_index"]]
            area_missing = False
            break
    
    if area_missing:
        return ValueError("Chat area does not exist.")
    
    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()
