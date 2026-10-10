import pandas as pd

cols = [
    "ID",
    "TITLE_RAW",
    "TITLE",
    "TITLE_NAME",
    "TITLE_CLEAN",
    "NAICS3",
    "NAICS3_NAME"
]

df = pd.read_csv("lightcast_job_postings.csv", usecols=cols)

# Industry scope: NAICS 523
industry = df[df["NAICS3"] == 523].copy()

# Strict Data Analyst baseline
strict_pattern = (
    r"\bdata analyst\b"
    r"|data analyst\s*(i|ii|iii|iv|1|2|3|4)"
)

strict = industry[
    industry["TITLE_RAW"].fillna("").str.contains(
        strict_pattern, case=False, regex=True
    )
].copy()

# Expanded Data Analytics career sample
expanded_pattern = (
    r"data analyst"
    r"|data & bi analyst"
    r"|bi analyst"
    r"|business intelligence analyst"
    r"|data analytics"
    r"|data insights"
    r"|data governance analyst"
    r"|data visualization analyst"
    r"|data management analyst"
    r"|data operations analyst"
    r"|data reporting analyst"
    r"|reporting data analyst"
    r"|data quality.*analyst"
    r"|data steward"
    r"|market data analyst"
    r"|product data analyst"
    r"|customer data analyst"
    r"|client data analyst"
)

expanded = industry[
    industry["TITLE_RAW"].fillna("").str.contains(
        expanded_pattern, case=False, regex=True
    )
].copy()

# Remove clearly unrelated uses of "data analyst"
exclude_pattern = (
    r"maintenance data analyst"
    r"|cybersecurity data analyst"
    r"|legal analyst"
    r"|academic data analyst"
    r"|health data"
    r"|clinical"
    r"|data privacy"
)

expanded_clean = expanded[
    ~expanded["TITLE_RAW"].fillna("").str.contains(
        exclude_pattern, case=False, regex=True
    )
].copy()

print("\n===== INDUSTRY =====")
print("NAICS 523 postings:", len(industry))

print("\n===== STRICT BASELINE =====")
print("Strict Data Analyst postings:", len(strict))

print("\nTop strict titles:")
print(strict["TITLE_RAW"].value_counts().head(30).to_string())

print("\n===== EXPANDED SAMPLE =====")
print("Expanded postings before exclusions:", len(expanded))
print("Expanded postings after exclusions:", len(expanded_clean))

print("\nTop expanded titles:")
print(expanded_clean["TITLE_RAW"].value_counts().head(50).to_string())

