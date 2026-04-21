# Mobile Usage vs Academic Performance Project

## Project Overview
This project identifies, collects, and analyzes human behavior data specifically focusing on how **Mobile Phone Usage** impacts **Academic Performance**. It uses a dataset of 150 students to demonstrate behavioral trends.

## What I Can Do
I have performed the following tasks autonomously:
1.  **Data Identification:** Identified relevant human behavior datasets (E-commerce and Student Performance).
2.  **Dataset Creation:** Generated a specific dataset of **150 records** for the topic "Mobile Usage vs Academic Performance".
3.  **Data Analysis:**
    *   Calculated data size and identified feature columns.
    *   Detected and reported missing values.
    *   Analyzed correlations between habits (Mobile/Study/Sleep) and results (Exam Scores).
4.  **Visualizations:** Created multiple graphical reports:
    *   `final_150_data_line.png`: A complete line graph of all 150 students.
    *   `academic_performance_analysis.png`: Correlation heatmaps and trend analysis.
    *   `mobile_performance_150_graph.png`: Comparison of study vs. mobile influence.
5.  **Data Export:** Provided clean CSV files (`mobile_performance_150.csv`) for use in other tools like Power BI.

## Dataset Features (150 Records)
- **Input Features:** `Age`, `Gender`, `Mobile_Usage_Hours`, `Social_Media_Hours`, `Study_Hours`, `Sleep_Hours`.
- **Target Output:** `Exam_Score`.

## How to Run
All scripts are managed using `uv`. To regenerate the data and graphs, run:
```powershell
uv run final_analysis.py
```

## Files in this Project
- `mobile_performance_150.csv`: The primary dataset (150 lines).
- `final_150_data_line.png`: The main visualization of all student data.
- `analyze_performance.py`: The original analysis script.
- `run_all.py`: Master script to run all project components.
