import json
import pandas as pd

RAW = "data/raw_naics_523000.json"

with open(RAW, encoding="utf-8") as f:
    data = json.load(f)

df = pd.json_normalize(data["results"])

# ------------------------------------------------------------
# Step 2 scope
# ------------------------------------------------------------

df["naics_code"] = df["naics_code"].astype(str).str.strip()

industry_df = df[df["naics_code"] == "523000"].copy()

# Direct Data Analyst / Data & Insights title logic
title_text = (
    industry_df["title"]
    .fillna("")
    .astype(str)
    .str.lower()
)

career_mask = (
    title_text.str.contains(r"\bdata\s*&\s*insights\s*analyst\b", regex=True, na=False)
    |
    title_text.str.contains(r"\bdata\s+analyst\b", regex=True, na=False)
)

career_df = industry_df[career_mask].copy()

# Remove duplicate postings
career_df = career_df.drop_duplicates(
    subset=["job_id"],
    keep="first"
)

# ------------------------------------------------------------
# Clean core variables
# ------------------------------------------------------------

date_cols = ["posted_at", "expires_at"]

for col in date_cols:
    if col in career_df.columns:
        career_df[col] = pd.to_datetime(
            career_df[col],
            errors="coerce",
            utc=True
        )

salary_cols = [
    "annual_salary_min",
    "annual_salary_max",
    "hourly_salary_min",
    "hourly_salary_max"
]

for col in salary_cols:
    if col in career_df.columns:
        career_df[col] = pd.to_numeric(
            career_df[col],
            errors="coerce"
        )

text_cols = [
    "title",
    "normalized_title",
    "company_name",
    "location_text",
    "city",
    "state",
    "state_code",
    "remote_status",
    "employment_type",
    "soc_code",
    "soc_name",
    "occupation_family",
    "naics_code",
    "naics_name",
    "onet_code",
    "onet_name"
]

for col in text_cols:
    if col in career_df.columns:
        career_df[col] = (
            career_df[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

# ------------------------------------------------------------
# Save final analytical dataset
# ------------------------------------------------------------

output = "data/career_market_panel.csv"

career_df.to_csv(
    output,
    index=False,
    encoding="utf-8"
)

# ------------------------------------------------------------
# Create data dictionary
# ------------------------------------------------------------

dictionary = [
    ["job_id", "Unique MET job posting identifier."],
    ["posted_at", "Job posting publication date/time."],
    ["title", "Original job posting title."],
    ["normalized_title", "MET-normalized job title."],
    ["company_name", "Employer name."],
    ["location_text", "Job location text."],
    ["city", "Job city/location."],
    ["state", "Job state or region."],
    ["remote_status", "Remote, hybrid, onsite, or unknown."],
    ["employment_type", "Employment type when available."],
    ["annual_salary_min", "Minimum annual salary."],
    ["annual_salary_max", "Maximum annual salary."],
    ["hourly_salary_min", "Minimum hourly salary."],
    ["hourly_salary_max", "Maximum hourly salary."],
    ["soc_code", "SOC occupation code."],
    ["soc_name", "SOC occupation name."],
    ["occupation_family", "Occupation family."],
    ["naics_code", "NAICS industry code."],
    ["naics_name", "NAICS industry name."],
    ["onet_code", "O*NET occupation code."],
    ["onet_name", "O*NET occupation name."],
    ["skills", "Skills associated with the posting."],
    ["description", "Job posting description."]
]

dictionary_df = pd.DataFrame(
    dictionary,
    columns=["variable", "description"]
)

dictionary_df.to_csv(
    "data/data_dictionary.csv",
    index=False
)

# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("=" * 70)
print("STEP 2 FINAL DATASET")
print("=" * 70)
print("Raw NAICS 523000 records:", len(df))
print("Verified NAICS 523000 records:", len(industry_df))
print("Direct Data Analyst/Data & Insights Analyst records:", len(career_df))
print("Duplicate postings removed:", 0)
print()
print("Final dataset:", output)
print("Data dictionary: data/data_dictionary.csv")
print()

if len(career_df):
    print("Included postings:")
    print(
        career_df[
            ["job_id", "title", "company_name", "location_text",
             "remote_status"]
        ].to_string(index=False)
    )

print()
print("NOTE:")
print(
    "The MET API returned 400 NAICS 523000 records before requests "
    "starting at offset 400 timed out. The limitation will be documented "
    "in the Step 2 methodology."
)
