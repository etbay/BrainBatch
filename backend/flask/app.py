import flask
import supabase
import supabase_auth
import supabase_auth.errors as supa_errors
import os
from headers import *
from dotenv import load_dotenv

# Environment variables should be placed in a ".env" file.
load_dotenv()
SUPA_URL: str = os.environ.get("SUPABASE_URL")
SUPA_KEY: str = os.environ.get("SUPABASE_KEY")

app = flask.Flask(__name__)


@app.route("/login", methods=["POST", "OPTIONS"])
async def userlogin():
    # Process OPTIONS and non-POST requests
    if flask.request.method == "OPTIONS":
        return "", 204, POST_PREFLIGHT_HEADERS
    if flask.request.method != "POST":
        return flask.jsonify({"error": "This endpoint only accepts POST requests."}), 405, COMMON_HEADERS
    
    supa: supabase.AsyncClient = await supabase.create_async_client(SUPA_URL, SUPA_KEY)
    data = flask.request.json
    # Forward authentication to Supabase
    try:
        supa_response = await supa.auth.sign_in_with_password({
            "email": data["username"],
            "password": data["password"]
        })
        user_id = supa_response.user.id
        user_session: supabase_auth.Session = supa_response.session
    except supa_errors.AuthApiError as e:
        return flask.jsonify({"success": False, "error": e.code}), 200, COMMON_HEADERS
    except BaseException as e:
        return flask.jsonify({"success": False, "error": "Internal server error"}), 500, COMMON_HEADERS
    
    response = flask.jsonify({"success": True, "uuid": user_id})
    # Set cookies for auth session
    response.set_cookie("sb-access-token", user_session.access_token, max_age=user_session.expires_in)
    response.set_cookie("sb-refresh-token", user_session.refresh_token, max_age=user_session.expires_in)
    response.headers.extend(COMMON_HEADERS)
    response.status_code = 200
    return response