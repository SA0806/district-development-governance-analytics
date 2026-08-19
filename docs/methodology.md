# Methodology

This document explains the analytical approach behind the District Development & Governance Analytics project: how the data is prepared, how districts are scored and segmented and why each modelling choice was made.

---

## 1. Data

Two datasets, both derived from NITI Aayog's Aspirational Districts Programme, are used:

| File | Rows | Columns | Description |
|---|---|---|---|
| `data/baseline_ranking.csv` | 101 | `district`, `state`, `baseline_score`, `baseline_rank` | Composite development score and national rank for each district at baseline. |
| `data/delta_ranking.csv` | 108 | `district`, `state`, `delta`, `delta_rank` | Improvement (change) score and rank for each district over the measurement period. |

The two files do not cover an identical set of districts. The delta file includes several districts (largely in Odisha, e.g. Malkangiri, Gajapati, Kalahandi, Mewat, Dhenkanal, Rayagada, Nabarangapur, Kandhamal) that are absent from the baseline file and are therefore excluded once the two datasets are merged (see Section 2.2). This is a property of the source data, not a filtering decision made during analysis.

## 2. Preprocessing (`src/preprocessing.py`)

### 2.1 District name standardisation

The two datasets use inconsistent spellings or historical names for a small number of districts. A manual alias map (`DISTRICT_ALIASES`) resolves these before merging:

| Baseline/ Delta name | Standardised as |
|---|---|
| Cuddapah/ Y.S.R. | YSR Kadapa |
| Dohad | Dahod |
| Dhaulpur | Dholpur |
| Bhoopalpalli | Bhoopalapalli |
| Pashchimi Singhbhum | West Singbhum |

Each district name is also stripped of whitespace and lower-cased into a `district_key` used purely for joining -- the original `district` column (from the baseline file) is retained for display.

### 2.2 Merging

The baseline and delta datasets are joined on `district_key` using an **inner join**. This means:

- A district must appear in **both** files to be included in the analysis.
- Districts present in only one file (see Section 1) are dropped.
- The merge yields **101 districts** -- every baseline district successfully matches a delta record once aliases are applied.

This is a deliberate trade-off: an inner join guarantees that every analysed district has both a level and a momentum score, which the Level-Momentum framework requires. The cost is that a small number of districts with only a delta score are excluded from this analysis.

## 3. Level-Momentum Framework (`src/segmentation.py`)

### 3.1 Defining the two axes

- **Level** = `baseline_score` -- how developed a district currently is.
- **Momentum** = `delta` -- how much a district has improved over the measurement period.

### 3.2 Quadrant segmentation

Each axis is split at its **median** across the merged 101-district dataset:

- Median baseline score: **35.42**
- Median delta: **5.70**

Using the median rather than an arbitrary fixed cutoff keeps the framework relative to the actual distribution of districts in this cohort and transparent -- anyone can recompute the same thresholds directly from the data.

Each district falls into one of four quadrants:

| Level | Momentum | Quadrant |
|---|---|---|
| >= median | >= median | High Level/ High Momentum |
| >= median | < median | High Level/ Low Momentum |
| < median | >= median | Low Level/ High Momentum |
| < median | < median | Critical Priority |

This produces a simple, explainable classification that a non-technical stakeholder can verify by hand.

## 4. Machine Learning Layer (`src/segmentation.py`)

As a secondary, exploratory technique, **K-Means clustering** (`k = 4`) is applied to the same two features (`baseline_score`, `delta`).

### 4.1 Why standardise first

`baseline_score` and `delta` are on different scales, so both are standardised (zero mean, unit variance) using `StandardScaler` before clustering. Without this step, the feature with the larger numeric range would dominate the distance calculation K-Means relies on.

### 4.2 Why `k = 4`

Four clusters were chosen to mirror the four quadrants of the policy framework, making the two segmentations directly comparable, rather than because four is statistically optimal (e.g. via an elbow-method or silhouette analysis). This is a conscious simplification, noted as a limitation.

### 4.3 Interpreting clusters

K-Means itself only returns cluster numbers (0-3), not labels. Each cluster's centre (in standardised space) is inspected relative to the origin -- the average district -- and mapped to a human-readable profile:

| Centre position | Profile |
|---|---|
| Level below average, momentum below average | Lagging & Stalled |
| Level below average, momentum above average | Lagging but Accelerating |
| Level above average, momentum below average | Established but Slowing |
| Level above average, momentum above average | Leading Accelerators |

Because cluster assignment depends on the data-driven centroid positions (not fixed medians), the K-Means segmentation can and does disagree with the quadrant segmentation for some districts near the boundary. This disagreement is intentional and useful: it flags districts where the two methods give a different read, which is often worth a closer look.

## 5. Policy Translation (`src/recommendations.py`)

Each of the four **quadrant** labels (not the K-Means clusters) is mapped to a short, generic policy recommendation. The recommendations are analytical starting points, not district-specific interventions -- they are intentionally generic because they are derived only from two summary indicators (level and momentum), not from sector-level data.

## 6. Summary Statistics (`src/insights.py`)

National and state-level summaries -- total districts, Critical Priority count, high-momentum count, states represented, Critical Priority districts by state, top-momentum districts and lowest-baseline districts -- are computed directly from the merged, quadrant-labelled dataset and surfaced in the dashboard's overview panels.

## 7. Known Limitations

- Only two indicators (baseline level and delta) are used; no sector-level (health, education, agriculture, infrastructure) breakdown is incorporated.
- Median-based thresholds are transparent but simplify what is likely a more continuous underlying reality.
- `k = 4` for K-Means was chosen for interpretability and comparability with the quadrant model, not validated against alternative values of `k`.
- Cluster and quadrant labels are analytical interpretations produced by this project, not official NITI Aayog classifications.
- Recommendations are generic per-quadrant text, not district-specific policy advice and should be validated against local context before use.
- The analysis does not establish causal relationships between any intervention and district outcomes.