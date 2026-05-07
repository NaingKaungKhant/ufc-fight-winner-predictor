# UFC Fight Winner Prediction App

## Project Goal

This project aims to build a portfolio-level data science application that predicts the winner of a UFC fight using historical fight data and fighter statistics.

The finished project will combine data collection, data cleaning, exploratory data analysis, feature engineering, machine learning, model evaluation, and a Streamlit web app for interactive predictions.

## Planned Workflow

1. Collect and organize UFC fight and fighter statistics data.
2. Clean the raw data and create analysis-ready datasets.
3. Explore patterns in fighter attributes, fight history, and outcomes.
4. Engineer predictive features from historical fighter performance.
5. Train and evaluate machine learning models.
6. Build a Streamlit app that allows users to enter two fighters and view a predicted winner.

## Current Status

Initial project structure created. Step 1, data collection and organization, has started.

No UFC dataset has been added yet and no model has been trained.

## Project Structure

```text
.
├── app/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── src/
├── README.md
└── requirements.txt
```

## Folder Purpose

- `app/`: Streamlit application code for the final interactive prediction tool.
- `data/`: Raw and processed datasets used throughout the project.
- `data/raw/`: Original downloaded datasets. These files should not be manually edited.
- `data/processed/`: Cleaned datasets created from the raw data.
- `models/`: Saved trained models and model evaluation artifacts.
- `notebooks/`: Jupyter notebooks for exploration, cleaning, feature engineering, and modeling experiments.
- `src/`: Reusable Python modules for data processing, features, modeling, and utilities.

## Step 1: Data Collection

The first data science task is to collect historical UFC fight data and place the original files in `data/raw/`.

Important beginner rule: keep raw data unchanged. When we clean or transform data later, we will save new files in `data/processed/`.

The first raw dataset source has been documented in `docs/data_sources.md`. Raw UFCStats CSV files are stored in `data/raw/ufcstats/`.

## Step 2: Initial Data Cleaning

The first cleaning script is `src/clean_data.py`.

It creates beginner-friendly processed files in `data/processed/`:

- `clean_fight_results.csv`
- `clean_fighter_tott.csv`
- `cleaning_summary.md`

This step standardizes columns, extracts explicit winners from fight outcomes, parses fighter measurements, and keeps modeling work for later.
