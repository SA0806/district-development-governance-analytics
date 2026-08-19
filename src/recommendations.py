from preprocessing import merge_datasets
from segmentation import create_quadrants


RECOMMENDATIONS = {
    "Critical Priority": (
        "Prioritise foundational service delivery, "
        "monitor leading indicators, and escalate "
        "persistent state-level bottlenecks."
    ),

    "Low Level / High Momentum": (
        "Study successful implementation practices "
        "and identify interventions that can be replicated."
    ),

    "High Level / Low Momentum": (
        "Diagnose sector-specific bottlenecks "
        "and protect existing development gains."
    ),

    "High Level / High Momentum": (
        "Document best practices and use the district "
        "as a peer-learning benchmark."
    )
}


def get_recommendation(quadrant):
    """Return a policy recommendation for a district profile."""

    return RECOMMENDATIONS.get(
        quadrant,
        "No recommendation available."
    )


def add_recommendations(df):
    """Add policy recommendations to the district dataset."""

    df = df.copy()

    df["policy_recommendation"] = (
        df["quadrant"]
        .map(get_recommendation)
    )

    return df


if __name__ == "__main__":

    df = merge_datasets()

    df, level_median, momentum_median = create_quadrants(df)

    df = add_recommendations(df)

    print("\nSample policy recommendations:\n")

    print(
        df[
            [
                "district",
                "quadrant",
                "policy_recommendation"
            ]
        ].head(10).to_string(index=False)
    )