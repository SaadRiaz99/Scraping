import pandas as pd
import matplotlib.pyplot as plt

def create_basic_line_graph():
    # Load the 150 records
    df = pd.read_csv("mobile_performance_150.csv")
    
    # Sort by Mobile Usage to make the line graph meaningful
    df_sorted = df.sort_values(by='Mobile_Usage_Hours')
    
    plt.figure(figsize=(10, 6))
    
    # Simple line plot
    plt.plot(df_sorted['Mobile_Usage_Hours'], df_sorted['Exam_Score'], color='red', linewidth=1)
    
    # Labels
    plt.title('Basic Line Graph: Mobile Usage vs Exam Score')
    plt.xlabel('Mobile Usage (Hours)')
    plt.ylabel('Exam Score')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('basic_line_graph.png')
    print("Basic line graph saved as 'basic_line_graph.png'")

if __name__ == "__main__":
    create_basic_line_graph()
