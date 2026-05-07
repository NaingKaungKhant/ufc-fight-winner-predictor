# Data Cleaning

This step converts raw UFCStats CSV files into cleaner processed datasets.

## Script

Run the cleaning script from the project root:

```bash
python src/clean_data.py
```

If using the project virtual environment:

```bash
.venv/bin/python src/clean_data.py
```

## Processed Outputs

The script creates:

- `data/processed/clean_fight_results.csv`
- `data/processed/clean_fighter_tott.csv`
- `data/processed/cleaning_summary.md`

## What Gets Cleaned

For fight results:

- standardizes column names
- strips extra spaces from text values
- splits `BOUT` into `fighter_1` and `fighter_2`
- converts outcome codes like `W/L` and `L/W` into explicit winner and loser columns
- flags draws and no contests
- joins event date and location

For fighter tale-of-the-tape:

- standardizes column names
- converts height to inches
- converts weight to pounds
- converts reach to inches
- flags fighters over 300 lbs as extreme weight values for later analysis
- flags fighters with complete height, weight, and reach measurements
- parses date of birth into a date column

## What This Step Does Not Do

This step does not train a model and does not create final machine learning features.
