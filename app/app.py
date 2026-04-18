import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Poll Results Visualizer", layout="wide")

# -----------------------------
# LOAD DATA (NO ERROR VERSION)
# -----------------------------
@st.cache_data
def load_data():
    path = "data/cleaned_poll_data.csv"

    if not os.path.exists(path):
        st.error("❌ Data file not found. Run data_cleaning.py first.")
        st.stop()

    df = pd.read_csv(path)

    # SAFE TIMESTAMP (handles microseconds / mixed)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # DROP BAD ROWS
    df = df.dropna(subset=['Timestamp'])

    # CREATE DATE
    df['Date'] = df['Timestamp'].dt.date

    return df

df = load_data()

# -----------------------------
# SAVE RESPONSE
# -----------------------------
def save_response(entry):
    global df
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv("data/cleaned_poll_data.csv", index=False)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("🔍 Filters")

tools = st.sidebar.multiselect(
    "Tool",
    df['Preferred Tool'].unique(),
    default=df['Preferred Tool'].unique()
)

regions = st.sidebar.multiselect(
    "Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

filtered_df = df[
    (df['Preferred Tool'].isin(tools)) &
    (df['Region'].isin(regions))
]

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Poll Results Visualizer")

# -----------------------------
# FORM INPUT
# -----------------------------
st.subheader("🗳️ Submit Your Response")

with st.form("poll_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        tool = st.selectbox("Preferred Tool", df['Preferred Tool'].unique())

    with col2:
        age = st.selectbox("Age Group", df['Age Group'].unique())

    with col3:
        region = st.selectbox("Region", df['Region'].unique())

    satisfaction = st.slider("Satisfaction (1-5)", 1, 5)
    feedback = st.text_input("Feedback")

    submitted = st.form_submit_button("Submit")

if submitted:
    new_entry = {
        "Timestamp": pd.Timestamp.now(),
        "Respondent_ID": f"NEW_{len(df)+1}",
        "Age Group": age,
        "Gender": "Unknown",
        "Region": region,
        "Preferred Tool": tool,
        "Satisfaction (1-5)": satisfaction,
        "Feedback": feedback,
        "Date": pd.Timestamp.now().date(),
        "Feedback Length": len(str(feedback))
    }

    save_response(new_entry)
    st.success("✅ Response submitted successfully!")

    try:
        st.rerun()
    except:
        st.info("🔄 Refresh page manually")

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total = len(filtered_df)
avg_sat = round(filtered_df['Satisfaction (1-5)'].mean(), 2) if total > 0 else 0

if total > 0:
    top_tool = filtered_df['Preferred Tool'].value_counts().idxmax()
    top_share = round(
        filtered_df['Preferred Tool'].value_counts(normalize=True).max() * 100, 1
    )
else:
    top_tool = "-"
    top_share = 0

col1.metric("Total Responses", total)
col2.metric("Avg Satisfaction", avg_sat)
col3.metric("Top Tool", top_tool)
col4.metric("Top Share %", f"{top_share}%")

# -----------------------------
# BAR CHART
# -----------------------------
st.subheader("📊 Vote Share")

if total > 0:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered_df, x='Preferred Tool', ax=ax)
    st.pyplot(fig)
else:
    st.warning("No data")

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("🥧 Distribution")

if total > 0:
    tool_counts = filtered_df['Preferred Tool'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(tool_counts, labels=tool_counts.index, autopct='%1.1f%%')
    st.pyplot(fig2)
else:
    st.warning("No data")

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Monthly Trend")

if total > 0:
    trend = filtered_df.groupby(
        pd.to_datetime(filtered_df['Date']).dt.to_period("M")
    ).size()
    st.line_chart(trend)
else:
    st.warning("No data")

# -----------------------------
# HEATMAP
# -----------------------------
st.subheader("🔥 Satisfaction Heatmap")

if total > 0:
    pivot = pd.pivot_table(
        filtered_df,
        values='Satisfaction (1-5)',
        index='Preferred Tool',
        columns='Region'
    )

    fig3, ax3 = plt.subplots()
    sns.heatmap(pivot, annot=True, ax=ax3)
    st.pyplot(fig3)
else:
    st.warning("No data")

# -----------------------------
# DEMOGRAPHICS
# -----------------------------
st.subheader("👥 Demographic Insights")

if total > 0:
    st.write("Age Group vs Tool")
    age_pivot = pd.crosstab(
        filtered_df['Age Group'],
        filtered_df['Preferred Tool']
    )
    st.bar_chart(age_pivot)

    st.write("Region vs Tool")
    region_pivot = pd.crosstab(
        filtered_df['Region'],
        filtered_df['Preferred Tool']
    )
    st.bar_chart(region_pivot)
else:
    st.warning("No data")

# -----------------------------
# NLP
# -----------------------------
st.subheader("🧠 NLP Insights")

text = " ".join(filtered_df['Feedback'].dropna().astype(str))

# Word Cloud
st.write("☁️ Word Cloud")
if text.strip():
    wc = WordCloud(width=800, height=400).generate(text)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wc)
    ax_wc.axis("off")
    st.pyplot(fig_wc)
else:
    st.warning("No text data")

# Sentiment
def get_sentiment(t):
    score = TextBlob(str(t)).sentiment.polarity
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

if total > 0:
    filtered_df['Sentiment'] = filtered_df['Feedback'].apply(get_sentiment)
    st.write("😊 Sentiment Distribution")
    st.bar_chart(filtered_df['Sentiment'].value_counts())

# Keywords
st.write("🔑 Top Keywords")
if text.strip():
    words = text.split()
    freq = pd.Series(words).value_counts().head(10)
    st.dataframe(freq)
else:
    st.warning("No keywords")

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🧠 Key Insights")

if total > 0:
    st.write(f"• Most preferred tool: {top_tool}")
    st.write(f"• Least preferred tool: {filtered_df['Preferred Tool'].value_counts().idxmin()}")
    st.write(f"• Average satisfaction: {avg_sat}")
else:
    st.write("No insights available")