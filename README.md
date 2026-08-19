# District Development & Governance Analytics

A data-driven governance prioritisation framework built using data from **NITI Aayog's Aspirational Districts Programme (ADP)**. The project identifies districts that are developmentally lagging, evaluates how quickly they are improving and turns those findings into targeted, actionable policy recommendations.

<!-- 🚧 **Status:** Project under active development -->

---

## Table of Contents

- [Objective](#objective)
- [Key Questions](#key-questions)
- [Methodology](#methodology)
- [Data Source](#data-source)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Objective

To identify districts that are developmentally lagging, assess their improvement momentum and translate quantitative findings into targeted governance recommendations - helping policymakers prioritise attention and resources where they matter most.

## Key Questions

- Which districts are performing poorly relative to the national aspirational-district cohort?
- Which low-performing districts are improving rapidly?
- Which districts are both low-performing **and** stagnant?
- Which regions and sectors require greater policy attention?

## Methodology

```
Official NITI Aayog Data
        ↓
Data Cleaning & Normalisation
        ↓
Baseline + Delta Data Integration
        ↓
Level–Momentum Analysis
        ↓
K-Means Clustering
        ↓
District Segmentation
        ↓
Policy Recommendations
```

The core idea is a **level–momentum framework**: districts are scored both on their current performance *level* (how far behind they are) and their *momentum* (rate of improvement over time). Combining these two axes via K-Means clustering segments districts into actionable groups - for example, "low level, low momentum" districts that most urgently need intervention versus "low level, high momentum" districts that are already on the right track.

## Data Source

- [NITI Aayog - Aspirational Districts Programme](https://www.niti.gov.in/aspirational-districts-programme)

## Project Structure

```
district-development-governance-analytics/
├── data/          # Raw and processed NITI Aayog datasets
├── docs/          # Documentation, notes and supporting material
├── notebooks/     # Exploratory analysis and modelling notebooks
├── src/           # Core source code (cleaning, analysis, clustering)
├── app.py         # Streamlit dashboard application
├── style.css      # Custom styling for the Streamlit app
├── requirements.txt
└── README.md
```

## Tech Stack

- **Python**
- **Pandas** & **NumPy** - data processing and manipulation
- **Scikit-learn** - K-Means clustering and modelling
- **Plotly** - interactive data visualisation
- **Streamlit** - interactive web dashboard

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/SA0806/district-development-governance-analytics.git
cd district-development-governance-analytics

# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run the Streamlit dashboard locally:

```bash
streamlit run app.py
```

This launches an interactive app where you can explore district-level performance, momentum scores and cluster segmentation.

Analysis notebooks used for exploration and model development are available in the [`notebooks/`](notebooks) directory.

## Roadmap

- [ ] Finalise data cleaning and normalisation pipeline
- [ ] Validate clustering approach across sectors (health, education, agriculture, infrastructure)
- [ ] Expand policy recommendation logic
- [ ] Polish and deploy the Streamlit dashboard
- [ ] Add automated tests and documentation

## Contributing

Contributions, issues and feature requests are welcome. Feel free to open an issue or submit a pull request.


---

*Built to support evidence-based governance and policy prioritisation across India's aspirational districts.*