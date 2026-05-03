# Data Folder

This folder stores the datasets used in the UFC fight winner prediction project.

## Folder Structure

```text
data/
├── raw/
├── processed/
└── README.md
```

## Folder Purpose

- `raw/`: Original datasets exactly as downloaded. Do not manually edit these files.
- `processed/`: Cleaned or transformed datasets created from the raw data.

## Data Collection Plan

For the next stage, we will look for historical UFC fight data with fields such as:

- fight date
- event name
- weight class
- fighter names
- winner
- method of victory
- round and time
- fighter age, height, reach, stance, and record
- strike, grappling, takedown, and submission statistics

The important rule is: raw data should stay unchanged. Any cleaning or feature engineering should create new files in `data/processed/`.

