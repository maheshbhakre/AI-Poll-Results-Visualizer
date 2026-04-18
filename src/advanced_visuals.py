import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("data/cleaned_poll_data.csv")

sns.set(style="whitegrid")

# -----------------------------
# 1. VOTE SHARE BAR (WITH %)
# -----------------------------
tool_counts = df["Preferred Tool"].value_counts()
total = len(df)
percentages = (tool_counts / total) * 100

plt.figure(figsize=(8,5))
ax = sns.barplot(x=tool_counts.index, y=tool_counts.values)

for i, v in enumerate(tool_counts.values):
    ax.text(i, v + 2, f"{percentages[i]:.1f}%", ha='center')

plt.title("Vote Share by Tool (%)")
plt.ylabel("Votes")
plt.tight_layout()
plt.savefig("images/vote_share_bar.png")
plt.show()

# -----------------------------
# 2. PIE CHART (VOTE SHARE)
# -----------------------------
plt.figure(figsize=(6,6))
plt.pie(tool_counts, labels=tool_counts.index, autopct='%1.1f%%')
plt.title("Vote Share Distribution")
plt.savefig("images/vote_share_pie.png")
plt.show()

# -----------------------------
# 3. AGE GROUP COMPARISON
# -----------------------------
age_tool = pd.crosstab(df["Age Group"], df["Preferred Tool"])

age_tool.plot(kind="bar", figsize=(8,5))
plt.title("Tool Preference by Age Group")
plt.ylabel("Votes")
plt.tight_layout()
plt.savefig("images/age_group_comparison.png")
plt.show()

# -----------------------------
# 4. REGION STACKED CHART
# -----------------------------
region_tool = pd.crosstab(df["Region"], df["Preferred Tool"])

region_tool.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Region-wise Tool Preference")
plt.tight_layout()
plt.savefig("images/region_stacked.png")
plt.show()

# -----------------------------
# 5. SATISFACTION HEATMAP
# -----------------------------
pivot = df.pivot_table(
    values="Satisfaction (1-5)",
    index="Age Group",
    columns="Preferred Tool",
    aggfunc="mean"
)

plt.figure(figsize=(8,5))
sns.heatmap(pivot, annot=True, cmap="coolwarm")
plt.title("Satisfaction Heatmap")
plt.tight_layout()
plt.savefig("images/satisfaction_heatmap.png")
plt.show()

print("✅ Advanced visualizations created in /images/")