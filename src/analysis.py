import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_poll_data.csv")

print("📊 Dataset Shape:", df.shape)

# -----------------------------
# 1. TOTAL RESPONSES
# -----------------------------
total_responses = len(df)
print("\n🔹 Total Responses:", total_responses)

# -----------------------------
# 2. VOTE COUNT & PERCENTAGE
# -----------------------------
tool_counts = df["Preferred Tool"].value_counts()
tool_percentage = (tool_counts / total_responses) * 100

result_df = pd.DataFrame({
    "Votes": tool_counts,
    "Percentage": tool_percentage.round(2)
})

print("\n🔹 Vote Share:\n", result_df)

# -----------------------------
# 3. TOP TOOL
# -----------------------------
top_tool = tool_counts.idxmax()
print("\n🏆 Most Preferred Tool:", top_tool)

# -----------------------------
# 4. AVERAGE SATISFACTION
# -----------------------------
avg_satisfaction = df["Satisfaction (1-5)"].mean()
print("\n⭐ Average Satisfaction:", round(avg_satisfaction, 2))

# -----------------------------
# 5. SATISFACTION BY TOOL
# -----------------------------
sat_by_tool = df.groupby("Preferred Tool")["Satisfaction (1-5)"].mean().round(2)
print("\n🔹 Satisfaction by Tool:\n", sat_by_tool)

# -----------------------------
# 6. AGE GROUP ANALYSIS
# -----------------------------
age_analysis = pd.crosstab(df["Age Group"], df["Preferred Tool"], normalize="index") * 100
print("\n🔹 Age Group % Distribution:\n", age_analysis.round(2))

# -----------------------------
# 7. REGION ANALYSIS
# -----------------------------
region_analysis = pd.crosstab(df["Region"], df["Preferred Tool"], normalize="index") * 100
print("\n🔹 Region % Distribution:\n", region_analysis.round(2))

# -----------------------------
# 8. SAVE RESULTS
# -----------------------------
result_df.to_csv("outputs/vote_share.csv")
sat_by_tool.to_csv("outputs/satisfaction_by_tool.csv")

print("\n✅ Analysis completed. Results saved in /outputs/")