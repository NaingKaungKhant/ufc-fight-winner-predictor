# Data Sources

## Selected Source: Greco1899 UFCStats CSV Exports

For the first version of this project, the raw data comes from the public GitHub repository:

<https://github.com/Greco1899/scrape_ufc_stats>

The repository provides CSV files scraped from UFCStats. This is useful for a beginner portfolio project because the data is already exported as CSV files, so we can focus on learning the data science workflow before building a custom web scraper.

## Raw Files Downloaded

The following files were saved in `data/raw/ufcstats/`:

- `ufc_event_details.csv`
- `ufc_fight_details.csv`
- `ufc_fight_results.csv`
- `ufc_fight_stats.csv`
- `ufc_fighter_details.csv`
- `ufc_fighter_tott.csv`

## Why This Source Is Useful

- It contains fight-level UFC history.
- It includes fighter-level information.
- It includes fight result data, which is needed for winner prediction.
- It separates raw fight, event, and fighter tables, which is good practice for learning joins and feature engineering.

## Important Notes

- The raw CSV files should stay unchanged.
- Any cleaned or merged datasets should be saved later in `data/processed/`.
- Before modeling, we still need to inspect the columns, handle missing values, and decide which tables should be joined.
- This project should cite the original source if published on GitHub or used in a portfolio.

