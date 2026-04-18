import pandas as pd

# Load data
df = pd.read_csv("data/cleaned_poll_data.csv")

report = []

# -----------------------------
# 1. TOTAL RESPONSES
# -----------------------------
total = len(df)
report.append(f"Total Responses Collected: {total}")

# -----------------------------
# 2. TOP TOOL
# -----------------------------
tool_counts = df["Preferred Tool"].value_counts()
top_tool = tool_counts.idxmax()
top_pct = (tool_counts.max() / total) * 100

report.append(f"Most Preferred Tool: {top_tool} ({top_pct:.2f}%)")

# -----------------------------
# 3. LOWEST TOOL
# -----------------------------
least_tool = tool_counts.idxmin()
least_pct = (tool_counts.min() / total) * 100

report.append(f"Least Preferred Tool: {least_tool} ({least_pct:.2f}%)")

# -----------------------------
# 4. AVG SATISFACTION
# -----------------------------
avg_sat = df["Satisfaction (1-5)"].mean()
report.append(f"Average Satisfaction Score: {avg_sat:.2f} / 5")

# -----------------------------
# 5. BEST TOOL BY SATISFACTION
# -----------------------------
sat_by_tool = df.groupby("Preferred Tool")["Satisfaction (1-5)"].mean()
best_tool = sat_by_tool.idxmax()

report.append(f"Highest Satisfaction Tool: {best_tool}")

# -----------------------------
# 6. AGE GROUP INSIGHT
# -----------------------------
age_pref = pd.crosstab(df["Age Group"], df["Preferred Tool"])
dominant_age_tool = age_pref.idxmax(axis=1)

for age, tool in dominant_age_tool.items():
    report.append(f"Age Group {age} prefers {tool}")

# -----------------------------
# 7. REGION INSIGHT
# -----------------------------
region_pref = pd.crosstab(df["Region"], df["Preferred Tool"])
dominant_region_tool = region_pref.idxmax(axis=1)

for region, tool in dominant_region_tool.items():
    report.append(f"{region} users prefer {tool}")

# -----------------------------
# 8. FINAL RECOMMENDATIONS
# -----------------------------
report.append("\n--- Recommendations ---")

report.append(f"Focus on {top_tool} as the primary offering due to highest demand.")

report.append(f"Improve {least_tool} experience to increase adoption.")

report.append("Target marketing campaigns based on age-group preferences.")

report.append("Leverage high-satisfaction tools for retention strategies.")

# -----------------------------
# 9. SAVE REPORT
# -----------------------------
with open("outputs/insights_report.txt", "w") as f:
    for line in report:
        f.write(line + "\n")

print("✅ Insights report generated at outputs/insights_report.txt")