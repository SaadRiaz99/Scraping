import pandas as pd
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("student_performance.csv")

# 2. Calculate average score for each student
score_cols = ["Math_Score", "Reading_Score", "Writing_Score"]
df["Average_Score"] = df[score_cols].mean(axis=1)

# 3. Create Performance Category and Mobile Usage logic
def classify(score):
    if score > 70: return "High"
    if score > 40: return "Medium"
    return "Low"

df["Performance"] = df["Average_Score"].apply(classify)

# Mobile Usage logic: High performance = Low usage, Low performance = High usage
df["Mobile_Usage"] = df["Average_Score"].apply(lambda x: "Low" if x > 70 else ("Medium" if x > 40 else "High"))

# Chart Settings
plt.style.use('seaborn-v0_8-muted')

# --- 1. Bar Chart: Performance Category Counts ---
plt.figure(figsize=(8, 6))
counts = df["Performance"].value_counts().reindex(["High", "Medium", "Low"])
counts.plot(kind='bar', color=['#2ecc71', '#f1c40f', '#e74c3c'])

# Axis labels (Dataset driven, max 3 words)
plt.title("Student Performance Counts", fontsize=14)
plt.xlabel("Performance Category", fontsize=12) # 2 words
plt.ylabel("Student Count", fontsize=12) # 2 words
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("student_performance_bar.png")
print("Saved student_performance_bar.png")

# --- 2. Line Chart: Average Score Trend ---
plt.figure(figsize=(12, 6))
# Using ID for X-axis to keep it dataset-driven but readable
plt.plot(df["ID"], df["Average_Score"], marker='o', linestyle='-', color='#3498db', markersize=4)

# Axis labels (Dataset driven, max 3 words)
plt.title("Average Score Trend", fontsize=14)
plt.xlabel("Student ID", fontsize=12) # 2 words
plt.ylabel("Average Score", fontsize=12) # 2 words
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("average_score_line.png")
print("Saved average_score_line.png")

# --- 3. Pie Chart: Performance Distribution ---
plt.figure(figsize=(8, 8))
plt.pie(counts, labels=counts.index, autopct='%1.1f%%', 
        colors=['#2ecc71', '#f1c40f', '#e74c3c'], startangle=140)
plt.title("Performance Percentage", fontsize=14) # 2 words
plt.tight_layout()
plt.savefig("performance_pie_distribution.png")
print("Saved performance_pie_distribution.png")

print(f"\nSuccessfully generated charts for {len(df)} students.")
