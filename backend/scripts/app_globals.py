
"""Please create a file named ".env" in this directory with the following contents:
SUPABASE_URL=insert supabase url here
SUPABASE_KEY=insert supabase key here

Alternatively, you can set the environment variables by the usual methods.
Be careful to keep these variables secret!
"""

from dotenv import load_dotenv
from os import environ

load_dotenv()

_test_supa_url = environ.get("SUPABASE_URL")
_test_supa_key = environ.get("SUPABASE_KEY")

if _test_supa_url is None or _test_supa_key is None:
    raise EnvironmentError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file, or otherwise be defined environment variables.")

SUPA_URL: str = _test_supa_url
SUPA_KEY: str = _test_supa_key
QUART_PORT    = int(environ.get("QUART_PORT", 5000))
