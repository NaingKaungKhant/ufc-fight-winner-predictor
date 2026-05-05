# 02 Initial Data Inventory

This step records what raw UFC data files entered the project.

The goal is not to clean data yet. The goal is to answer basic questions:

1. Which raw CSV files do we have?
2. How many rows and columns does each file contain?
3. Which file likely contains the target variable, meaning the fight winner?
4. Which files contain fighter attributes or fight statistics?

The companion script for this step is:

```bash
python src/data_inventory.py
```

This script uses Python's built-in `csv` module so it can run even before the full data science environment is installed.

