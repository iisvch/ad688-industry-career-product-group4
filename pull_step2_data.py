import os
import re
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")

BASE = os.getenv("EMPLOYABILITY_API_BASE_URL")
PREFIX = os.getenv("EMPLOYABILITY_API_PATH_PREFIX")
API_KEY = os.getenv("EMPLOYABILITY_API_KEY")

URL = f"{BASE}/{PREFIX.lstrip('/')}/jobs/"

HEADERS = {"X-API-Key": API_KEY}

PAGE_SIZE = 100
OFFSET = 0
MAX_PAGES = 200

all_results = []
first_meta = None

print("=" * 70)
print("MET CAREER COMPASS — STEP 2 DATA PULL")
print("Industry: NAICS 523000")
print("Career: Data Analyst / Data Analytics")
print("=" * 70)

while OFFSET is not None and len(all_results) < PAGE_SIZE * MAX_PAGES:
    params = {
        "naics": "523000",
        "limit": PAGE_SIZE,
        "offset": OFFSET
    }

    print(f"\nRequesting offset={OFFSET}, limit={PAGE_SIZE}...")

    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            params=params,
            timeout=(10, 90)
        )
        response.raise_for_status()
        payload = response.json()

    except Exception as e:
        print(f"\nERROR at offset {OFFSET}: {type(e).__name__}: {e}")
        print("Saving the records collected so far.")
        break

    if first_meta is None:
        first_meta = payload.get("meta", {})

    results = payload.get("results", [])

    print(f"Received {len(results)} records.")

    if not results:
        break

    all_results.extend(results)

    meta = payload.get("meta", {})
    has_more = meta.get("has_more", False)

    if not has_more:
        print("API reports no more records.")
        break

    next_url = meta.get("next")

    if next_url and "offset=" in next_url:
        match = re.search(r"offset=(\d+)", next_url)
        if match:
            OFFSET = int(match.group(1))
        else:
            OFFSET += PAGE_SIZE
    else:
        OFFSET += PAGE_SIZE

    time.sleep(0.2)

print("\n" + "=" * 70)
print(f"TOTAL RAW RECORDS DOWNLOADED: {len(all_results):,}")
print("=" * 70)

# ------------------------------------------------------------------
# Save raw API response
# ------------------------------------------------------------------

raw_path = "data/raw_naics_523000.json"

with open(raw_path, "w", encoding="utf-8") as f:
    json.dump(
        {
            "meta": first_meta,
            "record_count": len(all_results),
            "results": all_results
        },
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Raw data saved to: {raw_path}")

if not all_results:
    raise SystemExit("No records were downloaded. Stop here and inspect the API response.")

# ------------------------------------------------------------------
# Convert to DataFrame
# ------------------------------------------------------------------

df = pd.json_normalize(all_results)

print(f"Raw dataframe shape: {df.shape}")

# ------------------------------------------------------------------
# Verify NAICS
# ------------------------------------------------------------------

if "naics_code" in df.columns:
    df["naics_code"] = df["naics_code"].astype(str).str.strip()

df = df[df["naics_code"] == "523000"].copy()

print(f"Records after NAICS 523000 verification: {len(df):,}")

# ------------------------------------------------------------------
# Data Analyst / Analytics title filter
#
# We intentionally do NOT use the API q parameter because it caused
# the API request to hang. We perform the career filter locally so
# the methodology is transparent and reproducible.
# ------------------------------------------------------------------

title_columns = [
    c for c in ["title", "normalized_title"]
    if c in df.columns
]

title_text = (
    df[title_columns]
    .fillna("")
    .astype(str)
    .agg(" ".join, axis=1)
    .str.lower()
)

role_pattern = (
    r"\bdata analyst\b"
    r"|\bdata analytics\b"
    r"|\bbusiness data analyst\b"
    r"|\bbusiness intelligence analyst\b"
    r"|\bbi analyst\b"
    r"|\banalytics analyst\b"
    r"|\breporting analyst\b"
    r"|\bdecision analyst\b"
    r"|\bmarketing analyst\b"
    r"|\bfinancial analyst\b"
)

df["career_scope_match"] = title_text.str.contains(
    role_pattern,
    regex=True,
    na=False
)

career_df = df[df["career_scope_match"]].copy()

print(f"Data Analyst/Analytics records: {len(career_df):,}")

# ------------------------------------------------------------------
# Basic cleaning
# ------------------------------------------------------------------

# Dates
for col in ["posted_at", "expires_at"]:
    if col in career_df.columns:
        career_df[col] = pd.to_datetime(
            career_df[col],
            errors="coerce",
            utc=True
        )

# Salary
salary_columns = [
    "annual_salary_min",
    "annual_salary_max",
    "hourly_salary_min",
    "hourly_salary_max"
]

for col in salary_columns:
    if col in career_df.columns:
        career_df[col] = pd.to_numeric(
            career_df[col],
            errors="coerce"
        )

# Remote status
if "remote_status" in career_df.columns:
    career_df["remote_status"] = (
        career_df["remote_status"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

# Location
for col in ["location_text", "city", "state", "state_code"]:
    if col in career_df.columns:
        career_df[col] = (
            career_df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

# Remove duplicate postings
before_duplicates = len(career_df)

if "job_id" in career_df.columns:
    career_df = career_df.drop_duplicates(
        subset=["job_id"],
        keep="first"
    )
else:
    career_df = career_df.drop_duplicates()

print(
    f"Duplicates removed: "
    f"{before_duplicates - len(career_df):,}"
)

# ------------------------------------------------------------------
# Keep useful analytical fields
# ------------------------------------------------------------------

preferred_columns = [
    "job_id",
    "posted_at",
    "expires_at",
    "title",
    "normalized_title",
    "company_name",
    "organization",
    "is_staffing_agency",
    "location_text",
    "city",
    "state",
    "state_code",
    "remote_status",
    "employment_type",
    "salary_text",
    "annual_salary_min",
    "annual_salary_max",
    "hourly_salary_min",
    "hourly_salary_max",
    "soc_code",
    "soc_name",
    "occupation_family",
    "naics_code",
    "naics_name",
    "onet_code",
    "onet_name",
    "skills",
    "description",
    "apply_url",
    "student_signals.requirements_summary",
    "student_signals.responsibilities_summary",
    "student_signals.technical_tools_summary",
    "bls.area_name",
    "bls.employment",
    "bls.annual_mean_wage",
    "bls.annual_median_wage",
    "census.state_name",
    "census.median_household_income",
    "census.bachelors_or_higher_pct"
]

available_columns = [
    c for c in preferred_columns
    if c in career_df.columns
]

career_df = career_df[available_columns].copy()

# ------------------------------------------------------------------
# Save analytical dataset
# ------------------------------------------------------------------

output_path = "data/career_market_panel.csv"

career_df.to_csv(
    output_path,
    index=False,
    encoding="utf-8"
)

print(f"\nCleaned dataset saved to: {output_path}")
print(f"Final analytical records: {len(career_df):,}")
print(f"Final variables: {len(career_df.columns)}")

# ------------------------------------------------------------------
# Data dictionary
# ------------------------------------------------------------------

descriptions = {
    "job_id": "Unique MET job posting identifier.",
    "posted_at": "Date and time the job posting was published.",
    "expires_at": "Expiration date/time when available.",
    "title": "Original job posting title.",
    "normalized_title": "MET-normalized job title.",
    "company_name": "Employer name.",
    "location_text": "Original location text.",
    "city": "City or location supplied by MET.",
    "state": "State or region supplied by MET.",
    "state_code": "State code when available.",
    "remote_status": "Remote, hybrid, onsite, or unknown work arrangement.",
    "employment_type": "Employment type when available.",
    "salary_text": "Original salary representation.",
    "annual_salary_min": "Minimum annual salary when available.",
    "annual_salary_max": "Maximum annual salary when available.",
    "hourly_salary_min": "Minimum hourly salary when available.",
    "hourly_salary_max": "Maximum hourly salary when available.",
    "soc_code": "SOC occupation code.",
    "soc_name": "SOC occupation name.",
    "occupation_family": "Occupation family.",
    "naics_code": "NAICS industry code.",
    "naics_name": "NAICS industry name.",
    "onet_code": "O*NET occupation code.",
    "onet_name": "O*NET occupation name.",
    "skills": "Skills associated with the posting.",
    "description": "Job posting description.",
    "apply_url": "Application URL when available.",
    "student_signals.requirements_summary": "MET summary of job requirements.",
    "student_signals.responsibilities_summary": "MET summary of job responsibilities.",
    "student_signals.technical_tools_summary": "MET summary of technical tools.",
    "bls.area_name": "BLS geographic area.",
    "bls.employment": "BLS employment estimate when available.",
    "bls.annual_mean_wage": "BLS annual mean wage when available.",
    "bls.annual_median_wage": "BLS annual median wage when available.",
    "census.state_name": "Census state name.",
    "census.median_household_income": "Census median household income.",
    "census.bachelors_or_higher_pct": "Census percentage with bachelor's degree or higher."
}

dictionary = []

for col in career_df.columns:
    dictionary.append({
        "variable": col,
        "description": descriptions.get(
            col,
            "MET Career Compass job-level field."
        ),
        "dtype": str(career_df[col].dtype),
        "missing_count": int(career_df[col].isna().sum()),
        "missing_percent": round(
            career_df[col].isna().mean() * 100,
            2
        )
    })

dictionary_df = pd.DataFrame(dictionary)

dictionary_path = "data/data_dictionary.csv"

dictionary_df.to_csv(
    dictionary_path,
    index=False
)

print(f"Data dictionary saved to: {dictionary_path}")

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 2 DATA SUMMARY")
print("=" * 70)

if len(career_df):
    print("\nTop titles:")
    print(
        career_df["title"]
        .value_counts()
        .head(15)
        .to_string()
    )

    if "remote_status" in career_df.columns:
        print("\nRemote status:")
        print(
            career_df["remote_status"]
            .value_counts()
            .to_string()
        )

    if "state" in career_df.columns:
        print("\nTop locations:")
        print(
            career_df["state"]
            .replace("", pd.NA)
            .dropna()
            .value_counts()
            .head(15)
            .to_string()
        )

    if "annual_salary_min" in career_df.columns:
        salary = career_df["annual_salary_min"].dropna()
        if len(salary):
            print("\nAnnual salary minimum summary:")
            print(salary.describe().to_string())

print("\nDONE.")
