import quart
import supabase
import uuid
from werkzeug.datastructures import FileStorage
from app_globals import *
from misc_utils import *
import multidict


uploads_bp = quart.Blueprint('uploads', __name__, url_prefix='/uploads')


# The file types that are allowed to be uploaded.
# For images/video/audio, I'm restricting it to formats that are widely supported by web browsers.
ALLOWED_FILETYPES = {
    # Documents
    "text/plain": ".txt",
    "application/pdf": ".pdf",
    "text/markdown": ".md",
    "application/x-tex": ".tex",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.oasis.opendocument.text": ".odt",
    "application/vnd.oasis.opendocument.presentation": ".odp",
    "application/vnd.oasis.opendocument.spreadsheet": ".ods",
    "text/csv": ".csv",
    # Images
    "image/png": ".png",
    "image/apng": ".apng",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/avif": ".avif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    # Videos
    "video/mp4": ".mp4",
    "video/webm": ".webm",
    # Audio
    "audio/mpeg": ".mp3",
    "audio/mp4": ".m4a",
    "audio/wav": ".wav",
    "audio/flac": ".flac",
    "audio/ogg": ".ogg"
}


@uploads_bp.route("/upload_file", methods=["POST", "OPTIONS"])
async def upload_file_full():
    """API endpoint for uploading a user file.
    To upload to this endpoint, send a POST request with a FormData body (no JSON) containing a single file.
    Only certain file types are allowed (see ALLOWED_FILETYPES)."""
    return await request_shell(upload_file, config_dict_response, "files")


async def upload_file(client: supabase.AsyncClient, files):
    # Must have a Content-Type of multipart/form-data
    if not quart.request.content_type.startswith("multipart/form-data"):
        raise ValueError("Files must be uploaded as a FormData object.")
    
    if len(files) != 1:
        resp = make_error("The request must contain exactly one file.", 400)
        resp.headers.add("Accept-Post", "multipart/form-data")
        return resp
    
    file: FileStorage = files.getlist(list(files.keys())[0])[0]

    # Check that the file type is allowed
    if not file.mimetype:
        resp = make_error("The uploaded file must have a valid MIME type.", 415)
        resp.headers.add("Accept-Post", "multipart/form-data")
        return resp
    if file.mimetype not in ALLOWED_FILETYPES:
        resp = make_error(f"Files of type {file.mimetype} are not allowed.", 415)
        resp.headers.add("Accept-Post", "multipart/form-data")
        return resp
    
    filename = file.filename
    # Add correct file extension if necessary
    if not filename:
        filename = f"file{ALLOWED_FILETYPES[file.mimetype]}"
    elif not filename.lower().endswith(ALLOWED_FILETYPES[file.mimetype]):
        filename = filename + ALLOWED_FILETYPES[file.mimetype]

    # Generate a unique file ID
    file_id = str(uuid.uuid4())

    # Add file data to database
    await client.table("user_message_files").insert({
        "id": file_id,
        "filename": filename
    }).execute()

    buffer = file.stream.read()
    filepath = f"{file_id}/{filename}"

    # Upload file to storage bucket
    await client.storage.from_("UserMessageFiles").upload(
        path=filepath,
        file=buffer,
        file_options={"content_type": str(file.mimetype)}
    )

    # Public URL of the uploaded file
    file_url = await client.storage.from_("UserMessageFiles").get_public_url(filepath)
    
    file.close()
    # Send response
    return {"id": file_id, "url": file_url}


@uploads_bp.route("/get_file", methods=["GET", "OPTIONS"])
async def get_file_full():
    """Given a file UUID, this endpoint redirects to the public URL of the file.
    Use the "id" query parameter to specify the file UUID, for example:
    
    /uploads/get_file?id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    On success, a 303 redirect to the file location is returned.
    If the file is not found, a 404 error is returned.
    """
    return await request_shell(get_file, None, "args", "GET")


async def get_file(client: supabase.AsyncClient, data: multidict.MultiDict):
    file_id = data.get("id", type=str)

    # Lookup file in database
    db_response = await client.table("user_message_files").select("filename").eq("id", file_id).execute()

    if len(db_response.data) > 0:
        filename = db_response.data[0]["filename"]
    else:
        return make_error("No file with this ID was found.", 404)
    
    # Get public URL of the file
    file_url = await client.storage.from_("UserMessageFiles").get_public_url(f"{file_id}/{filename}")
    # Return redirect to the file URL
    return quart.redirect(file_url, code=303)
