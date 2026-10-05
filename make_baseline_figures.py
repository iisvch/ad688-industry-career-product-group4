import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

RAW = "data/raw_naics_523000.json"
FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

with open(RAW, encoding="utf-8") as f:
    data = json.load(f)

df = pd.json_normalize(data["results"])

# ------------------------------------------------------------
# Basic cleaning
# ------------------------------------------------------------

for col in ["title", "company_name", "state", "location_text", "remote_status"]:
    if col in df.columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

# ------------------------------------------------------------
# 1. Job volume by title
# ------------------------------------------------------------

top_titles = df["title"].replace("", "Unknown").value_counts().head(10)

plt.figure(figsize=(10, 6))
top_titles.sort_values().plot(kind="barh")
plt.title("Top Job Titles — NAICS 523000")
plt.xlabel("Number of Postings")
plt.ylabel("Job Title")
plt.tight_layout()
plt.savefig(FIG_DIR / "job_volume_by_title.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# 2. Remote / onsite / hybrid
# ------------------------------------------------------------

remote = (
    df["remote_status"]
    .replace("", "unknown")
    .str.lower()
    .value_counts()
)

plt.figure(figsize=(8, 5))
remote.plot(kind="bar")
plt.title("Work Arrangement — NAICS 523000")
plt.xlabel("Work Arrangement")
plt.ylabel("Number of Postings")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(FIG_DIR / "remote_status.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# 3. Top locations
# ------------------------------------------------------------

location_col = "state" if "state" in df.columns else "location_text"

locations = (
    df[location_col]
    .replace("", "Unknown")
    .value_counts()
    .head(10)
)

plt.figure(figsize=(10, 6))
locations.sort_values().plot(kind="barh")
plt.title("Top Hiring Locations — NAICS 523000")
plt.xlabel("Number of Postings")
plt.ylabel("Location")
plt.tight_layout()
plt.savefig(FIG_DIR / "top_locations.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# 4. Salary availability
# ------------------------------------------------------------

salary_cols = [
    c for c in [
        "annual_salary_min",
        "annual_salary_max",
        "hourly_salary_min",
        "hourly_salary_max"
    ]
    if c in df.columns
]

for col in salary_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if salary_cols:
    salary_available = df[salary_cols].notna().any(axis=1)
    salary_counts = pd.Series(
        {
            "Salary reported": int(salary_available.sum()),
            "Salary not reported": int((~salary_available).sum())
        }
    )

    plt.figure(figsize=(7, 5))
    salary_counts.plot(kind="bar")
    plt.title("Salary Information Availability")
    plt.ylabel("Number of Postings")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "salary_availability.png", dpi=200)
    plt.close()

# ------------------------------------------------------------
# 5. Salary distribution where available
# ------------------------------------------------------------

if "annual_salary_min" in df.columns and "annual_salary_max" in df.columns:
    salary_df = df[
        df["annual_salary_min"].notna() &
        df["annual_salary_max"].notna()
    ].copy()

    if len(salary_df) > 0:
        salary_df["salary_midpoint"] = (
            salary_df["annual_salary_min"] +
            salary_df["annual_salary_max"]
        ) / 2

        plt.figure(figsize=(9, 5))
        salary_df["salary_midpoint"].plot(
            kind="hist",
            bins=15
        )
        plt.title("Annual Salary Midpoint Distribution")
        plt.xlabel("Annual Salary")
        plt.ylabel("Number of Postings")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "salary_distribution.png", dpi=200)
        plt.close()

# ------------------------------------------------------------
# 6. Experience fields — detect available field
# ------------------------------------------------------------

experience_candidates = [
    c for c in df.columns
    if any(
        word in c.lower()
        for word in ["experience", "years_experience", "experience_level"]
    )
]

print("=" * 70)
print("MARKET BASELINE FIGURE GENERATION")
print("=" * 70)
print("Records:", len(df))
print()
print("Columns related to experience:")
print(experience_candidates)
print()

print("Salary fields:")
print(salary_cols)
print()

print("Top titles:")
print(top_titles.to_string())
print()

print("Remote status:")
print(remote.to_string())
print()

print("Top locations:")
print(locations.to_string())
print()

print("Figures created:")
for f in sorted(FIG_DIR.glob("*.png")):
    print(" -", f)

print()
print("DONE")
