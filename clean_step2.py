import pandas as pd

src = "data/career_market_panel_clean.csv"
df = pd.read_csv(src)

# -------------------------------------------------
# 1. Remove exact duplicate job IDs
# -------------------------------------------------
before = len(df)
df = df.drop_duplicates(subset="ID", keep="first")
duplicates_removed = before - len(df)

# -------------------------------------------------
# 2. Clean date fields
# -------------------------------------------------
for col in ["LAST_UPDATED_DATE", "POSTED", "EXPIRED"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# -------------------------------------------------
# 3. Clean numeric fields
# -------------------------------------------------
numeric_cols = [
    "MIN_YEARS_EXPERIENCE",
    "MAX_YEARS_EXPERIENCE",
    "SALARY_FROM",
    "SALARY_TO"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------------------------------
# 4. Salary cleaning
# Keep missing salary values as missing.
# Remove impossible negative salary values.
# -------------------------------------------------
for col in ["SALARY_FROM", "SALARY_TO"]:
    df.loc[df[col] < 0, col] = pd.NA

# If salary range is reversed, swap the two values.
reverse_salary = (
    df["SALARY_FROM"].notna()
    & df["SALARY_TO"].notna()
    & (df["SALARY_FROM"] > df["SALARY_TO"])
)

df.loc[reverse_salary, ["SALARY_FROM", "SALARY_TO"]] = (
    df.loc[reverse_salary, ["SALARY_TO", "SALARY_FROM"]].to_numpy()
)

# -------------------------------------------------
# 5. Experience cleaning
# Remove impossible negative values.
# -------------------------------------------------
for col in ["MIN_YEARS_EXPERIENCE", "MAX_YEARS_EXPERIENCE"]:
    df.loc[df[col] < 0, col] = pd.NA

# -------------------------------------------------
# 6. Clean remote/work arrangement labels
# -------------------------------------------------
df["remote_status"] = df["REMOTE_TYPE_NAME"].replace(
    ["[None]", "", "None", "nan"], pd.NA
)

df["remote_status"] = df["remote_status"].fillna("Unknown")

# -------------------------------------------------
# 7. Clean location fields
# -------------------------------------------------
df["city_clean"] = df["CITY_NAME"].replace(
    ["[Unknown City]", "", "Unknown", "nan"], pd.NA
)

df["state_clean"] = df["STATE_NAME"].replace(
    ["[Unknown State]", "", "Unknown", "nan"], pd.NA
)

# -------------------------------------------------
# 8. Salary midpoint
# Only calculate when both endpoints exist.
# -------------------------------------------------
df["salary_midpoint"] = (
    df["SALARY_FROM"] + df["SALARY_TO"]
) / 2

# -------------------------------------------------
# 9. Preserve the industry definition
# -------------------------------------------------
df["NAICS3"] = pd.to_numeric(df["NAICS3"], errors="coerce")
df["industry_scope"] = "NAICS 523"

# -------------------------------------------------
# 10. Add career scope label
# -------------------------------------------------
df["career_scope"] = "Core Data Analyst"

# -------------------------------------------------
# 11. Save cleaned dataset
# -------------------------------------------------
df.to_csv(src, index=False)

print("Cleaning complete.")
print("Rows retained:", len(df))
print("Exact duplicate IDs removed:", duplicates_removed)
print("Salary midpoint available:", df["salary_midpoint"].notna().sum())
print("Unknown remote status:", (df["remote_status"] == "Unknown").sum())
print("Missing minimum experience:", df["MIN_YEARS_EXPERIENCE"].isna().sum())
print("Missing maximum experience:", df["MAX_YEARS_EXPERIENCE"].isna().sum())
print("Missing city:", df["city_clean"].isna().sum())
print("Missing state:", df["state_clean"].isna().sum())
