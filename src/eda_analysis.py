import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("data/cleaned_poll_data.csv")

# Set style
sns.set(style="whitegrid")

print("📊 Dataset Shape:", df.shape)

# -----------------------------
# 1. TOOL PREFERENCE COUNT
# -----------------------------
tool_counts = df["Preferred Tool"].value_counts()
print("\n🔹 Tool Preference:\n", tool_counts)

plt.figure(figsize=(8,5))
sns.countplot(x="Preferred Tool", data=df)
plt.title("Most Preferred Tools")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("images/tool_preference.png")
plt.show()

# -----------------------------
# 2. SATISFACTION DISTRIBUTION
# -----------------------------
plt.figure(figsize=(6,4))
sns.histplot(df["Satisfaction (1-5)"], bins=5, kde=True)
plt.title("Satisfaction Distribution")
plt.tight_layout()
plt.savefig("images/satisfaction_distribution.png")
plt.show()

# -----------------------------
# 3. RESPONSES OVER TIME
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"])
daily = df.groupby("Date").size()

plt.figure(figsize=(8,4))
daily.plot(marker='o')
plt.title("Daily Responses Trend")
plt.xlabel("Date")
plt.ylabel("Responses")
plt.grid(True)
plt.tight_layout()
plt.savefig("images/daily_trend.png")
plt.show()

# -----------------------------
# 4. AGE GROUP VS TOOL
# -----------------------------
age_tool = pd.crosstab(df["Age Group"], df["Preferred Tool"])
print("\n🔹 Age vs Tool:\n", age_tool)

age_tool.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Age Group vs Tool Preference")
plt.tight_layout()
plt.savefig("images/age_vs_tool.png")
plt.show()

# -----------------------------
# 5. REGION VS TOOL
# -----------------------------
region_tool = pd.crosstab(df["Region"], df["Preferred Tool"])

region_tool.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Region vs Tool Preference")
plt.tight_layout()
plt.savefig("images/region_vs_tool.png")
plt.show()

# -----------------------------
# 6. SATISFACTION BY TOOL
# -----------------------------
plt.figure(figsize=(8,5))
sns.boxplot(x="Preferred Tool", y="Satisfaction (1-5)", data=df)
plt.title("Satisfaction by Tool")
plt.tight_layout()
plt.savefig("images/satisfaction_by_tool.png")
plt.show()

print("\n✅ EDA Completed. Charts saved in /images/")