import db_connect as dc


def trim_user(user_data: dict) -> dict:
    return {
        "id": user_data["id"],
        "created_at": user_data["created_at"],
        "username": user_data["username"],
        "email": user_data["email"],
        "description": user_data["description"],
        "tags": user_data["tags"]
    }


def get_user(id: str) -> dict | None:
    response = dc.db_client.table("user_data").select("*").eq("id", id).execute()

    if len(response.data) > 0:
        return trim_user(response.data[0])
    else:
        return None


def authenticate_user(username: str, password: str) -> dict | None:
    response = dc.db_client.table("user_data").select("*").eq("username", username).eq("password", password).execute()

    if len(response.data) > 0:
        return trim_user(response.data[0])
    else:
        return None


def valid_email(email: str) -> bool:
    response = dc.db_client.table("user_data").select("*").eq("email", email).execute()
    return len(response.data) == 0


def create_user(username: str, password: str, email: str) -> dict | int:
    response = dc.db_client.table("user_data").select("*").eq("username", username).execute()

    if len(response.data) > 0:
        return 0
    elif len(password) < 8:
        return 1
    elif not valid_email(email):
        return 2
    
    response = dc.db_client.auth.admin.create_user({
        "email": email
    })
    
    response = dc.db_client.table("user_data").insert({
        "id": response.user.id,
        "username": username,
        "email": email,
        "password": password
    }).execute()

    return trim_user(response.data[0])


def update_user_settings(id: str, new_description: str, new_tags: list[str]) -> dict | None:
    response = dc.db_client.table("user_data").update({
        "description": new_description,
        "tags": new_tags
    }).eq("id", id).execute()

    return trim_user(response.data[0])
