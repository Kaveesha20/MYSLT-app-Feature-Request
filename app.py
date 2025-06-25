
import streamlit as st
import pandas as pd
import plotly.express as px
import os


# Streamlit app configuration
st.set_page_config(page_title="MYSLT Feature Requests", layout="wide")
# password = st.text_input("Enter Password", type="password")
# if password != "Nirmani@25":
#     st.error("Access denied")
#     st.stop()
# Title and description
st.title("MYSLT App Feature Requests")
st.markdown("""
Welcome to the MYSLT feature request dashboard. Explore feature requests from Google Play and App Store reviews, categorized for development prioritization.
""")

# File paths (update these if hosted elsewhere, e.g., Google Drive)
FILES = {
    "Feature Requests": "feature_requests_only.csv",
    "Categorized Requests": "categorized_feature_requests.csv",
    "Summary": "feature_requests_summary.csv"
}

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select View", ["Overview", "Feature Requests", "Categorized Requests", "Summary"])

# Load and display data
def load_csv(file_path):
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            st.error(f"File {file_path} not found.")
            return None
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

# Overview page
if page == "Overview":
    st.header("Overview")
    st.markdown("""
    This dashboard contains feature requests extracted from MYSLT app reviews:
    - **Feature Requests**: All reviews identified as feature requests.
    - **Categorized Requests**: Requests classified into main (e.g., UI/UX) and sub-categories (e.g., dark mode).
    - **Summary**: Counts of requests per category.
    Use the sidebar to navigate and download files.
    """)

# Feature Requests page
elif page == "Feature Requests":
    st.header("Feature Requests")
    df = load_csv(FILES["Feature Requests"])
    if df is not None:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Feature Requests",
            data=csv,
            file_name="feature_requests_only.csv",
            mime="text/csv"
        )

# Categorized Requests page
elif page == "Categorized Requests":
    st.header("Categorized Feature Requests")
    df = load_csv(FILES["Categorized Requests"])
    if df is not None:
        # Filter options
        main_category = st.selectbox("Filter by Main Category", ["All"] + list(df["main_category"].unique()))
        if main_category != "All":
            df = df[df["main_category"] == main_category]
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Categorized Requests",
            data=csv,
            file_name="categorized_feature_requests.csv",
            mime="text/csv"
        )

# Summary page
elif page == "Summary":
    st.header("Feature Request Summary")
    df = load_csv(FILES["Summary"])
    if df is not None:
        st.dataframe(df, use_container_width=True)
        # Bar chart
        fig = px.bar(df, x="main_category", y="count", color="sub_category", title="Feature Requests by Category")
        st.plotly_chart(fig, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Summary",
            data=csv,
            file_name="feature_requests_summary.csv",
            mime="text/csv"
        )