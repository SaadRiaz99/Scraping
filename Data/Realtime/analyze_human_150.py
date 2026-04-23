import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_human_subset():
    # Load 150 records
    df = pd.read_csv("human_behavior_data.csv").head(150)
    df.to_csv("human_behavior_150.csv", index=False)
    
    plt.figure(figsize=(15, 6))
    
    # Graph 1: Bounce Rates vs Exit Rates (Behavioral pattern)
    plt.subplot(1, 2, 1)
    sns.scatterplot(x='BounceRates', y='ExitRates', hue='Revenue', data=df, palette='coolwarm')
    plt.title('150 Humans: Bounce vs Exit Rates')
    
    # Graph 2: Visitor Type Distribution
    plt.subplot(1, 2, 2)
    df['VisitorType'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightblue', 'pink'])
    plt.title('150 Humans: Visitor Types')
    
    plt.tight_layout()
    plt.savefig('human_150_behavior.png')
    print("Subset of 150 human records saved to 'human_behavior_150.csv'")
    print("Graph saved as 'human_150_behavior.png'")

if __name__ == "__main__":
    analyze_human_subset()
