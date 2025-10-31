import db_connect as dc


def get_group(id: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", id).execute()

    if len(response.data) > 0:
        return response.data[0]
    else:
        return None


def chat_area_base(name: str) -> dict:
    return {
        "name": name,
        "messages": []
    }


def create_group(group_name: str, user_id: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("name", group_name).execute()

    if len(response.data) > 0:
        return None
    
    response = dc.db_client.table("group_data").insert({
        "name": group_name,
        "members": [],
        "moderators": [user_id],
        "chat_areas": [chat_area_base("general")]
    }).execute()

    return response.data[0]


def add_member(group_id: str, user_id: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]
    moderators: list = group_data["moderators"]

    if user_id in members:
        return None

    if user_id in moderators:
        moderators.remove(user_id)

    members.append(user_id)

    response = dc.db_client.table("group_data").update({
        "members": members,
        "moderators": moderators
    }).eq("id", group_id).execute()

    return response.data[0]


def remove_member(group_id: str, user_id: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]

    if user_id not in members:
        return None
    
    members.remove(user_id)

    response = dc.db_client.table("group_data").update({
        "members": members
    }).eq("id", group_id).execute()

    return response.data[0]


def add_moderator(group_id: str, user_id: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    group_data: dict = response.data[0]
    members: list = group_data["members"]
    moderators: list = group_data["moderators"]

    if user_id in moderators:
        return None

    if user_id in members:
        members.remove(user_id)

    moderators.append(user_id)

    response = dc.db_client.table("group_data").update({
        "members": members,
        "moderators": moderators
    }).eq("id", group_id).execute()

    return response.data[0]


def remove_moderator(group_id: str, user_id: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    group_data: dict = response.data[0]
    moderators: list = group_data["moderators"]

    if user_id not in moderators:
        return None
    
    moderators.remove(user_id)

    response = dc.db_client.table("group_data").update({
        "moderators": moderators
    }).eq("id", group_id).execute()

    return response.data[0]


def add_chat_area(group_id: str, chat_area_name: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]

    for chat_area in chat_areas:
        if chat_area_name == chat_area["name"]:
            return None
    
    chat_areas.append(chat_area_base(chat_area_name))
    response = dc.db_client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", group_id).execute()

    return response.data[0]


def remove_chat_area(group_id: str, chat_area_name: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True

    for chat_area in chat_areas:
        if chat_area_name == chat_area["name"]:
            chat_areas.remove(chat_area)
            area_missing = False
            break
    
    if area_missing:
        return None
    
    response = dc.db_client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", group_id).execute()
    
    return response.data[0]


def send_message(group_id: str, sender_id: str, chat_area_name: str, message: str) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True

    for chat_area in chat_areas:
        if chat_area_name == chat_area["name"]:
            chat_area["messages"].append({
                "sender_id": sender_id,
                "contents": message
            })
            area_missing = False
            break
    
    if area_missing:
        return None

    response = dc.db_client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", group_id).execute()

    return response.data[0]


def delete_message(group_id: str, sender_id: str, chat_area_name: str, message_index: int) -> dict | None:
    response = dc.db_client.table("group_data").select("*").eq("id", group_id).execute()
    chat_areas: list[dict] = response.data[0]["chat_areas"]
    area_missing = True

    for chat_area in chat_areas:
        if chat_area_name == chat_area["name"]:
            del chat_area["messages"][message_index]
            area_missing = False
            break
    
    if area_missing:
        return None
    
    response = dc.db_client.table("group_data").update({
        "chat_areas": chat_areas
    }).eq("id", group_id).execute()

    return response.data[0]
