"""Clean raw UFCStats data into beginner-friendly processed CSV files.

This is the first real data cleaning step. It does not train a model.

Outputs:
- data/processed/clean_fight_results.csv
- data/processed/clean_fighter_tott.csv
- data/processed/cleaning_summary.md
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "ufcstats"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def clean_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Convert messy CSV column names into lowercase snake_case names."""
    cleaned_columns = (
        dataframe.columns.str.strip()
        .str.lower()
        .str.replace(".", "", regex=False)
        .str.replace("%", "pct", regex=False)
        .str.replace(" ", "_", regex=False)
    )

    dataframe = dataframe.copy()
    dataframe.columns = cleaned_columns
    return dataframe


def strip_text_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Remove extra spaces from text columns and convert '--' to missing."""
    dataframe = dataframe.copy()

    for column in dataframe.select_dtypes(include="object").columns:
        dataframe[column] = dataframe[column].str.strip()

    return dataframe.replace({"--": pd.NA, "": pd.NA})


def split_bout_column(series: pd.Series) -> pd.DataFrame:
    """Split 'Fighter A vs. Fighter B' into two fighter-name columns."""
    fighters = series.str.split(" vs. ", n=1, expand=True)
    fighters.columns = ["fighter_1", "fighter_2"]
    return fighters


def parse_height_to_inches(value: object) -> float:
    """Convert a height like 5' 11\" into total inches.

    Missing values stay missing because models cannot use strings such as
    "5' 11\"" directly. Later, we can decide how to impute missing heights.
    """
    if pd.isna(value):
        return np.nan

    match = re.search(r"(\d+)'\s*(\d+)", str(value))

    if not match:
        return np.nan

    feet = int(match.group(1))
    inches = int(match.group(2))
    return float(feet * 12 + inches)


def parse_number(value: object) -> float:
    """Extract the first number from strings like '155 lbs.' or '66\"'."""
    if pd.isna(value):
        return np.nan

    match = re.search(r"\d+(\.\d+)?", str(value))
    return float(match.group(0)) if match else np.nan


def clean_fight_results() -> pd.DataFrame:
    """Create a cleaned fight-level table with an explicit winner column."""
    fights = pd.read_csv(RAW_DATA_DIR / "ufc_fight_results.csv")
    events = pd.read_csv(RAW_DATA_DIR / "ufc_event_details.csv")

    fights = strip_text_columns(clean_column_names(fights))
    events = strip_text_columns(clean_column_names(events))

    fighters = split_bout_column(fights["bout"])
    fights = pd.concat([fights, fighters], axis=1)

    outcomes = fights["outcome"].str.split("/", n=1, expand=True)
    fights["fighter_1_result"] = outcomes[0]
    fights["fighter_2_result"] = outcomes[1]

    fights["winner"] = np.select(
        [
            fights["fighter_1_result"].eq("W"),
            fights["fighter_2_result"].eq("W"),
        ],
        [
            fights["fighter_1"],
            fights["fighter_2"],
        ],
        default=pd.NA,
    )

    fights["loser"] = np.select(
        [
            fights["fighter_1_result"].eq("L"),
            fights["fighter_2_result"].eq("L"),
        ],
        [
            fights["fighter_1"],
            fights["fighter_2"],
        ],
        default=pd.NA,
    )

    fights["is_draw"] = fights["outcome"].eq("D/D")
    fights["is_no_contest"] = fights["outcome"].eq("NC/NC")
    fights["has_winner"] = fights["winner"].notna()

    fights["weight_class"] = fights["weightclass"].str.replace(
        " Bout", "", regex=False
    )
    fights["round"] = pd.to_numeric(fights["round"], errors="coerce")

    events["date"] = pd.to_datetime(events["date"], errors="coerce")
    events = events.rename(columns={"url": "event_url"})

    fights = fights.rename(columns={"url": "fight_url"})
    fights = fights.merge(
        events[["event", "date", "location", "event_url"]],
        on="event",
        how="left",
    )

    selected_columns = [
        "event",
        "date",
        "location",
        "bout",
        "fighter_1",
        "fighter_2",
        "outcome",
        "fighter_1_result",
        "fighter_2_result",
        "winner",
        "loser",
        "has_winner",
        "is_draw",
        "is_no_contest",
        "weight_class",
        "method",
        "round",
        "time",
        "time_format",
        "referee",
        "details",
        "fight_url",
        "event_url",
    ]

    return fights[selected_columns].sort_values(["date", "event", "bout"])


def clean_fighter_tott() -> pd.DataFrame:
    """Create a cleaned fighter tale-of-the-tape table."""
    fighters = pd.read_csv(RAW_DATA_DIR / "ufc_fighter_tott.csv")
    fighters = strip_text_columns(clean_column_names(fighters))

    fighters["height_inches"] = fighters["height"].apply(parse_height_to_inches)
    fighters["weight_lbs"] = fighters["weight"].apply(parse_number)
    fighters["reach_inches"] = fighters["reach"].apply(parse_number)
    fighters["date_of_birth"] = pd.to_datetime(fighters["dob"], errors="coerce")
    fighters["is_extreme_weight"] = fighters["weight_lbs"].gt(300)
    fighters["has_complete_measurements"] = fighters[
        ["height_inches", "weight_lbs", "reach_inches"]
    ].notna().all(axis=1)

    fighters = fighters.rename(columns={"url": "fighter_url"})

    selected_columns = [
        "fighter",
        "height",
        "height_inches",
        "weight",
        "weight_lbs",
        "reach",
        "reach_inches",
        "is_extreme_weight",
        "has_complete_measurements",
        "stance",
        "dob",
        "date_of_birth",
        "fighter_url",
    ]

    return fighters[selected_columns].sort_values("fighter")


def write_cleaning_summary(
    clean_fights: pd.DataFrame, clean_fighters: pd.DataFrame
) -> None:
    """Write a short Markdown summary of the cleaned output files."""
    summary_path = PROCESSED_DATA_DIR / "cleaning_summary.md"

    summary = f"""# Data Cleaning Summary

This summary was generated by `src/clean_data.py`.

## Files Created

- `clean_fight_results.csv`
- `clean_fighter_tott.csv`

## Cleaned Fight Results

- Rows: {len(clean_fights):,}
- Columns: {clean_fights.shape[1]:,}
- Fights with winners: {clean_fights["has_winner"].sum():,}
- Draws: {clean_fights["is_draw"].sum():,}
- No contests: {clean_fights["is_no_contest"].sum():,}

## Cleaned Fighter Tale Of The Tape

- Rows: {len(clean_fighters):,}
- Columns: {clean_fighters.shape[1]:,}
- Fighters with height in inches: {clean_fighters["height_inches"].notna().sum():,}
- Fighters with reach in inches: {clean_fighters["reach_inches"].notna().sum():,}
- Fighters over 300 lbs: {clean_fighters["is_extreme_weight"].sum():,}
- Fighters with complete measurements: {clean_fighters["has_complete_measurements"].sum():,}

## Notes

This step cleans the raw data structure but does not create model features yet.
Feature engineering will happen later after exploratory data analysis.
"""

    summary_path.write_text(summary, encoding="utf-8")


def main() -> None:
    """Run the cleaning pipeline and save processed CSV files."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    clean_fights = clean_fight_results()
    clean_fighters = clean_fighter_tott()

    clean_fights.to_csv(PROCESSED_DATA_DIR / "clean_fight_results.csv", index=False)
    clean_fighters.to_csv(PROCESSED_DATA_DIR / "clean_fighter_tott.csv", index=False)
    write_cleaning_summary(clean_fights, clean_fighters)

    print("Saved cleaned fight results and fighter attributes.")
    print(f"Clean fight rows: {len(clean_fights):,}")
    print(f"Clean fighter rows: {len(clean_fighters):,}")


if __name__ == "__main__":
    main()
