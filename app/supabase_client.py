import os
import httpx
from urllib.parse import urlencode

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

async def get_part_from_supabase(part_number: str):
    url = f"{SUPABASE_URL}/rest/v1/MASTER_FILE"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Accept": "application/json"
    }
    params = {
        "PartNumber": f"eq.{part_number}",
        "select": "*"
    }
    full_url = f"{url}?{urlencode(params)}"
    print(f"[Supabase] FULL REQUEST: {full_url}")
    print(f"[Supabase] Headers: {{'apikey': '***', 'Authorization': '***', 'Accept': 'application/json'}}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]
        return None 