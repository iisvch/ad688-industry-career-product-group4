import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv(".env")

BASE = os.getenv("EMPLOYABILITY_API_BASE_URL")
PREFIX = os.getenv("EMPLOYABILITY_API_PATH_PREFIX")
KEY = os.getenv("EMPLOYABILITY_API_KEY")

URL = f"{BASE}/{PREFIX.lstrip('/')}/jobs/"
HEADERS = {"X-API-Key": KEY}

RAW_FILE = "data/raw_naics_523000.json"
PAGE_SIZE = 100
START_OFFSET = 400
MAX_OFFSET = 2000

# Load existing records
with open(RAW_FILE, encoding="utf-8") as f:
    existing = json.load(f)

records = existing.get("results", [])

print(f"Existing records: {len(records)}")
print(f"Resuming at offset: {START_OFFSET}")

for offset in range(START_OFFSET, MAX_OFFSET + 1, PAGE_SIZE):

    params = {
        "naics": "523000",
        "limit": PAGE_SIZE,
        "offset": offset
    }

    print(f"\nRequesting offset={offset}...")

    try:
        r = requests.get(
            URL,
            headers=HEADERS,
            params=params,
            timeout=(10, 60)
        )

        r.raise_for_status()
        payload = r.json()

    except Exception as e:
        print(f"ERROR at offset {offset}: {type(e).__name__}: {e}")
        print("Stopping and saving everything collected so far.")
        break

    new_records = payload.get("results", [])

    print(f"Received {len(new_records)} records.")

    if not new_records:
        print("No more records.")
        break

    records.extend(new_records)

    # Save after every successful page
    existing["results"] = records
    existing["record_count"] = len(records)

    with open(RAW_FILE, "w", encoding="utf-8") as f:
        json.dump(
            existing,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"Saved total: {len(records)}")

    if not payload.get("meta", {}).get("has_more", False):
        print("API reports no more records.")
        break

    time.sleep(0.5)

print("\n====================================")
print(f"FINAL RAW RECORD COUNT: {len(records)}")
print("====================================")
