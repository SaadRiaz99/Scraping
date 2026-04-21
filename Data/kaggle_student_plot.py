import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io

def fetch_and_plot_kaggle_student_data():
    print("Fetching Kaggle Student Performance dataset...")
    # This is a highly popular Kaggle dataset mirrored on GitHub
    url = "https://raw.githubusercontent.com/rashida048/Datasets/master/StudentsPerformance.csv"
    
    try:
        response = requests.get(url)
        df = pd.read_csv(io.StringIO(response.text))
        print(f"Data fetched successfully. Records: {len(df)}")
        
        # Save a local copy
        df.to_csv("kaggle_students_data.csv", index=False)
        
        # Set visual style
        sns.set(style="whitegrid")
        plt.figure(figsize=(20, 15))
        
        # 1. Distribution of Math, Reading, and Writing Scores
        plt.subplot(2, 2, 1)
        sns.kdeplot(df['math score'], fill=True, label='Math', color='blue')
        sns.kdeplot(df['reading score'], fill=True, label='Reading', color='green')
        sns.kdeplot(df['writing score'], fill=True, label='Writing', color='orange')
        plt.title('Distribution of Student Scores')
        plt.xlabel('Score')
        plt.legend()

        # 2. Performance by Parental Level of Education
        plt.subplot(2, 2, 2)
        edu_order = [
            "some high school", "high school", "some college", 
            "associate's degree", "压 bachelor's degree", "master's degree"
        ]
        # Clean up labels for display
        df_display = df.copy()
        sns.boxplot(x='math score', y='parental level of education', data=df_display, palette='Set2')
        plt.title('Math Scores by Parental Education Level')

        # 3. Gender-based Performance Comparison
        plt.subplot(2, 2, 3)
        avg_scores = df.groupby('gender')[['math score', 'reading score', 'writing score']].mean().reset_index()
        melted_scores = avg_scores.melt(id_vars='gender', var_name='Subject', value_name='Average Score')
        sns.barplot(x='Subject', y='Average Score', hue='gender', data=melted_scores, palette='pastel')
        plt.title('Average Scores by Gender')
        plt.ylim(0, 100)

        # 4. Impact of Test Preparation Course
        plt.subplot(2, 2, 4)
        sns.violinplot(x='test preparation course', y='reading score', data=df, split=True, palette='coolwarm')
        plt.title('Impact of Test Prep on Reading Scores')

        plt.tight_layout()
        plt.savefig('kaggle_student_analysis.png')
        print("Visualization saved as 'kaggle_student_analysis.png'.")
        
        # Print a short summary
        print("\n--- KAGGLE STUDENT DATA SUMMARY ---")
        print(f"Columns: {list(df.columns)}")
        print(f"Average Math Score: {df['math score'].mean():.2f}")
        print(f"Average Reading Score: {df['reading score'].mean():.2f}")
        print(f"Average Writing Score: {df['writing score'].mean():.2f}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_plot_kaggle_student_data()
