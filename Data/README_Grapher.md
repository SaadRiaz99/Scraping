# Automated CSV Grapher (UV Project)

## Project Overview
This project is an automated data visualization tool. It scans a specific folder for CSV files and generates a **Bar Chart** and a **Line Graph** for every file found. It is designed to be completely dynamic—just drop a new CSV file into the folder, and the graphs will be generated automatically.

## How to Install Dependencies
This project uses `uv` for lightning-fast dependency management. You don't need to use `pip`.

1.  **Install `uv`** (if not already installed):
    Follow instructions at [astral.sh/uv](https://astral.sh/uv).
2.  **Sync Dependencies**:
    Run the following command in the project root:
    ```bash
    uv sync
    ```
    This will automatically install `pandas` and `matplotlib` into a virtual environment.

## How to Run the Project
To run the script and generate your graphs using the `uv` environment, use:
```bash
uv run grapher.py
```

## CSV File Structure
For the script to work correctly, your CSV files should follow this simple structure:
- **Column 1**: Labels (e.g., Names, Months, Categories)
- **Column 2**: Numerical Values (e.g., Scores, Prices, Counts)

Example (`sales.csv`):
```csv
Month,Sales
January,150
February,200
```

## How Graphs are Generated
- **Bar Chart**: Generated using `plt.bar()`. It uses a sky-blue color scheme and is ideal for comparing categories.
- **Line Graph**: Generated using `plt.plot()`. It uses a red line with markers to show trends over time or sequence.
- **Dynamic Processing**: The script uses the `glob` library to find every file ending in `.csv` inside the `csv_data/` folder, ensuring you never have to edit the code to add new data.

All generated graphs are saved in the `output_graphs/` folder with names like `filename_bar.png` and `filename_line.png`.
