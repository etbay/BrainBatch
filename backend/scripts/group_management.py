import quart
from misc_utils import *
from headers import COMMON_HEADERS


group_bp = quart.Blueprint('groups', __name__, url_prefix='/groups')


def chat_area_base(name: str) -> dict:
    return {
        "name": name,
        "messages": []
    }


@group_bp.route("/get_group", methods=["POST", "OPTIONS"])
async def get_group_full() -> quart.Response | tuple:
    return await request_shell(get_group)


async def get_group(client, data) -> quart.Response | tuple:
    return await client.table("group_data").select("*").eq("id", data["id"]).execute()


@group_bp.route("/new_group", methods=["POST", "OPTIONS"])
async def create_group_full() -> quart.Response | tuple:
    return await request_shell(create_group)


async def create_group(client, data) -> quart.Response | tuple:
    return await client.table("group_data").insert({
        "name": data["group_name"],
        "moderators": [data["creator_id"]],
        "members": [],
        "chat_areas": [chat_area_base("General")]
    }).execute()


@group_bp.route("/add_member", methods=["POST", "OPTIONS"])
async def add_member_full() -> quart.Response | tuple:
    return await request_shell(add_member)


async def add_member(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]
    moderators: list = group_data["moderators"]

    if data["user_id"] in members:
        return make_error("User was already a member", 200)

    if data["user_id"] in moderators:
        moderators.remove(data["user_id"])

    members.append(data["user_id"])

    return await client.table("group_data").update({
        "members": members,
        "moderators": moderators
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/remove_member", methods=["POST", "OPTIONS"])
async def remove_member_full() -> quart.Response | tuple:
    return await request_shell(remove_member)


async def remove_member(client, data):
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]

    if data["user_id"] not in members:
        return make_error("User was already not a member")
    
    members.remove(data["user_id"])

    return await client.table("group_data").update({
        "members": members
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/add_moderator", methods=["POST", "OPTIONS"])
async def add_moderator_full() -> quart.Response | tuple:
    return await request_shell(add_moderator)


async def add_moderator(client, data):
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]
    moderators: list = group_data["moderators"]

    if data["user_id"] in moderators:
        return quart.jsonify({"success": False, "error": "User was already a moderator"}), 200, COMMON_HEADERS

    if data["user_id"] in members:
        members.remove(data["user_id"])

    moderators.append(data["user_id"])

    return await client.table("group_data").update({
        "members": members,
        "moderators": moderators
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/remove_moderator", methods=["POST", "OPTIONS"])
async def remove_moderator() -> quart.Response | tuple:
    return await request_shell(remove_moderator)


async def remove_moderator(client, data):
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    group_data: dict = response.data[0]
    moderators: list = group_data["moderators"]

    if data["user_id"] not in moderators:
        return quart.jsonify({"success": False, "error": "User was already not a moderator"}), 200, COMMON_HEADERS
    
    moderators.remove(data["user_id"])

    return await client.table("group_data").update({
        "moderators": moderators
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/add_chat_area", methods=["POST", "OPTIONS"])
async def add_chat_area_full() -> quart.Response | tuple:
    return await request_shell(add_chat_area)


async def add_chat_area(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]

    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            return make_error("Chat area already existed", 200)
    
    chat_areas.append(chat_area_base(data["chat_area_name"]))
    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/remove_chat_area", methods=["POST", "OPTIONS"])
async def remove_chat_area_full() -> quart.Response | tuple:
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
        return make_error("Chat area already doesn't exist", 200)
    
    response = await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()
    
    return response


@group_bp.route("/send_message", methods=["POST", "OPTIONS"])
async def send_message_full() -> quart.Response | tuple:
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
        return make_error("Chat area does not exist", 200)

    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()


@group_bp.route("/delete_message", methods=["POST", "OPTIONS"])
async def delete_message_full() -> quart.Response | tuple:
    return await request_shell(delete_message)


async def delete_message(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True
    
    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            if data["message_index"] < 0 and data["message_index"] >= len(chat_area["messages"]):
                return make_error("Message index out of range", 200)

            del chat_area["messages"][data["message_index"]]
            area_missing = False
            break
    
    if area_missing:
        return make_error("Chat area does not exist", 200)
    
    return await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()
