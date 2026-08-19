# District Development & Governance Analytics

An interactive data analytics platform for analysing India's Aspirational Districts using development-level and improvement-momentum data from NITI Aayog.

The project combines transparent policy segmentation, unsupervised machine learning, and interactive visualisation to identify districts that require prioritisation, districts showing strong improvement, and districts that can serve as benchmarks for peer learning.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Analytical Framework](#analytical-framework)
- [Machine Learning](#machine-learning)
- [Policy Translation](#policy-translation)
- [Dashboard](#dashboard)
- [Project Structure](#project-structure)
- [Data Pipeline](#data-pipeline)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running the Analytical Pipeline](#running-the-analytical-pipeline)
- [Example Findings](#example-findings)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Data Sources](#data-sources)
- [Why This Project?](#why-this-project)
<!-- - [Author](#author) -->
- [License](#license)

---

## Overview

Governance decisions often require answering two questions:

1. **How developed is a district currently?**
2. **How quickly is the district improving?**

This project introduces a **Level–Momentum Framework** that analyses both dimensions simultaneously.

Each district is classified into one of four development profiles:

| Profile | Interpretation |
|---|---|
| High Level / High Momentum | Strong development with strong improvement |
| High Level / Low Momentum | Strong development but slowing improvement |
| Low Level / High Momentum | Lower development but improving rapidly |
| Critical Priority | Lower development with weak improvement |

A secondary **K-Means clustering model** provides an independent, unsupervised segmentation of districts.

## Key Features

- Interactive district-level analytics dashboard
- State and development-profile filters
- Development Level vs Improvement Momentum scatter plot
- Median-based Level–Momentum segmentation
- K-Means clustering on standardised district indicators
- Interpretable ML cluster profiles
- National state-level priority analysis
- Top momentum and lowest-development district analysis
- District Explorer with individual recommendations
- Policy-oriented recommendations based on analytical profiles

## Analytical Framework

### 1. Development Level

The project uses the **NITI Aayog baseline composite score** (`baseline_score`) as the measure of development level.

### 2. Improvement Momentum

The project uses the corresponding **delta/improvement score** (`delta`) to represent improvement momentum.

### 3. Level–Momentum Matrix

The median values of the two variables are used as transparent thresholds:

```text
                         HIGH MOMENTUM
                              │
          Low Level /         │       High Level /
          High Momentum       │       High Momentum
                              │
──────────────────────────────┼────────────────────────
                              │
          Critical            │       High Level /
          Priority            │       Low Momentum
                              │
                         LOW MOMENTUM
```

This produces the four policy-oriented development profiles listed above.

## Machine Learning

K-Means clustering (`k=4`) is applied as a secondary, unsupervised segmentation technique using standardised `baseline_score` and `delta` values.

### Pipeline

```
Baseline Score + Momentum
            ↓
     Feature Standardisation
            ↓
        K-Means (k=4)
            ↓
     Cluster Identification
            ↓
 Meaningful Cluster Interpretation
```

Cluster centres are interpreted relative to the origin in standardised space and mapped to one of four labels:

- **Leading Accelerators**
- **Established but Slowing**
- **Lagging but Accelerating**
- **Lagging & Stalled**

The clustering layer is used as an exploratory analytical tool rather than as a replacement for the transparent, median-based policy framework.

## Policy Translation

The analytical profiles are translated into governance-oriented recommendations. Examples:

**Critical Priority**
> Prioritise foundational service delivery, monitor leading indicators, and escalate persistent state-level bottlenecks.

**Low Level / High Momentum**
> Study successful implementation practices and identify interventions that can be replicated.

**High Level / High Momentum**
> Document best practices and use the district as a peer-learning benchmark.

**High Level / Low Momentum**
> Diagnose sector-specific bottlenecks and protect existing development gains.

## Dashboard

The Streamlit dashboard provides:

**National Overview**
- Total districts analysed
- Critical Priority districts
- High-momentum districts
- States / UTs represented

**Interactive Analysis**

Users can filter districts by:
- State
- Development Profile

The scatter plot dynamically updates based on the selected filters.

**District Explorer**

For an individual district, the dashboard displays:
- State
- Baseline development score
- Improvement momentum
- Baseline rank
- Development profile
- ML cluster profile
- Policy recommendation

## Project Structure

```
district-development-governance-analytics/
│
├── app.py                        # Streamlit dashboard application
├── style.css                     # Custom dashboard styling
├── requirements.txt
├── README.md
│
├── data/
│   ├── baseline_ranking.csv      # district, state, baseline_score, baseline_rank
│   └── delta_ranking.csv         # district, state, delta, delta_rank
│
├── src/
│   ├── data_loader.py            # Loads baseline and delta CSVs
│   ├── preprocessing.py          # Cleans district names and merges datasets
│   ├── segmentation.py           # Level–Momentum quadrants + K-Means clustering
│   ├── recommendations.py        # Maps development profiles to policy actions
│   └── insights.py               # National/state-level summary statistics
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
└── docs/
    └── methodology.md
```

## Data Pipeline

```
NITI Aayog Data
      │
      ├── Baseline Ranking
      │
      └── Delta / Improvement Ranking
               │
               ▼
        Data Loading
               │
               ▼
       Data Preprocessing
      (district name standardisation)
               │
               ▼
      Dataset Alignment
       (inner merge on district)
               │
               ▼
    Level–Momentum Analysis
               │
        ┌──────┴──────┐
        ▼             ▼
   Quadrant Model   K-Means
        │             │
        └──────┬──────┘
               ▼
      Policy Recommendations
               │
               ▼
      Interactive Dashboard
```

## Tech Stack

**Language**
- Python

**Data Analysis**
- Pandas
- NumPy

**Machine Learning**
- Scikit-learn
- K-Means Clustering
- StandardScaler

**Visualisation**
- Plotly

**Dashboard**
- Streamlit

**Development**
- Git
- GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/SA0806/district-development-governance-analytics.git
```

Move into the project directory:

```bash
cd district-development-governance-analytics
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will open in your browser.

## Running the Analytical Pipeline

Each module in `src/` can also be run independently for inspection, from the project root, with `src` on the Python path:

**Data Loading**
```bash
PYTHONPATH=src python src/data_loader.py
```

**Preprocessing**
```bash
PYTHONPATH=src python src/preprocessing.py
```

**Segmentation and Clustering**
```bash
PYTHONPATH=src python src/segmentation.py
```

**Policy Recommendations**
```bash
PYTHONPATH=src python src/recommendations.py
```

**Analytical Insights**
```bash
PYTHONPATH=src python src/insights.py
```

*(On Windows, set the path first with `set PYTHONPATH=src`.)*

## Example Findings

Running the pipeline on the included datasets produces:

- **101** districts analysed
- **31** districts classified as **Critical Priority**
- **51** districts with above-median improvement momentum
- **25** states / UTs represented
- Median baseline score: **35.42** · Median momentum (delta): **5.7**

Critical Priority districts are geographically concentrated — **Jharkhand (11)** and **Bihar (8)** together account for over 60% of identified priority districts, followed by Assam and Uttar Pradesh (4 each).

The districts with the strongest improvement momentum (Dahod, West Sikkim, Ramanathapuram, Vizianagaram, and Cuddapah/YSR Kadapa) illustrate the framework's second use case: surfacing districts whose implementation practices may be worth studying and replicating elsewhere.

## Limitations

- The analysis is based on the two publicly available baseline and delta ranking datasets; it does not incorporate sector-level indicators individually.
- The Level–Momentum framework uses median thresholds, which provide transparency but may simplify underlying development dynamics.
- K-Means results depend on the selected features and number of clusters (`k=4` was chosen for interpretability, not statistically optimised).
- Cluster labels are analytical interpretations, not official government classifications.
- Policy recommendations are analytical suggestions and should be validated against local administrative, socioeconomic, and sector-specific context.
- The project does not claim causal relationships between interventions and development outcomes.

## Future Improvements

- Sector-level analysis across health, education, agriculture, and financial inclusion
- Time-series monitoring of district performance
- State-level comparative dashboards
- Geospatial district visualisation
- Automated policy brief generation
- Additional clustering and dimensionality-reduction techniques
- Integration of newer Aspirational District datasets
- Deployment as a public-facing governance analytics platform

## Data Sources

The project uses district-level data published by NITI Aayog's Aspirational Districts Programme, including baseline development scores and improvement/delta rankings.

The datasets used in this repository are included under [`data/`](data).

Source reports should be referenced alongside the corresponding datasets when reproducing the analysis.

## Why This Project?

The project was designed to combine:

**Data → Diagnosis → Segmentation → Insight → Policy Recommendation**

rather than treating data visualisation as the final output.

The goal is to demonstrate how quantitative analysis and machine learning can support structured governance and development decision-making.

<!-- ## Author

**Sahiba Joshi**
Mechanical Engineering | IIT Indore -->

## License

This project is intended for educational, analytical, and portfolio purposes.