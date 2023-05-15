from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

load_dotenv()

url: str = getenv("SUPABASE_URL")
key: str = getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

today = datetime.now().date()

# select today's data from DB
data = supabase.table("TEST-TABLE1").select('*').eq("date", today).execute()

daily_events = data.data
