# Mobile Usage vs Academic Performance: Data Analysis

## 📌 Project Overview
This project explores the relationship between a student's leisure/social activity (a proxy for mobile usage in modern research) and their final academic grades. We use the **UCI Student Performance Dataset**, a globally recognized real-world dataset, to ensure authentic results.

## 🛠️ How to Set Up and Run (using UV)
This project is built using the `uv` environment for maximum speed and reliability. No manual `pip` commands are required.

1.  **Clone/Open the project folder**.
2.  **Sync Dependencies**:
    ```bash
    uv sync
    ```
3.  **Run the Analysis**:
    ```bash
    uv run mobile_academic_analysis/main_analysis.py
    ```

## 📊 Dataset Structure
The project uses the `student-mat.csv` from the UCI Repository:
- **`goout` (Social/Mobile Usage Proxy)**: Frequency of going out with friends (1 - very low to 5 - very high).
- **`G3` (Academic Performance)**: Final grade (numeric: from 0 to 20).
- **Other features**: Age, study time, family support, and health.

## 📈 Visualizations Generated
- **Line Graph**: Shows the downward trend in average grades as mobile/social time increases.
- **Bar Chart**: Compares the average final grades between 'Low', 'Medium', and 'High' usage groups.
- **Scatter Plot**: Displays individual student data points with a regression line to show the negative correlation.
- **Density Plot**: Shows the distribution of grades, revealing that 'High Usage' students have a peak at lower grade values.

## 📝 Key Findings
The analysis shows a clear negative correlation. Students with lower social/mobile distractions consistently maintain higher grade averages, whereas high usage levels are associated with a noticeable drop in academic performance.
