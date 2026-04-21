import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def process_150_records():
    input_file = "kaggle_students_data.csv"
    output_file = "kaggle_students_150.csv"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run the previous script first.")
        return

    # Load and truncate to 150 rows
    df = pd.read_csv(input_file)
    df_150 = df.head(150)
    
    # Save the 150-line dataset
    df_150.to_csv(output_file, index=False)
    print(f"Successfully saved 150 records to {output_file}")

    # Generate Graphs for the 150-record subset
    sns.set(style="whitegrid")
    plt.figure(figsize=(16, 10))

    # 1. Math vs Reading Score (Subset)
    plt.subplot(2, 2, 1)
    sns.scatterplot(x='math score', y='reading score', hue='gender', data=df_150)
    plt.title('Math vs Reading Score (First 150 Records)')

    # 2. Gender Count in 150 records
    plt.subplot(2, 2, 2)
    sns.countplot(x='gender', data=df_150, palette='pastel')
    plt.title('Gender Distribution (Subset)')

    # 3. Average Score by Prep Course (Subset)
    plt.subplot(2, 2, 3)
    avg_prep = df_150.groupby('test preparation course')[['math score', 'reading score', 'writing score']].mean().reset_index()
    avg_prep.melt(id_vars='test preparation course').pipe((sns.barplot, "data"), x='variable', y='value', hue='test preparation course')
    plt.title('Avg Scores by Prep Course (150 Records)')
    plt.ylim(0, 100)

    # 4. Score Heatmap (Subset)
    plt.subplot(2, 2, 4)
    corr = df_150[['math score', 'reading score', 'writing score']].corr()
    sns.heatmap(corr, annot=True, cmap='Blues')
    plt.title('Score Correlation (Subset)')

    plt.tight_layout()
    plt.savefig('kaggle_150_analysis.png')
    print("New analysis for 150 records saved as 'kaggle_150_analysis.png'.")

if __name__ == "__main__":
    process_150_records()
