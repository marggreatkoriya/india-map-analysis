import pandas as pd
import matplotlib.pyplot as plt

# Load data
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scores_path = os.path.join(BASE_DIR, "data", "scores.csv")

df = pd.read_csv(scores_path)

print("========== DATA ANALYSIS ==========")

# Basic stats
print("\nTotal Players:", len(df))
print("Average Score:", df["score"].mean())
print("Highest Score:", df["score"].max())

# Accuracy calculation
df["accuracy"] = df["score"] / df["total_attempts"]

print("\nTop Players:")
print(df.sort_values(by="score", ascending=False).head())

print("\nAccuracy of Players:")
print(df[["name", "accuracy"]])

# GRAPH 1: Score Distribution
plt.figure()
df["score"].plot(kind="hist")
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.show()

# GRAPH 2: Accuracy Comparison
plt.figure()
df.plot(x="name", y="accuracy", kind="bar")
plt.title("Player Accuracy")
plt.ylabel("Accuracy")
plt.show()