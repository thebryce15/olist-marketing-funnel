<!--
  README for Olist Marketing Funnel Case Study
  Streamlined for non-technical audiences • Updated June 2025
-->

# Olist Marketing Funnel Case Study

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)  
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](#tech-stack--dependencies)  
[![Tableau Public](https://img.shields.io/badge/Tableau-Public-orange.svg)](#live-dashboard)  

---

## At a Glance

- **Goal:** Identify which marketing channels deliver the highest revenue per lead and where the biggest funnel drop-offs occur.  
- **Impact:**  
  - **$138 per lead** from “Unknown” segment (highest ROI)  
  - **Paid campaigns** under‑deliver (6.3 % conv, \$48 Rev/Lead)  
  - **Front-load campaigns** in Q1 to maximize seasonal peaks  
- **Audience:** Marketing Managers, Campaign Leads, BI/Analytics Teams  
- **Live Dashboard:** [View the Tableau dashboard](#) ← *insert your Tableau Public link here*  

---

## Table of Contents

1. [Overview](#overview)  
2. [Key Metrics & Findings](#key-metrics--findings)  
3. [Live Dashboard](#live-dashboard)  
4. [Data & Methodology](#data--methodology)  
5. [Tech Stack & Dependencies](#tech-stack--dependencies)  
6. [Setup & Installation](#setup--installation)  
7. [Usage](#usage)  
8. [Project Structure](#project-structure)  
9. [Additional Resources](#additional-resources)  
10. [Troubleshooting](#troubleshooting)  
11. [Contributing](#contributing)  
12. [License & Contact](#license--contact)  

---

## Overview

Uncover which acquisition sources deliver the best ROI (conversion × revenue per lead) and pinpoint process bottlenecks so marketing can optimize budget and follow-up cadence.

---

## Key Metrics & Findings

- **Unknown Leads (16% of volume):**  
  - Conversion Rate: **14.0%**  
  - Revenue per Lead: **$138**  
- **Paid Channels:**  
  - Conversion Rate: **6.3%**  
  - Revenue per Lead: **$48**  
  - *Action:* Reallocate budget or adjust messaging  
- **Organic Traffic:**  
  - Volume Share: **55%** of leads  
  - Conversion Rate: **9.3%**  
  - Revenue per Lead: **$66**  
- **Seasonality:**  
  - **Jan–Apr** peak in revenue per lead  
  - Recommend front-loading major promotions  

---

## Live Dashboard

🔗 **Tableau Public Dashboard:**  
[Insert your Tableau link here]

> *No setup required—just click and explore key channel filters, time-series trends, and funnel drop-offs.*

---

## Data & Methodology

- **Source Datasets:**  
  - [Brazilian E-commerce (Olist)](https://www.kaggle.com/olistbr/brazilian-ecommerce)  
  - [Marketing Funnel Olist](https://www.kaggle.com/olistbr/marketing-funnel-olist)  
- **Volume & Time Span:**  
  - 7 CSV tables (~1 million rows)  
  - Jan–Dec 2024  
- **Workflow:**  
  1. **ETL (Python):** Clean & stage raw CSVs  
  2. **SQL:** Funnel & revenue aggregation  
  3. **Tableau:** Dashboards & visualizations  
  4. **Reporting:** Stakeholder deck & write-up  

---

## Tech Stack & Dependencies

- **Languages & Tools:**  
  - Python 3.8+  
  - PostgreSQL (or any RDBMS)  
  - Tableau Desktop / Reader / Public  
  - PowerPoint / Google Slides  
- **Key Libraries:**  
  - pandas, numpy, psycopg2-binary  
  - tableau-api-lib  
- **Requirements File:**  
  ```bash
  pip install -r scripts/requirements.txt
  ```  

---

## Project Structure

```
Olist_Marketing_Funnel/
├── data/
│   ├── raw/         ← original CSVs
│   └── processed/   ← cleaned staging tables
├── scripts/
│   ├── import_data.py
│   ├── run_funnel_queries.py
│   ├── export_charts.py
│   └── requirements.txt
├── tableau/
│   ├── Olist_Project.twbx
│   └── images/      ← exported PNGs
├── slides/
│   └── Olist_Marketing_Presentation.pptx
├── docs/
│   └── Olist_Case_Study_Writeup.pdf
└── README.md
```

---

## Additional Resources

- **Full Methodology:** `docs/Olist_Marketing_Funnel_Case_Study.pdf`  
- **Stakeholder Deck:** `slides/Olist_Marketing_Presentation.pdf`

---

## License & Contact

- **License:** MIT  
- **Email:** brycesmithx@gmail.com  
- **GitHub:** https://github.com/thebryce15  
