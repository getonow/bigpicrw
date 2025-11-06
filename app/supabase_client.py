import os
import httpx
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

async def get_part_from_supabase(part_number: str):
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        logger.error("Supabase credentials not configured. SUPABASE_URL and SUPABASE_ANON_KEY must be set.")
        raise ValueError("Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
    
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
    logger.debug(f"[Supabase] Requesting part: {part_number}")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data:
                return data[0]
            return None
    except httpx.HTTPError as e:
        logger.error(f"Supabase request failed: {str(e)}")
        raise 