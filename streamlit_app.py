import streamlit as st
import pandas as pd

st.set_page_config(page_title="PG Management Dashboard", layout="wide")
st.title("🏨 PG Management Dashboard")

# Load data
df = pd.read_csv("students_clean.csv")

# Ensure datetime conversion
if "registered_day" in df.columns:
    df["registered_day"] = pd.to_datetime(df["registered_day"])
elif "created_at" in df.columns:
    df["registered_day"] = pd.to_datetime(df["created_at"], errors='coerce')

# Sidebar filters
st.sidebar.header("Filters")
aadhaar_filter = st.sidebar.selectbox("Aadhaar Uploaded", ["All", True, False])

if aadhaar_filter != "All":
    df = df[df["aadhaar_uploaded"] == (aadhaar_filter is True)]

# 🔢 Metric: Total Students
st.metric("👥 Total Students", len(df))

# 📅 Registrations Over Time
if "registered_day" in df.columns:
    st.subheader("📅 Registrations Over Time")
    daily_counts = df.groupby("registered_day").size()
    st.line_chart(daily_counts)

# 🏠 Students per Room
if "room_no" in df.columns:
    st.subheader("🏠 Students per Room")
    room_counts = df["room_no"].value_counts().sort_index()
    st.bar_chart(room_counts)

# 📋 Data Table
st.subheader("📋 Student Records")
st.dataframe(df)
