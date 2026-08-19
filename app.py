import sys
import os

import streamlit as st
import pandas as pd
import plotly.express as px

# Allow Python to find modules inside src/
sys.path.append(
    os.path.join(os.path.dirname(__file__), "src")
)

from preprocessing import merge_datasets
from segmentation import create_quadrants, create_clusters
from recommendations import add_recommendations

from insights import (
    get_overall_metrics,
    get_critical_by_state,
    get_top_momentum_districts,
    get_lowest_level_districts,
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="District Development Analytics",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# CUSTOM STYLING
# ==================================================

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_processed_data():

    df = merge_datasets()

    df, level_median, momentum_median = create_quadrants(df)

    df = create_clusters(df)

    df = add_recommendations(df)

    return df, level_median, momentum_median


df, level_median, momentum_median = load_processed_data()


# ==================================================
# METRICS
# ==================================================

metrics = get_overall_metrics(
    df,
    level_median,
    momentum_median
)


# ==================================================
# HEADER
# ==================================================

st.title("District Development & Governance Analytics")

st.markdown(
    """
    **Level–Momentum Framework**

    A data-driven analysis of India's Aspirational Districts
    using NITI Aayog's baseline and improvement data.
    """
)

st.divider()


# ==================================================
# KPI CARDS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Districts Analysed",
    metrics["total_districts"]
)

col2.metric(
    "Critical Priority",
    metrics["critical_priority"]
)

col3.metric(
    "High Momentum",
    metrics["high_momentum"]
)

col4.metric(
    "States / UTs",
    metrics["states"]
)


st.divider()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df["state"].unique())
)

selected_quadrant = st.sidebar.selectbox(
    "Select Development Profile",
    ["All"] + sorted(df["quadrant"].unique())
)


filtered_df = df.copy()

if selected_state != "All":

    filtered_df = filtered_df[
        filtered_df["state"] == selected_state
    ]

if selected_quadrant != "All":

    filtered_df = filtered_df[
        filtered_df["quadrant"] == selected_quadrant
    ]


# ==================================================
# LEVEL–MOMENTUM CHART
# ==================================================

st.subheader(
    "Development Level vs Improvement Momentum"
)

fig = px.scatter(
    filtered_df,
    x="baseline_score",
    y="delta",
    color="quadrant",
    hover_name="district",
    hover_data={
        "state": True,
        "baseline_score": ":.2f",
        "delta": ":.1f",
        "quadrant": True,
    },
    labels={
        "baseline_score": "Baseline Development Score",
        "delta": "Improvement Momentum",
    },
)


fig.add_vline(
    x=level_median,
    line_dash="dash",
)

fig.add_hline(
    y=momentum_median,
    line_dash="dash",
)


fig.update_layout(
    height=600,
    legend_title="Development Profile",
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ==================================================
# STATE INSIGHTS
# ==================================================

st.divider()

st.subheader("National State-Level Priority Analysis")

st.caption(
    "National benchmark — unaffected by the dashboard filters."
)

critical_states = get_critical_by_state(df)

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "### Critical Priority by State"
    )

    state_chart = px.bar(
        critical_states.head(10),
        orientation="h",
        labels={
            "value": "Critical Priority Districts",
            "state": "State",
        },
    )

    state_chart.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=400,
    )

    st.plotly_chart(
        state_chart,
        use_container_width=True
    )


with col2:

    st.markdown(
        "### Priority Concentration"
    )

    if len(critical_states) >= 2:

        top_two = (
            critical_states.iloc[:2].sum()
        )

        percentage = (
            top_two /
            metrics["critical_priority"] *
            100
        )

        st.metric(
            "Top 2 States",
            f"{top_two} districts"
        )

        st.metric(
            "Share of Critical Priority",
            f"{percentage:.0f}%"
        )

        st.write(
            f"**{critical_states.index[0]}** "
            f"has {critical_states.iloc[0]} "
            f"Critical Priority districts."
        )

        st.write(
            f"**{critical_states.index[1]}** "
            f"has {critical_states.iloc[1]} "
            f"Critical Priority districts."
        )


# ==================================================
# TOP / BOTTOM DISTRICTS
# ==================================================

st.divider()

st.subheader("National District Performance Leaders & Laggards")

st.caption(
    "National benchmark — showing the highest momentum "
    "and lowest baseline districts across the full dataset."
)

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "### Highest Momentum"
    )

    top_momentum = get_top_momentum_districts(
        df
    )

    st.dataframe(
        top_momentum[
            [
                "district",
                "state",
                "delta",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


with col2:

    st.markdown(
        "### Lowest Development Level"
    )

    lowest_level = get_lowest_level_districts(
        df
    )

    st.dataframe(
        lowest_level[
            [
                "district",
                "state",
                "baseline_score",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# ==================================================
# DISTRICT EXPLORER
# ==================================================

st.divider()

st.subheader("District Explorer")

# Use filtered districts when filters are active.
# Fall back to all districts if no filter is applied.

if len(filtered_df) > 0:

    district_options = sorted(
        filtered_df["district"].unique()
    )

else:

    district_options = []


if district_options:

    selected_district = st.selectbox(
        "Select a district",
        district_options
    )

    district = df[
        df["district"] == selected_district
    ].iloc[0]

else:

    st.warning(
        "No districts match the selected filters."
    )

    district = None


district = df[
    df["district"] == selected_district
].iloc[0]


if district is not None:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "State",
        district["state"]
    )

    col2.metric(
        "Baseline Score",
        f'{district["baseline_score"]:.2f}'
    )

    col3.metric(
        "Momentum",
        f'{district["delta"]:.1f}'
    )

    col4.metric(
        "Baseline Rank",
        int(district["baseline_rank"])
    )

    st.markdown(
        f"### {district['district']}"
    )

    st.write(
        f"**Development Profile:** "
        f"{district['quadrant']}"
    )

    st.write(
        f"**ML Cluster Profile:** "
        f"{district['cluster_profile']}"
    )

    st.info(
        district["policy_recommendation"]
    )

# ==================================================
# METHODOLOGY
# ==================================================

st.divider()

with st.expander("Methodology & Analytical Framework"):

    st.markdown(
        """
        ### 1. Development Level

        Each district is evaluated using its NITI Aayog
        baseline composite score.

        ### 2. Improvement Momentum

        The delta score represents the district's measured
        improvement between the baseline and first delta
        assessment.

        ### 3. Level–Momentum Segmentation

        Districts are divided using the median baseline score
        and median momentum score:

        - High Level / High Momentum
        - High Level / Low Momentum
        - Low Level / High Momentum
        - Critical Priority

        ### 4. K-Means Clustering

        K-Means clustering is applied to standardised
        baseline score and momentum features.

        The resulting clusters are interpreted as:

        - Leading Accelerators
        - Established but Slowing
        - Lagging but Accelerating
        - Lagging & Stalled

        ### 5. Policy Translation

        Analytical profiles are translated into
        governance-oriented recommendations focused on
        prioritisation, replication and bottleneck diagnosis.
        """
    )

# ==================================================
# COMPLETE DATASET
# ==================================================

st.divider()

st.subheader("District Dataset")

display_columns = [
    "district",
    "state",
    "baseline_score",
    "delta",
    "quadrant",
    "cluster_profile",
]


st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
)
st.sidebar.markdown("---")

st.sidebar.metric(
    "Filtered Districts",
    len(filtered_df)
)