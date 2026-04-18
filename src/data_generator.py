import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)

# Number of responses
n = 200

# Generate timestamps
start_date = datetime(2024, 4, 1)
timestamps = [start_date + timedelta(minutes=i*10) for i in range(n)]

# Respondent IDs
respondent_ids = [f"R{i+1:03d}" for i in range(n)]

# Demographics
age_groups = ['18-24', '25-34', '35-44']
genders = ['Male', 'Female']
regions = ['Urban', 'Rural']

# Tools
tools = ['Python', 'Excel', 'R', 'Power BI']

# Feedback samples
positive_feedback = [
    "Very useful tool", "Loved it", "Great experience", "Super helpful"
]

neutral_feedback = [
    "It was okay", "Average experience", "Nothing special"
]

negative_feedback = [
    "Needs improvement", "Not user friendly", "Poor experience"
]

data = []

for i in range(n):
    age = np.random.choice(age_groups, p=[0.5, 0.3, 0.2])
    
    # Tool preference logic
    if age == '18-24':
        tool = np.random.choice(['Python', 'Power BI'], p=[0.7, 0.3])
    elif age == '25-34':
        tool = np.random.choice(['Python', 'Excel'], p=[0.5, 0.5])
    else:
        tool = np.random.choice(['Excel', 'R'], p=[0.7, 0.3])
    
    # Satisfaction logic
    if tool == 'Python':
        satisfaction = np.random.choice([4, 5], p=[0.4, 0.6])
        feedback = random.choice(positive_feedback)
    elif tool == 'Excel':
        satisfaction = np.random.choice([3, 4], p=[0.6, 0.4])
        feedback = random.choice(neutral_feedback)
    else:
        satisfaction = np.random.choice([2, 3], p=[0.5, 0.5])
        feedback = random.choice(negative_feedback)
    
    row = [
        timestamps[i],
        respondent_ids[i],
        age,
        np.random.choice(genders),
        np.random.choice(regions),
        tool,
        satisfaction,
        feedback
    ]
    
    data.append(row)

columns = [
    "Timestamp", "Respondent_ID", "Age Group",
    "Gender", "Region", "Preferred Tool",
    "Satisfaction (1-5)", "Feedback"
]

df = pd.DataFrame(data, columns=columns)

# Save dataset
df.to_csv("data/poll_data.csv", index=False)

print("✅ Dataset created successfully at data/poll_data.csv")