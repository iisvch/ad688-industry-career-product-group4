import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/career_market_panel_clean.csv")

Path("figures/revised").mkdir(parents=True, exist_ok=True)

# 1. Job volume by title
title_counts = df["TITLE_RAW"].value_counts().head(15).sort_values()

plt.figure(figsize=(10, 7))
title_counts.plot(kind="barh")
plt.title("Top Data Analyst Job Titles — NAICS 523")
plt.xlabel("Number of Postings")
plt.ylabel("Job Title")
plt.tight_layout()
plt.savefig("figures/revised/job_volume_by_title.png", dpi=150)
plt.close()

# 2. Salary midpoint distribution
salary = df["salary_midpoint"].dropna()

plt.figure(figsize=(10, 6))
plt.hist(salary, bins=15)
plt.title("Salary Distribution — NAICS 523 Data Analyst Sample")
plt.xlabel("Annual Salary Midpoint ($)")
plt.ylabel("Number of Postings")
plt.tight_layout()
plt.savefig("figures/revised/salary_distribution.png", dpi=150)
plt.close()

# 3. Remote status
remote_counts = df["remote_status"].value_counts()

plt.figure(figsize=(8, 6))
remote_counts.plot(kind="bar")
plt.title("Remote Work Arrangement")
plt.xlabel("Work Arrangement")
plt.ylabel("Number of Postings")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figures/revised/remote_status.png", dpi=150)
plt.close()

# 4. Experience requirements
experience = df["MIN_YEARS_EXPERIENCE"].dropna()

plt.figure(figsize=(10, 6))
plt.hist(experience, bins=range(0, int(experience.max()) + 2))
plt.title("Minimum Experience Requirements")
plt.xlabel("Minimum Years of Experience")
plt.ylabel("Number of Postings")
plt.tight_layout()
plt.savefig("figures/revised/experience_requirements.png", dpi=150)
plt.close()

# 5. Top states
state_counts = df["state_clean"].value_counts().head(15).sort_values()

plt.figure(figsize=(10, 7))
state_counts.plot(kind="barh")
plt.title("Top Hiring States — NAICS 523 Data Analyst Sample")
plt.xlabel("Number of Postings")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("figures/revised/top_locations.png", dpi=150)
plt.close()

# 6. Top employers
employer_counts = df["COMPANY_NAME"].value_counts().head(15).sort_values()

plt.figure(figsize=(10, 7))
employer_counts.plot(kind="barh")
plt.title("Top Employers — NAICS 523 Data Analyst Sample")
plt.xlabel("Number of Postings")
plt.ylabel("Employer")
plt.tight_layout()
plt.savefig("figures/revised/top_employers.png", dpi=150)
plt.close()

print("Created revised Step 2 figures:")
for f in sorted(Path("figures/revised").glob("*.png")):
    print(f)
