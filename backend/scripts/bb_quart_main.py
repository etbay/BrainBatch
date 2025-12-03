import quart
import tracemalloc
import re
from quart_cors import cors
from app_globals import *


tracemalloc.start()
app = quart.Quart(__name__)

from user_management import user_bp
from group_management import group_bp
from file_uploads import uploads_bp

app.register_blueprint(user_bp)
app.register_blueprint(group_bp)
app.register_blueprint(uploads_bp)

# Set allowed CORS origins, headers, and methods
app = cors(app, 
           allow_headers="*", 
           allow_methods=["GET", "POST", "OPTIONS"],
           allow_origin=re.compile(r"https?:\/\/(((\S+\.)?brainbatch\.xyz)|(localhost|127\.0\.0\.1)(:\d+)?)")
           )

# Set maximum file upload size to 5 MiB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Run the Quart app
app.run(host="127.0.0.1", port=QUART_PORT, use_reloader=False)
