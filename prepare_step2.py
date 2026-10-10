import pandas as pd

# ============================================================
# Step 2: Prepare the NAICS 523 Data Analyst market dataset
# ============================================================

SOURCE = "lightcast_job_postings.csv"
OUTPUT = "data/career_market_panel.csv"

cols = [
    "ID",
    "LAST_UPDATED_DATE",
    "POSTED",
    "EXPIRED",
    "TITLE_RAW",
    "TITLE",
    "TITLE_NAME",
    "TITLE_CLEAN",
    "BODY",
    "COMPANY_NAME",
    "LOCATION",
    "CITY_NAME",
    "STATE_NAME",
    "REMOTE_TYPE",
    "REMOTE_TYPE_NAME",
    "MIN_YEARS_EXPERIENCE",
    "MAX_YEARS_EXPERIENCE",
    "EDUCATION_LEVELS_NAME",
    "SALARY",
    "SALARY_FROM",
    "SALARY_TO",
    "ORIGINAL_PAY_PERIOD",
    "SKILLS",
    "SKILLS_NAME",
    "SPECIALIZED_SKILLS",
    "SPECIALIZED_SKILLS_NAME",
    "COMMON_SKILLS",
    "COMMON_SKILLS_NAME",
    "SOFTWARE_SKILLS",
    "SOFTWARE_SKILLS_NAME",
    "NAICS3",
    "NAICS3_NAME",
    "SOC_2021_5",
    "SOC_2021_5_NAME",
    "ONET",
    "ONET_NAME",
]

print("Reading Lightcast dataset...")
df = pd.read_csv(SOURCE, usecols=cols)

# ------------------------------------------------------------
# 1. Industry scope: NAICS 523
# ------------------------------------------------------------
industry = df[df["NAICS3"] == 523].copy()

print("NAICS 523 postings:", len(industry))

# ------------------------------------------------------------
# 2. Strict Data Analyst career filter
# ------------------------------------------------------------
title = industry["TITLE_RAW"].fillna("")

strict_pattern = (
    r"\bdata analyst\b"
    r"|data analyst\s*(i|ii|iii|iv|1|2|3|4)"
)

strict = industry[
    title.str.contains(strict_pattern, case=False, regex=True)
].copy()

# ------------------------------------------------------------
# 3. Exclude clearly unrelated uses of Data Analyst
# These are the exclusions used to create the original 140-posting
# Step 2 dataset.
exclude_pattern = (
    r"maintenance"
    r"|cybersecurity"
    r"|academic"
    r"|internship"
    r"|platform services"
    r"|CV-22"
    r"|SC2"
)

final = strict[
    ~strict["TITLE_RAW"].fillna("").str.contains(
        exclude_pattern, case=False, regex=True
    )
].copy()

# ------------------------------------------------------------
# 4. Remove exact duplicate posting IDs
# ------------------------------------------------------------
before = len(final)
final = final.drop_duplicates(subset="ID", keep="first")
duplicates_removed = before - len(final)

# ------------------------------------------------------------
# 5. Clean dates
# ------------------------------------------------------------
for col in ["LAST_UPDATED_DATE", "POSTED", "EXPIRED"]:
    final[col] = pd.to_datetime(final[col], errors="coerce")

# ------------------------------------------------------------
# 6. Clean numeric variables
# ------------------------------------------------------------
numeric_cols = [
    "MIN_YEARS_EXPERIENCE",
    "MAX_YEARS_EXPERIENCE",
    "SALARY_FROM",
    "SALARY_TO",
]

for col in numeric_cols:
    final[col] = pd.to_numeric(final[col], errors="coerce")

# ------------------------------------------------------------
# 7. Clean salary values
# ------------------------------------------------------------
for col in ["SALARY_FROM", "SALARY_TO"]:
    final.loc[final[col] < 0, col] = pd.NA

reverse_salary = (
    final["SALARY_FROM"].notna()
    & final["SALARY_TO"].notna()
    & (final["SALARY_FROM"] > final["SALARY_TO"])
)

final.loc[
    reverse_salary, ["SALARY_FROM", "SALARY_TO"]
] = final.loc[
    reverse_salary, ["SALARY_TO", "SALARY_FROM"]
].to_numpy()

# ------------------------------------------------------------
# 8. Clean experience values
# ------------------------------------------------------------
for col in ["MIN_YEARS_EXPERIENCE", "MAX_YEARS_EXPERIENCE"]:
    final.loc[final[col] < 0, col] = pd.NA

# ------------------------------------------------------------
# 9. Clean remote status
# ------------------------------------------------------------
final["remote_status"] = final["REMOTE_TYPE_NAME"].replace(
    ["[None]", "", "None", "nan"], pd.NA
)

final["remote_status"] = final["remote_status"].fillna("Unknown")

# ------------------------------------------------------------
# 10. Clean locations
# ------------------------------------------------------------
final["city_clean"] = final["CITY_NAME"].replace(
    ["[Unknown City]", "", "Unknown", "nan"], pd.NA
)

final["state_clean"] = final["STATE_NAME"].replace(
    ["[Unknown State]", "", "Unknown", "nan"], pd.NA
)

# ------------------------------------------------------------
# 11. Salary midpoint
# ------------------------------------------------------------
final["salary_midpoint"] = (
    final["SALARY_FROM"] + final["SALARY_TO"]
) / 2

# ------------------------------------------------------------
# 12. Preserve analysis scope
# ------------------------------------------------------------
final["NAICS3"] = pd.to_numeric(final["NAICS3"], errors="coerce")
final["industry_scope"] = "NAICS 523"
final["career_scope"] = "Core Data Analyst"

# ------------------------------------------------------------
# 13. Save final analytical dataset
# ------------------------------------------------------------
final.to_csv(OUTPUT, index=False)

print("\n===== STEP 2 COMPLETE =====")
print("NAICS 523 postings:", len(industry))
print("Strict Data Analyst postings:", len(strict))
print("Final postings after exclusions:", len(final))
print("Exact duplicate IDs removed:", duplicates_removed)
print("Salary midpoint available:", final["salary_midpoint"].notna().sum())
print("Unknown remote status:", (final["remote_status"] == "Unknown").sum())
print("Missing minimum experience:", final["MIN_YEARS_EXPERIENCE"].isna().sum())
print("Missing maximum experience:", final["MAX_YEARS_EXPERIENCE"].isna().sum())
print("Output:", OUTPUT)
