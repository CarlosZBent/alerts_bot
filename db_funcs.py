from supabase import create_client, Client
from dotenv import load_dotenv
from os import getenv

load_dotenv()

url: str = getenv("SUPABASE_URL")
key: str = getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

data = supabase.table("TEST-TABLE1").select('*').eq("date", "2023-05-05").execute()

for i in data:
    print(i)
