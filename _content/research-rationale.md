# DRAFT — WIP

## 1 Research rationale

Students preparing for Data Analyst careers must connect their current capabilities to the requirements of actual employers. A job title alone does not explain which skills a position requires, how much experience is expected, whether compensation is disclosed, or whether the work arrangement fits a job seeker's circumstances. This project develops a career evaluation prototype for students and aspiring Data Analysts considering securities, investments, and related financial activities.

The target user is a student or early-career job seeker pursuing a **Data Analyst / Data Analytics** pathway. The primary focus is **skill and career readiness**. Salary, experience, location, and employment patterns provide supporting evidence for deciding where to apply and what to learn next. This framing follows the AD688 running case, which asks teams to connect an industry-scoped dataset to practical job-seeker decisions [@ad688case].

Reliable industry labels are important because an incorrectly classified employer can distort a sector-specific career benchmark. Chern et al. investigate employer-industry errors arising from employer identification and industry attributes, using posting-derived signals to help detect them [@chern2018]. For this project, the implication is to document how industry membership is selected and to treat potentially inconsistent employer labels as a data-quality limitation.

The selected industry provides a setting in which to examine whether technical tools, analytical methods, and business knowledge appear together in Data Analyst postings. Which skills recur most often, and whether they are associated with particular salary or experience bands, are questions for the analysis rather than established findings.

## 2 Scope and research questions

### Industry and career scope selection

**Financial Services – Data Analytics**

| Scope component               | Selected scope                                                                          |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| Target career pathway         | Data Analyst / Data Analytics                                                           |
| NAICS classification revision | 2022                                                                                    |
| Selected dataset code         | `523`                                                                                 |
| Classification level          | Three-digit subsector within sector `52`, Finance and Insurance                       |
| Industry label                | Securities, Commodity Contracts, and Other Financial Investments and Related Activities |
| Primary analytical focus      | Skill and career readiness                                                              |
| Supporting dimensions         | Salary, experience, geography, remote work, and employment type                         |

NAICS 523 covers securities and commodity intermediation, exchanges, and other investment-related services. It is narrower than the full Finance and Insurance sector and does not represent all financial-services employment. NAICS describes the economic activity of an establishment; it does not identify an employee's occupation [@naics2022]. A Data Analyst title and an employer's industry code therefore serve different purposes in the cohort definition.

The course guide prefers four- or six-digit industry codes where possible [@ad688case]. Group 4 uses the selected three-digit subsector to examine Data Analyst opportunities across related investment activities, while retaining more detailed codes for within-scope comparisons. The report should acknowledge the wider scope and avoid treating its subindustries as interchangeable.

The primary industry filter is `naics_2022_3 = '523'`. The group notes also use the notation `523000`; this project uses `523` consistently for the three-digit scope. A six-digit dataset value beginning with `523` can support a cross-check, but should not be assumed to provide an identical cohort when fields are incomplete or inconsistent.

Reference: [NAICS 523 industry description](https://www.naics.com/naics-code-description/?code=523).

### Primary project question

> What skills, experience levels, salary opportunities, and employment patterns should aspiring Data Analysts understand when pursuing careers in securities, investments, and related financial services (NAICS 523), and how can job seekers use these factors to evaluate their career readiness and identify areas for upskilling?

### Supporting research questions

1. **RQ1 — Skills and requirements:** Which technical, software, business, and specialized skills recur in the selected postings, and how do stated education and experience requirements vary?
2. **RQ2 — Opportunity patterns:** How do disclosed salary ranges, locations, remote-work arrangements, and employment types vary within the selected industry-career cohort?
3. **RQ3 — Career readiness:** How do the observed skill requirements compare with the team's self-assessed capabilities, and which learning priorities follow from a transparent comparison?

The career cohort will require both the industry filter and a documented title match in `title_raw` or `title_clean`. The current title rule recognizes Data Analyst and selected explicit variants, including Data & Insights Analyst, Data Analytics Analyst, and Analyst – Data Analysis. It can retain senior titles and can miss roles expressed differently. Experience and seniority must therefore be assessed separately; the cohort should not automatically be described as entry-level.

## 3 Short literature review

Five sources support the project's scope, data-quality approach, and interpretation. This is a focused narrative review rather than a systematic review.

**Employer-industry classification.** Goindani et al. examine employer-industry classification using job postings [@goindani2017]. The study provides a methodological reference for using recruitment records to examine employer classification. Its relevance here is to make industry selection explicit and review questionable labels. Classification research provides context for cohort quality; it does not establish skill demand or salary levels in this project's NAICS 523 sample.

**Industry-label error detection.** Chern et al. use employer names, employer descriptions, job titles, and job descriptions to identify possible industry-classification errors, comparing support vector machine and random forest approaches [@chern2018]. Their findings motivate checking employer and posting information when industry membership is uncertain. The paper's predictive results concern its own dataset and are not evidence of this project's accuracy or a requirement to reproduce its models.

**Representativeness of online postings.** Tsvetkova et al. compare Lightcast vacancies with official sources in Australia, Canada, the United Kingdom, and the United States [@tsvetkova2024]. They identify variation in representativeness across geography, occupation, and industry. This supports reporting the observed posting sample and its coverage rather than equating posting counts with all vacancies or employment. Their results do not provide a correction factor for the MET Career Compass dataset.

**Industry definition and analytical boundaries.** The 2022 NAICS manual supplies the classification framework used to define the selected subsector [@naics2022]. It supports keeping employer industry distinct from career pathway and retaining detailed industry labels for interpretation. This prevents a financial-services label from being used as a substitute for a Data Analyst title filter.

**Reproducible analytical implementation.** Pedregosa et al. describe scikit-learn as a general-purpose Python machine-learning library [@pedregosa2011]. The source is relevant if the final project uses a Python predictive or segmentation model. In that case, package versions, preprocessing, evaluation, and parameter choices must be documented separately. The software paper does not establish which skills financial employers require or validate a career-readiness scorecard.

Together, these sources support an industry-scoped, reproducible career benchmark with explicit limits. The proposed contribution is to turn posting evidence and self-assessed skills into interpretable learning and application priorities. The project does not claim to improve a proprietary classification system or demonstrate that acquiring a particular skill causes employment.

## 4 Analytical expectations and design status

The project will explore whether the selected postings reveal recurring combinations of technical tools, business capabilities, and experience requirements. SQL, Python, Excel, visualization tools, statistics, and business analysis are candidate skill categories to examine; their relative importance must be established from the selected records.

The analysis will also examine whether disclosed compensation and remote-work patterns vary with experience, location, or detailed industry group. Such comparisons describe associations within the sample. Missing salary information, unequal subgroup sizes, and inconsistent labels may restrict which comparisons are useful.

A career evaluation component will compare posting-derived skill demand with the team's existing self-assessments. Any scorecard will explain its dimensions, scaling, and weighting choices. A self-rating and a skill's posting frequency measure different things, so they should not be subtracted directly without a defined conversion rule. Rankings should be checked for sensitivity to reasonable changes in weights.

These are exploratory expectations, not reported results. This document does not establish a sample size, collection period, salary median, top-skill ranking, or model performance. Those findings must come from the cleaned project dataset and documented analysis. The running case's title retains “2024,” while the working dataset is named `Jobs_2026`; the final report should state the actual observed posting dates and snapshot provenance [@ad688case; @careercompass2026].

## 5 Data fields and intended use

### Posting data

The following fields are drawn from the supplied project filtering code. Their presence and types should be checked against the loaded Parquet schema before analysis. An API response should be mapped separately rather than assumed to have identical fields [@careercompass2026].

| Purpose                                 | Fields                                                                                                                                                                         | Intended use and interpretation control                                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| Record identity, dates, and duplicates  | `id`, `posted`, `is_duplicate`, `duplicate_of_id`                                                                                                                      | Document the posting window; check ID uniqueness; report duplicate exclusions and unknown duplicate status.                 |
| Industry scope                          | `naics_2022_3`, `naics_2022_3_name`, `naics_2022_4`, `naics_2022_4_name`, `naics_2022_5`, `naics_2022_5_name`, `naics_2022_6`, `naics_2022_6_name`             | Filter the three-digit code to 523; retain detailed classifications for within-scope comparisons and consistency checks.    |
| Career selection and occupation context | `title_raw`, `title_clean`, `soc_2021_5`, `soc_2021_5_name`, `onet`, `onet_name`                                                                                   | Apply the declared title rule; review occupation labels and ambiguous matches; distinguish role from employer industry.     |
| Employer context and source evidence    | `company_name`, `company_is_staffing`, `url`, `body`                                                                                                                   | Inspect employer and staffing flags; retain posting evidence for reviewing unexpected industry or title matches.            |
| Skills                                  | `skills_name`, `software_skills_name`, `specialized_skills_name`                                                                                                         | Decode and standardize skill lists; count each skill once per posting; avoid double counting overlapping skill fields.      |
| Education, experience, and credentials  | `min_years_experience`, `max_years_experience`, `education_levels_name`, `certifications_name`                                                                         | Build interpretable requirement groups; preserve unknown values; do not assume a missing experience requirement means zero. |
| Compensation                            | `text_salary_from`, `text_salary_to`, `text_pay_frequency`, `text_pay_currency`, `normalized_salary_from`, `normalized_salary_to`, `salary_normalization_status` | Verify currency, pay period, normalization, and valid ranges; report salary coverage and both bounds.                       |
| Employment and location                 | `remote_type_name`, `employment_type_name`, `city_name`, `state_name`, `parsed_country_iso_abbr`                                                                     | Define geographic scope; compare stated arrangements and employment types; show missing or unknown categories.              |
| Derived audit fields                    | `career_match_reason`, `analysis_include`                                                                                                                                  | Explain which title matched and which rows enter the analysis.                                                              |

The supplied filtering code includes rows in the analytical subset only when `is_duplicate` is explicitly false. True and null values are excluded from that subset. This rule uses the dataset's flag and does not independently resolve all repeated postings or employer aliases. The number excluded for each reason should be reported.

References

::: {#refs}
:::
