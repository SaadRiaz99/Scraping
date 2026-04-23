import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("student_performance.csv")

marks = df["Marks"].dropna()

high = sum(marks > 60)
medium = sum((marks > 30) & (marks <= 60))
low = sum(marks <= 30)

labels = ["High", "Medium", "Low"]
counts = [high, medium, low]

plt.pie(counts, labels=labels, autopct='%1.1f%%',
        colors=["green", "yellow", "red"])

plt.title("Student Performance (From CSV)")

plt.savefig("performance_distribution.png", dpi=300)

plt.show()