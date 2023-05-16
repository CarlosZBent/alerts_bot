from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SUPABASE_URL: str = getenv("SUPABASE_URL")
SUPABASE_KEY: str = getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def query_present_day_data(table:str, date:str) -> list:
    """
    Fetch the events data for today from the database
    """
    # select today's data from DB
    data = supabase.table(table).select('*').eq("date", date).execute().data
    return data
