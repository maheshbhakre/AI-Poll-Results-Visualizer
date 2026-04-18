import pandas as pd

# Load dataset
df = pd.read_csv("data/poll_data.csv")

print("🔍 Initial Shape:", df.shape)

# -----------------------------
# 1. REMOVE DUPLICATES
# -----------------------------
df = df.drop_duplicates()
print("✅ After removing duplicates:", df.shape)

# -----------------------------
# 2. HANDLE MISSING VALUES
# -----------------------------
print("\n❓ Missing Values:\n", df.isnull().sum())

# Drop rows where critical columns are missing
df = df.dropna(subset=["Preferred Tool", "Satisfaction (1-5)"])

# Fill optional columns if needed
df["Feedback"] = df["Feedback"].fillna("No Feedback")

# -----------------------------
# 3. STANDARDIZE TEXT DATA
# -----------------------------
df["Preferred Tool"] = df["Preferred Tool"].str.strip().str.title()
df["Gender"] = df["Gender"].str.strip().str.title()
df["Region"] = df["Region"].str.strip().str.title()

# -----------------------------
# 4. CONVERT DATA TYPES
# -----------------------------
df["Satisfaction (1-5)"] = pd.to_numeric(df["Satisfaction (1-5)"], errors='coerce')
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')

# -----------------------------
# 5. FEATURE ENGINEERING
# -----------------------------
df["Date"] = df["Timestamp"].dt.date
df["Feedback Length"] = df["Feedback"].astype(str).apply(len)

# -----------------------------
# 6. FINAL CLEAN CHECK
# -----------------------------
print("\n📊 Cleaned Info:")
print(df.info())

print("\n📈 Stats:")
print(df.describe())

# -----------------------------
# 7. SAVE CLEANED DATA
# -----------------------------
df.to_csv("data/cleaned_poll_data.csv", index=False)

print("\n✅ Cleaned dataset saved at data/cleaned_poll_data.csv")