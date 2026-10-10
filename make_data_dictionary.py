import pandas as pd

df = pd.read_csv("data/career_market_panel_clean.csv")

definitions = {
    "ID": "Unique Lightcast job-posting identifier.",
    "LAST_UPDATED_DATE": "Date the job posting record was last updated.",
    "POSTED": "Date the job posting was posted.",
    "EXPIRED": "Date the job posting expired, when available.",
    "TITLE_RAW": "Original job title from the Lightcast posting.",
    "TITLE": "Standardized Lightcast job title.",
    "TITLE_NAME": "Named occupational/job-title classification.",
    "TITLE_CLEAN": "Cleaned job title field.",
    "BODY": "Job-posting description text.",
    "COMPANY_NAME": "Employer name.",
    "LOCATION": "Original job location field.",
    "CITY_NAME": "City associated with the posting.",
    "STATE_NAME": "State associated with the posting.",
    "REMOTE_TYPE": "Lightcast remote-work classification code.",
    "REMOTE_TYPE_NAME": "Readable remote-work classification.",
    "MIN_YEARS_EXPERIENCE": "Minimum years of experience required, when available.",
    "MAX_YEARS_EXPERIENCE": "Maximum years of experience required, when available.",
    "EDUCATION_LEVELS_NAME": "Education-level information associated with the posting.",
    "SALARY": "Original salary field.",
    "SALARY_FROM": "Lower bound of reported salary range.",
    "SALARY_TO": "Upper bound of reported salary range.",
    "ORIGINAL_PAY_PERIOD": "Original salary pay-period information.",
    "SKILLS": "Lightcast coded skills associated with the posting.",
    "SKILLS_NAME": "Readable skill names.",
    "SPECIALIZED_SKILLS": "Lightcast specialized skill codes.",
    "SPECIALIZED_SKILLS_NAME": "Readable specialized skill names.",
    "COMMON_SKILLS": "Lightcast common skill codes.",
    "COMMON_SKILLS_NAME": "Readable common skill names.",
    "SOFTWARE_SKILLS": "Lightcast software skill codes.",
    "SOFTWARE_SKILLS_NAME": "Readable software skill names.",
    "NAICS3": "Three-digit NAICS industry subsector code.",
    "NAICS3_NAME": "Name of the three-digit NAICS industry subsector.",
    "SOC_2021_5": "Five-digit SOC 2021 occupation code.",
    "SOC_2021_5_NAME": "Name of the five-digit SOC 2021 occupation classification.",
    "ONET": "O*NET occupation code.",
    "ONET_NAME": "O*NET occupation name.",
    "remote_status": "Cleaned remote-work classification; missing classifications are labeled Unknown.",
    "city_clean": "Cleaned city field.",
    "state_clean": "Cleaned state field.",
    "salary_midpoint": "Midpoint of the reported salary range when both salary endpoints are available.",
    "industry_scope": "Analysis industry scope, defined as NAICS 523.",
    "career_scope": "Career filter used for the revised core Data Analyst sample."
}

rows = []

for col in df.columns:
    rows.append({
        "variable": col,
        "description": definitions.get(col, "Variable retained from the Lightcast dataset."),
        "data_type": str(df[col].dtype),
        "missing_count": int(df[col].isna().sum()),
        "non_missing_count": int(df[col].notna().sum())
    })

dictionary = pd.DataFrame(rows)
dictionary.to_csv("data/data_dictionary_new.csv", index=False)

print("Created data/data_dictionary_new.csv")
print("Variables documented:", len(dictionary))
