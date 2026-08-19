import pandas as pd


def get_overall_metrics(df, level_median, momentum_median):
    """Calculate high-level dashboard metrics."""

    metrics = {
        "total_districts": len(df),

        "critical_priority": (
            df["quadrant"] == "Critical Priority"
        ).sum(),

        "high_momentum": (
            df["delta"] >= momentum_median
        ).sum(),

        "states": df["state"].nunique(),

        "median_baseline": level_median,

        "median_momentum": momentum_median,
    }

    return metrics


def get_critical_by_state(df):
    """Count Critical Priority districts by state."""

    critical = df[
        df["quadrant"] == "Critical Priority"
    ]

    return (
        critical
        .groupby("state")
        .size()
        .sort_values(ascending=False)
    )


def get_top_momentum_districts(df, n=5):
    """Return districts with the highest improvement momentum."""

    return (
        df
        .sort_values("delta", ascending=False)
        .head(n)
    )


def get_lowest_level_districts(df, n=5):
    """Return districts with the lowest baseline scores."""

    return (
        df
        .sort_values("baseline_score")
        .head(n)
    )


def get_quadrant_summary(df):
    """Return district count by development profile."""

    return (
        df["quadrant"]
        .value_counts()
        .rename_axis("quadrant")
        .reset_index(name="districts")
    )


if __name__ == "__main__":

    from preprocessing import merge_datasets
    from segmentation import create_quadrants

    df = merge_datasets()

    df, level_median, momentum_median = create_quadrants(df)

    metrics = get_overall_metrics(
        df,
        level_median,
        momentum_median
    )

    print("\nOverall metrics:")
    print(metrics)

    print("\nCritical Priority by state:")
    print(get_critical_by_state(df).head(10))

    print("\nTop momentum districts:")
    print(
        get_top_momentum_districts(df)[
            ["district", "state", "delta"]
        ]
    )

    print("\nLowest baseline districts:")
    print(
        get_lowest_level_districts(df)[
            ["district", "state", "baseline_score"]
        ]
    )