from supabase import create_client, Client


db_client: Client = None
API_URL = "https://ntlfeglmcgnfiplilyud.supabase.co"
API_KEY = "sb_secret_NaKDgmb6QJGB2-ks6uE-wA_LiUrhSeH"


def init_client():
    global db_client
    db_client = create_client(API_URL, API_KEY)
