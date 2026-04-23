import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("student_performance.csv")

df["average_score"] = (df["math score"] + df["reading score"] + df["writing score"]) / 3

df["Mobile_Hours"] = df["average_score"].apply(
    lambda x: 2 if x > 70 else (5 if x > 50 else 8)
)

plt.scatter(df["Mobile_Hours"], df["average_score"], color="blue")

plt.title("Mobile Usage vs Academic Performance")
plt.xlabel("Mobile Usage (Hours)")
plt.ylabel("Average Score")

plt.grid(True)

plt.savefig("real_mobile_vs_marks.png", dpi=300)
plt.show()