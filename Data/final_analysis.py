import pandas as pd
import matplotlib.pyplot as plt

def create_final_150_line_graph():
    # Load the 150 records
    df = pd.read_csv("mobile_performance_150.csv")
    
    # We will plot by Student Index (1 to 150) to show every single data point
    plt.figure(figsize=(15, 7))
    
    plt.plot(df.index, df['Exam_Score'], color='blue', label='Exam Score', marker='o', markersize=3, linewidth=1)
    plt.plot(df.index, df['Mobile_Usage_Hours'] * 10, color='red', label='Mobile Usage (Scaled x10)', linestyle='--', alpha=0.7)
    
    plt.title('Complete Line Analysis: 150 Students Data')
    plt.xlabel('Student Number (1 to 150)')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('final_150_data_line.png')
    print("Final line graph for all 150 data points saved as 'final_150_data_line.png'")

if __name__ == "__main__":
    create_final_150_line_graph()
