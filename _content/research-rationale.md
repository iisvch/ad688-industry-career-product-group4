## Research rationale

Students preparing for Data Analyst careers must connect their current capabilities to the requirements of actual employers. A job title alone does not explain which skills a position requires, how much experience is expected, whether compensation is disclosed, or whether the work arrangement fits a job seeker's circumstances. This project develops a career evaluation prototype for students and aspiring Data Analysts considering securities, investments, and related financial activities.

The target user is a student or early-career job seeker pursuing a **Data Analyst / Data Analytics** pathway. The primary focus is **skill and career readiness**. Salary, experience, location, and employment patterns provide supporting evidence for deciding where to apply and what to learn next. This framing follows the AD688 running case, which asks teams to connect an industry-scoped dataset to practical job-seeker decisions.

Reliable industry labels are important because an incorrectly classified employer can distort a sector-specific career benchmark. Chern et al. investigate employer-industry errors arising from employer identification and industry attributes, using posting-derived signals to help detect them [@chern2018]. For this project, the implication is to document how industry membership is selected and to treat potentially inconsistent employer labels as a data-quality limitation.

The completed study uses **140 Lightcast postings from May–September 2024**, representing **102 distinct employer/title/description profiles**. It moves from data preparation and the market baseline to skill gaps, salary analysis and practical career recommendations. Salary is available for **86 postings**, representing **48 distinct profiles**; the remaining postings still inform the wider market and skill analysis.

## Scope and research questions

### Industry and career scope selection

**Financial Services – Data Analytics**

| Scope component               | Selected scope                                                                          |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| Target career pathway         | Data Analyst / Data Analytics                                                           |
| NAICS classification revision | 2022                                                                                    |
| Selected dataset code         | `523`                                                                                 |
| Industry label                | Securities, Commodity Contracts, and Other Financial Investments and Related Activities |
| Primary analytical focus      | Skill and career readiness                                                              |
| Supporting dimensions         | Salary, experience, geography, remote work, and employers                               |

NAICS 523 covers securities and commodity intermediation, exchanges, and other investment-related services. It is narrower than the full Finance and Insurance sector and does not represent all financial-services employment. NAICS describes the economic activity of an establishment; it does not identify an employee's occupation [@naics2022]. A Data Analyst title and an employer's industry code therefore serve different purposes in the cohort definition.

Group 4 uses the three-digit subsector to examine Data Analyst opportunities across related investment activities. The findings apply to this selected cohort, rather than all financial-services employment. A separate career-title filter identifies the Data Analyst roles within the industry.

Reference: [NAICS 523 industry description](https://www.naics.com/naics-code-description/?code=523).

### Primary project question

> What skills, experience levels, salary opportunities, and employment patterns should aspiring Data Analysts understand when pursuing careers in securities, investments, and related financial services (NAICS 523), and how can job seekers use these factors to evaluate their career readiness and identify areas for upskilling?

### Job-seeker decisions

- **Skills:** Which tools should I strengthen and demonstrate in a portfolio?
- **Experience:** Which roles match my background and stated requirements?
- **Compensation:** What salary benchmark can help me compare similar roles?
- **Search priorities:** Which employers, locations and work arrangements should I investigate?

## Short literature review

Five sources support the project's scope, data-quality approach, and interpretation. This is a focused narrative review rather than a systematic review.

**Employer-industry classification.** Goindani et al. examine employer-industry classification using job postings [@goindani2017]. The study provides a methodological reference for using recruitment records to examine employer classification. Its relevance here is to make industry selection explicit and review questionable labels. Classification research provides context for cohort quality; it does not establish skill demand or salary levels in this project's NAICS 523 sample.

**Industry-label error detection.** Chern et al. use employer names, employer descriptions, job titles, and job descriptions to identify possible industry-classification errors, comparing support vector machine and random forest approaches [@chern2018]. Their findings motivate checking employer and posting information when industry membership is uncertain. The paper's predictive results concern its own dataset and are not evidence of this project's accuracy or a requirement to reproduce its models.

**Representativeness of online postings.** Tsvetkova et al. compare Lightcast vacancies with official sources in Australia, Canada, the United Kingdom, and the United States [@tsvetkova2024]. They identify variation in representativeness across geography, occupation, and industry. This supports reporting the observed posting sample and its coverage rather than equating posting counts with all vacancies or employment. Their results do not provide a correction factor for the MET Career Compass dataset.

**Industry definition and analytical boundaries.** The 2022 NAICS manual supplies the classification framework used to define the selected subsector [@naics2022]. It supports keeping employer industry distinct from career pathway and retaining detailed industry labels for interpretation. This prevents a financial-services label from being used as a substitute for a Data Analyst title filter.

**Reproducible analytical implementation.** Pedregosa et al. describe scikit-learn as a general-purpose Python machine-learning library [@pedregosa2011]. The project uses Python to compare multiple linear regression, Random Forest and an average-salary baseline. The analysis notebook documents preprocessing and checks predictions on held-out posting groups, keeping repeated job descriptions together. The software paper does not establish which skills financial employers require or validate a career-readiness scorecard.

Together, these sources support an industry-scoped, reproducible career benchmark with explicit limits. The project's contribution is to turn posting evidence and self-assessed skills into interpretable learning and application priorities. The recommendations prioritize SQL, Python and BI development, matching experience requirements, using descriptive salary benchmarks and verifying work arrangements. The salary models provide supporting evidence; they do not define a job seeker's readiness. The project does not claim to improve a proprietary classification system or demonstrate that acquiring a particular skill causes employment.

## Data fields and intended use

| Variable                    | Description                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| `ID`                      | Unique Lightcast job-posting identifier.                                         |
| `LAST_UPDATED_DATE`       | Date the job posting record was last updated.                                    |
| `POSTED`                  | Date the job posting was posted.                                                 |
| `EXPIRED`                 | Date the job posting expired, when available.                                    |
| `TITLE_RAW`               | Original job title from the Lightcast posting.                                   |
| `BODY`                    | Job-posting description text.                                                    |
| `COMPANY_NAME`            | Employer name.                                                                   |
| `EDUCATION_LEVELS_NAME`   | Education-level information associated with the posting.                         |
| `MIN_YEARS_EXPERIENCE`    | Minimum years of experience required, when available.                            |
| `MAX_YEARS_EXPERIENCE`    | Maximum years of experience required, when available.                            |
| `SALARY`                  | Original salary field.                                                           |
| `REMOTE_TYPE`             | Lightcast remote-work classification code.                                       |
| `REMOTE_TYPE_NAME`        | Readable remote-work classification.                                             |
| `ORIGINAL_PAY_PERIOD`     | Original pay-period label; stored salary amounts are already annualized.         |
| `SALARY_TO`               | Upper annualized salary endpoint used in the analysis.                           |
| `SALARY_FROM`             | Lower annualized salary endpoint used in the analysis.                           |
| `LOCATION`                | Original job location field.                                                     |
| `CITY_NAME`               | City associated with the posting.                                                |
| `STATE_NAME`              | State associated with the posting.                                               |
| `NAICS3`                  | Three-digit NAICS industry subsector code.                                       |
| `NAICS3_NAME`             | Name of the three-digit NAICS industry subsector.                                |
| `TITLE`                   | Standardized Lightcast job title.                                                |
| `TITLE_NAME`              | Named occupational/job-title classification.                                     |
| `TITLE_CLEAN`             | Cleaned job title field.                                                         |
| `SKILLS`                  | Lightcast coded skills associated with the posting.                              |
| `SKILLS_NAME`             | Readable skill names.                                                            |
| `SPECIALIZED_SKILLS`      | Lightcast specialized skill codes.                                               |
| `SPECIALIZED_SKILLS_NAME` | Readable specialized skill names.                                                |
| `COMMON_SKILLS`           | Lightcast common skill codes.                                                    |
| `COMMON_SKILLS_NAME`      | Readable common skill names.                                                     |
| `SOFTWARE_SKILLS`         | Lightcast software skill codes.                                                  |
| `SOFTWARE_SKILLS_NAME`    | Readable software skill names.                                                   |
| `ONET`                    | O*NET occupation code.                                                           |
| `ONET_NAME`               | O*NET occupation name.                                                           |
| `SOC_2021_5`              | Five-digit SOC 2021 occupation code.                                             |
| `SOC_2021_5_NAME`         | Name of the five-digit SOC 2021 occupation classification.                       |
| `remote_status`           | Cleaned remote-work classification; missing classifications are labeled Unknown. |
| `city_clean`              | Cleaned city field.                                                              |
| `state_clean`             | Cleaned state field.                                                             |
| `salary_midpoint`         | Average of the two annualized salary endpoints; target of the salary regression. |
| `industry_scope`          | Analysis industry scope, defined as NAICS 523.                                   |
| `career_scope`            | Career filter used for the revised core Data Analyst sample.                     |


## Study and Product Limitations

The findings are exploratory because the sample is small, historical and unevenly distributed across regions and employers. Salary disclosure and missing job requirements further limit generalization. The career-readiness prototype helps organize learning and compare roles; it does not yet verify readiness or predict individual offers reliably. The report's [Limitations](limitations.qmd) section documents these boundaries and the next improvements.
