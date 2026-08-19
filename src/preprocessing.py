import pandas as pd

from data_loader import load_data


# Different names used for the same district
DISTRICT_ALIASES = {
    "Cuddapah": "YSR Kadapa",
    "Y.S.R.": "YSR Kadapa",
    "Dohad": "Dahod",
    "Dhaulpur": "Dholpur",
    "Bhoopalpalli": "Bhoopalapalli",
    "Pashchimi Singhbhum": "West Singbhum",
}


def clean_district_names(df):
    """Standardise district names for reliable merging."""

    df = df.copy()

    df["district_key"] = (
        df["district"]
        .replace(DISTRICT_ALIASES)
        .str.strip()
        .str.lower()
    )

    return df


def merge_datasets():
    """Clean and merge baseline and delta datasets."""

    baseline, delta = load_data()

    baseline = clean_district_names(baseline)
    delta = clean_district_names(delta)

    merged = baseline.merge(
        delta[["district_key", "delta", "delta_rank"]],
        on="district_key",
        how="inner"
    )

    return merged


if __name__ == "__main__":

    df = merge_datasets()

    print("Merged dataset:")
    print(df.head())

    print("\nMerged shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())