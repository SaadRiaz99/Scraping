import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_mobile_performance_subset():
    # Load the mobile performance data and take 150 lines
    file_path = "mobile_usage_academic_performance.csv"
    if not pd.io.common.file_exists(file_path):
        print("Error: Dataset file not found.")
        return
        
    df = pd.read_csv(file_path).head(150)
    df.to_csv("mobile_performance_150.csv", index=False)
    
    # Set style
    sns.set_theme(style="white")
    plt.figure(figsize=(15, 6))
    
    # Graph 1: The "Human Habit" Correlation (Mobile vs Study)
    plt.subplot(1, 2, 1)
    sns.regplot(x='Study_Hours', y='Exam_Score', data=df, scatter_kws={'color':'green', 'alpha':0.5}, line_kws={'color':'darkgreen'}, label='Study Influence')
    sns.regplot(x='Mobile_Usage_Hours', y='Exam_Score', data=df, scatter_kws={'color':'red', 'alpha':0.5}, line_kws={'color':'darkred'}, label='Mobile Influence')
    plt.title('150 Students: Study (+) vs Mobile (-) Influence')
    plt.ylabel('Exam Score')
    plt.legend()
    
    # Graph 2: Daily Time Allocation
    plt.subplot(1, 2, 2)
    avg_times = df[['Mobile_Usage_Hours', 'Social_Media_Hours', 'Study_Hours', 'Sleep_Hours']].mean()
    avg_times.plot(kind='barh', color=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title('Average Daily Human Behavior (150 Students)')
    plt.xlabel('Average Hours')
    
    plt.tight_layout()
    plt.savefig('mobile_performance_150_graph.png')
    print("Subset of 150 records saved to 'mobile_performance_150.csv'")
    print("Graph saved as 'mobile_performance_150_graph.png'")

if __name__ == "__main__":
    analyze_mobile_performance_subset()
