# import matplotlib.pyplot as plt
# import numpy as np

# marks = [50,80,30,60,15,50,-5,85,35,75,30,75,15,55,50,90,25,65,20,55,
#          -5,90,35,65,30,85,15,75,35,85,25,65,20,90,35,65,25,90,20,65]

# # Data cleaning
# marks = [m for m in marks if m >= 0]

# # Categories
# low = sum(1 for m in marks if m <= 30)
# avg = sum(1 for m in marks if 31 <= m <= 60)
# high = sum(1 for m in marks if m > 60)

# labels = ["Low (0–30)", "Average (31–60)", "High (61+)"]
# values = [low, avg, high]
# colors = ['#ff6b6b', '#feca57', '#1dd1a1']

# plt.figure(figsize=(8,5))

# bars = plt.bar(labels, values, color=colors, edgecolor='black')

# # value labels on bars
# for bar in bars:
#     height = bar.get_height()
#     plt.text(
#         bar.get_x() + bar.get_width()/2,
#         height + 0.3,
#         str(height),
#         ha='center',
#         fontsize=11,
#         fontweight='bold'
#     )

# plt.title("📊 Marks Distribution (Bar Graph)", fontsize=15)
# plt.xlabel("Performance Categories")
# plt.ylabel("Number of Students")

# plt.grid(axis='y', linestyle='--', alpha=0.5)

# # save image
# plt.savefig("Marks.png", dpi=300, bbox_inches='tight')

# plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# CSV read karo
df = pd.read_csv("student_performance.csv")

# marks column nikal lo
marks = df["Marks"].dropna()

# categories
low = 0
avg = 0
high = 0

for m in marks:
    if m <= 30:
        low += 1
    elif m <= 60:
        avg += 1
    else:
        high += 1

labels = ["Low", "Average", "High"]
values = [low, avg, high]

# graph
plt.bar(labels, values, color=["red", "orange", "green"])

# values show on bars
for i in range(len(values)):
    plt.text(i, values[i] + 0.5, values[i], ha='center')

plt.title("Marks Distribution from CSV")
plt.xlabel("Category")
plt.ylabel("Students")

plt.savefig("Marks.png", dpi=300)
plt.show()