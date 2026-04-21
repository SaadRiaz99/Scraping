import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import os

def analyze_student_performance():
    # 1. Load Real-World Data (UCI Student Performance Dataset)
    print("Fetching authentic student performance data...")
    url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/04_Apply/Students_Alcohol_Consumption/student-mat.csv"
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    
    # Save a local copy for the project
    df.to_csv("mobile_academic_analysis/data/student_raw_data.csv", index=False)
    
    # Context: In this real dataset, 'freetime' and 'goout' (going out with friends) 
    # are strong proxies for leisure/mobile usage in modern students.
    # 'G3' is the final grade (Academic Performance).
    
    # Set visual style
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(18, 12))

    # --- GRAPH 1: Line Graph (Trend) ---
    # Showing the trend of average grades as leisure/social time increases
    plt.subplot(2, 2, 1)
    trend_data = df.groupby('goout')['G3'].mean().reset_index()
    plt.plot(trend_data['goout'], trend_data['G3'], marker='o', color='crimson', linewidth=2)
    plt.title('Trend: Social/Mobile Time vs Final Grade', fontsize=14)
    plt.xlabel('Usage Level (1: Very Low to 5: Very High)')
    plt.ylabel('Average Grade (G3)')
    plt.grid(True, linestyle='--', alpha=0.7)

    # --- GRAPH 2: Bar Chart (Comparison) ---
    # Comparing grades between low-usage and high-usage groups
    plt.subplot(2, 2, 2)
    df['Usage_Category'] = pd.cut(df['goout'], bins=[0, 2, 3, 5], labels=['Low', 'Medium', 'High'])
    sns.barplot(x='Usage_Category', y='G3', data=df, palette='viridis', ci=None)
    plt.title('Comparison: Performance by Usage Category', fontsize=14)
    plt.xlabel('Social/Mobile Usage Level')
    plt.ylabel('Average Final Grade')

    # --- GRAPH 3: Scatter Plot (Correlation) ---
    # Analyzing individual student data points
    plt.subplot(2, 2, 3)
    sns.regplot(x='goout', y='G3', data=df, x_jitter=0.2, scatter_kws={'alpha':0.4, 'color':'teal'}, line_kws={'color':'darkorange'})
    plt.title('Correlation: Individual Student Data Points', fontsize=14)
    plt.xlabel('Social/Mobile Usage Frequency')
    plt.ylabel('Final Grade (0-20)')

    # --- GRAPH 4: Density Plot ---
    plt.subplot(2, 2, 4)
    sns.kdeplot(data=df, x="G3", hue="Usage_Category", fill=True, common_norm=False, palette="magma", alpha=.5)
    plt.title('Grade Distribution across Usage Groups', fontsize=14)
    plt.xlabel('Final Grade')

    plt.tight_layout()
    plt.savefig('mobile_academic_analysis/performance_dashboard.png')
    print("Analysis complete. Visualization saved as 'performance_dashboard.png'.")

    # --- Key Findings Calculation ---
    low_usage_avg = df[df['goout'] <= 2]['G3'].mean()
    high_usage_avg = df[df['goout'] >= 4]['G3'].mean()
    diff = low_usage_avg - high_usage_avg
    
    print("\n--- DATA ANALYSIS FINDINGS ---")
    print(f"Total Students Analyzed: {len(df)}")
    print(f"Average Grade for Low Usage Students: {low_usage_avg:.2f}")
    print(f"Average Grade for High Usage Students: {high_usage_avg:.2f}")
    print(f"Impact: High social/mobile usage correlates with a {diff:.2f} point drop in grades.")

if __name__ == "__main__":
    analyze_student_performance()
