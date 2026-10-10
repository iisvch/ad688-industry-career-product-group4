## Limits of the Evidence

- **Small, selected sample.** The study uses 140 Data Analyst postings in NAICS 523, representing 102 employer/title/description profiles. Salary analysis uses only 86 postings and 48 profiles. These findings are exploratory and do not support firm conclusions for the full Data Analyst market.
- **Uneven geographic coverage.** The data includes several states, but locations and employers are not evenly represented. Regional patterns describe this sample; they do not establish national demand, the best relocation choice, or salary differences after cost of living.
- **Historical and incomplete records.** The postings cover May–September 2024. Salary is missing for 54 postings, minimum experience for 28, and remote classification for 71. Missing information may affect which roles appear in each analysis.
- **Postings are not confirmed openings or offers.** One job can be advertised in several locations. Exact-text grouping reduces repeated counts but may miss similar reposts. Salary endpoints were annualized during preparation, but source discrepancies can remain; the low Ariel Investments value needs review.
- **Modest predictive performance.** Random Forest performs slightly better than the mean-salary benchmark, with MAE about $18,300 and R² 0.126. The models were compared using the same cross-validation results, with no separate final test. Predictions are too uncertain to serve as precise individual salary estimates.
- **Skills and pay are not causal measures.** Skill mentions describe posting requirements. Team proficiency is self-assessed, and the eight technical groups do not cover every skill. Neither demand percentages nor model importance establish hiring probability or a pay increase from learning a skill.

## Product Boundaries and Next Steps

The prototype supports **learning priorities, experience fit, employer research and salary benchmarks**. It does not yet provide live vacancy tracking, verified readiness scores, personalized offer predictions, or evidence that its advice improves hiring outcomes.

To strengthen the product:

1. Collect more recent, independent postings across states and employers, and verify salary values.
2. Assess skills through practical tasks and gather feedback from students using the recommendations.
3. Evaluate models on new employers or a later time period before offering individual salary estimates.
