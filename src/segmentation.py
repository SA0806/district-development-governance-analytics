import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from preprocessing import merge_datasets


def create_quadrants(df):
    """Classify districts using median development level and momentum."""

    level_median = df["baseline_score"].median()
    momentum_median = df["delta"].median()

    conditions = [
        (df["baseline_score"] >= level_median) &
        (df["delta"] >= momentum_median),

        (df["baseline_score"] >= level_median) &
        (df["delta"] < momentum_median),

        (df["baseline_score"] < level_median) &
        (df["delta"] >= momentum_median),

        (df["baseline_score"] < level_median) &
        (df["delta"] < momentum_median)
    ]

    labels = [
        "High Level / High Momentum",
        "High Level / Low Momentum",
        "Low Level / High Momentum",
        "Critical Priority"
    ]

    df = df.copy()

    df["quadrant"] = np.select(
        conditions,
        labels,
        default="Unclassified"
    )

    return df, level_median, momentum_median


def create_clusters(df):
    """Cluster districts using development level and momentum."""

    features = df[
        ["baseline_score", "delta"]
    ]

    scaler = StandardScaler()

    X = scaler.fit_transform(features)

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=20
    )

    df = df.copy()

    df["cluster"] = model.fit_predict(X)

    # Get cluster centres in standardised space
    centers = model.cluster_centers_

    # Give each cluster a meaningful interpretation.
    #
    # x-axis = development level
    # y-axis = improvement momentum

    cluster_profiles = {}

    for cluster_id, center in enumerate(centers):

        level = center[0]
        momentum = center[1]

        if level < 0 and momentum < 0:

            profile = "Lagging & Stalled"

        elif level < 0 and momentum >= 0:

            profile = "Lagging but Accelerating"

        elif level >= 0 and momentum < 0:

            profile = "Established but Slowing"

        else:

            profile = "Leading Accelerators"

        cluster_profiles[cluster_id] = profile

    df["cluster_profile"] = (
        df["cluster"]
        .map(cluster_profiles)
    )

    return df


if __name__ == "__main__":

    df = merge_datasets()

    df, level_median, momentum_median = create_quadrants(df)

    df = create_clusters(df)

    print("\nMedian baseline score:", round(level_median, 2))

    print(
        "Median momentum:",
        round(momentum_median, 2)
    )

    print("\nQuadrant distribution:")

    print(
        df["quadrant"].value_counts()
    )

    print("\nCluster profile distribution:")

    print(
        df["cluster_profile"].value_counts()
    )

    print("\nSample:")

    print(
        df[
            [
                "district",
                "baseline_score",
                "delta",
                "quadrant",
                "cluster_profile"
            ]
        ].head(10)
    )