import pandas as pd


BASELINE_PATH = "data/baseline_ranking.csv"
DELTA_PATH = "data/delta_ranking.csv"


def load_data():
    """Load the baseline and delta ranking datasets."""

    baseline = pd.read_csv(BASELINE_PATH)
    delta = pd.read_csv(DELTA_PATH)

    return baseline, delta


def get_data_summary():
    """Return basic information about both datasets."""

    baseline, delta = load_data()

    summary = {
        "baseline_rows": len(baseline),
        "delta_rows": len(delta),
        "baseline_columns": list(baseline.columns),
        "delta_columns": list(delta.columns),
    }

    return summary


if __name__ == "__main__":

    baseline, delta = load_data()

    print("Baseline dataset:")
    print(baseline.head())

    print("\nBaseline shape:", baseline.shape)

    print("\nDelta dataset:")
    print(delta.head())

    print("\nDelta shape:", delta.shape)