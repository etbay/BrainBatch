import quart
import supabase
from headers import COMMON_HEADERS
import supabase_auth.errors as supa_errors
from app_globals import SUPA_URL, SUPA_KEY
from misc_utils import *


group_bp = quart.Blueprint('users', __name__, url_prefix='/users')


def chat_area_base(name: str) -> dict:
    return {
        "name": name,
        "messages": []
    }


@group_bp.route("/get_user", methods=["POST", "OPTIONS"])
async def get_group() -> quart.Response | tuple:
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        response = await supa.table("group_data").select("*").eq("id", data["id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS
    
    response = quart.jsonify(response.data[0])
    return config_response(response)


@group_bp.route("/get_user", methods=["POST", "OPTIONS"])
async def create_group() -> quart.Response | tuple:
    result = affirm_request()

    if result is not None:
        return result
    
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json

    # Forward authentication to Supabase
    try:
        response = await supa.table("group_data").insert({
            "name": data["name"],
            "moderators": data["creator_id"]
        })
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    response = quart.jsonify({"success": True, "group_id": response.data[0]["id"]})
    return config_response(response)


@group_bp.route("/add_member", methods=["POST", "OPTIONS"])
async def add_member() -> quart.Response | tuple:
    result = affirm_request()

    if result is not None:
        return result
    
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        response = await supa.table("group_data").select("*").eq("id", data["group_id"]).execute()
        group_data: dict = response.data[0]
        members: list = group_data["members"]
        moderators: list = group_data["moderators"]

        if data["user_id"] in members:
            return quart.jsonify({"success": False, "error": "User was already a member"}), 200, COMMON_HEADERS

        if data["user_id"] in moderators:
            moderators.remove(data["user_id"])

        members.append(data["user_id"])

        response = await supa.table("group_data").update({
            "members": members,
            "moderators": moderators
        }).eq("id", data["user_id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    response = quart.jsonify({"success": True, "group_id": data["group_id"]})
    return config_response(response)


@group_bp.route("/remove_member", methods=["POST", "OPTIONS"])
async def remove_member() -> quart.Response | tuple:
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    # Forward authentication to Supabase
    try:
        response = await supa.table("group_data").select("*").eq("id", data["group_id"]).execute()
        group_data: dict = response.data[0]
        members: list = group_data["members"]

        if data["user_id"] not in members:
            return quart.jsonify({"success": False, "error": "User was already not a member"}), 200, COMMON_HEADERS
        
        members.remove(data["user_id"])

        response = await supa.table("group_data").update({
            "members": members
        }).eq("id", data["group_id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    return response.data[0]


@group_bp.route("/add_moderator", methods=["POST", "OPTIONS"])
async def add_moderator() -> quart.Response | tuple:
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    try:
        response = await supa.table("group_data").select("*").eq("id", data["group_id"]).execute()
        group_data: dict = response.data[0]
        members: list = group_data["members"]
        moderators: list = group_data["moderators"]

        if data["user_id"] in moderators:
            return quart.jsonify({"success": False, "error": "User was already a moderator"}), 200, COMMON_HEADERS

        if data["user_id"] in members:
            members.remove(data["user_id"])

        moderators.append(data["user_id"])

        response = await supa.table("group_data").update({
            "members": members,
            "moderators": moderators
        }).eq("id", data["group_id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    return config_response(response)

@group_bp.route("/remove_moderator", methods=["POST", "OPTIONS"])
async def remove_moderator() -> quart.Response | tuple:
    result = affirm_request()

    if result is not None:
        return result

    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = await quart.request.json
    
    try:
        response = await supa.table("group_data").select("*").eq("id", data["group_id"]).execute()
        group_data: dict = response.data[0]
        moderators: list = group_data["moderators"]

        if data["user_id"] not in moderators:
            return quart.jsonify({"success": False, "error": "User was already not a moderator"}), 200, COMMON_HEADERS
        
        moderators.remove(data["user_id"])

        response = await supa.table("group_data").update({
            "moderators": moderators
        }).eq("id", data["group_id"]).execute()
    except supa_errors.AuthApiError as e:
        return quart.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return quart.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS

    return config_response(response)


@group_bp.route("/add_chat_area", methods=["POST", "OPTIONS"])
async def add_chat_area_full() -> quart.Response | tuple:
    return request_shell(add_chat_area)


async def add_chat_area(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]

    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            return make_error("Chat area already existed", 200)
    
    chat_areas.append(chat_area_base(data["chat_area_name"]))
    response = await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()

    return response


@group_bp.route("/remove_chat_area", methods=["POST", "OPTIONS"])
async def remove_chat_area_full() -> quart.Response | tuple:
    return request_shell(remove_chat_area)


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
    return request_shell(send_message)


async def send_message(client, data) -> quart.Response | tuple:
    response = client.table("group_data").select("*").eq("id", data["group_id"]).execute()
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

    response = await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()

    return response.data[0]


@group_bp.route("/delete_message", methods=["POST", "OPTIONS"])
async def delete_message_full() -> quart.Response | tuple:
    return request_shell(delete_message)


async def delete_message(client, data) -> quart.Response | tuple:
    response = await client.table("group_data").select("*").eq("id", data["group_id"]).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True

    for chat_area in chat_areas:
        if data["chat_area_name"] == chat_area["name"]:
            if data["message_index"] < 0 and data["message_index"] < len(chat_area["messages"]):
                return make_error("Message index out of range", 200)

            del chat_area["messages"][data["message_index"]]
            area_missing = False
            break
    
    if area_missing:
        return make_error("Chat area does not exist", 200)
    
    response = await client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", data["group_id"]).execute()

    return response
