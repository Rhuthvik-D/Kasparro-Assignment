import streamlit as st
import pandas as pd
import json
import papermill as pm
import os

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="AI Market Intelligence Dashboard")

# --- App Title ---
st.title("🤖 AI-Powered Market Intelligence Dashboard")
st.markdown("This dashboard provides an interactive view of D2C performance data and AI-generated insights.")

# --- NEW: Notebook Execution Section ---
st.header("🔄 Data Pipeline Control")

# IMPORTANT: Replace 'Your_Notebook_Name.ipynb' with the actual filename of your notebook.
NOTEBOOK_PATH = 'D2C.ipynb' 
OUTPUT_NOTEBOOK_PATH = r'output\SL_executed_report.ipynb'

if st.button("Update Report from Source Data"):
    if not os.path.exists(NOTEBOOK_PATH):
        st.error(f"Error: Notebook '{NOTEBOOK_PATH}' not found. Please make sure the name is correct.")
    else:
        with st.spinner(f"Running analysis from '{NOTEBOOK_PATH}'... This may take a few minutes."):
            try:
                # Use Papermill to execute the notebook
                pm.execute_notebook(
                   NOTEBOOK_PATH,
                   OUTPUT_NOTEBOOK_PATH
                )
                st.success("Data pipeline executed successfully! The report has been updated.")
                st.info("The app is reloading to display the new data...")
                
                # Clear the cache and rerun the app to load the new files
                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.error(f"An error occurred during notebook execution:")
                st.exception(e)

st.divider()

# --- Cached function to load data ---
@st.cache_data
def load_data():
    """Loads the processed data and insights from files."""
    try:
        df = pd.read_csv('processed_d2c_data.csv')
        with open('insights.json', 'r') as f:
            insights = json.load(f)
        return df, insights
    except FileNotFoundError:
        return None, None

# Load the data
df, insights_data = load_data()

# Display an error if data files are not found, otherwise build the dashboard
if df is None or insights_data is None:
    st.warning("Data files not found. Click the 'Update Report' button above to generate them from the source notebook.")
else:
    # --- Section 1: High-Level KPIs ---
    st.header("📈 Overall Performance Metrics")
    
    total_spend = df['spend'].sum()
    total_revenue = df['revenue'].sum()
    overall_roas = total_revenue / total_spend if total_spend > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ad Spend", f"${total_spend:,.0f}")
    col2.metric("Total Revenue", f"${total_revenue:,.0f}")
    col3.metric("Overall ROAS", f"{overall_roas:.2f}x")

    st.divider()

    # --- Section 2: AI-Generated Insights ---
    st.header("🧠 AI-Generated Insights")
    st.markdown("The following insights were generated automatically, complete with confidence scores.")
    
    if insights_data and 'insights' in insights_data:
        for insight in insights_data['insights']:
            with st.expander(f"{insight['title']} (Confidence: {insight['confidence']['score']:.0%})"):
                st.markdown(f"**Description:** {insight['description']}")
                st.markdown(f"**Recommendation:** {insight['recommendation']}")
                st.markdown(f"_*Justification: {insight['confidence']['justification']}_")
                st.write("Supporting Data:", insight['data'])
    else:
        st.warning("No insights found in 'insights.json'.")

    st.divider()

    # --- Section 3: Deep Dive Explorer ---
    st.header("🔍 Deep Dive Explorer")
    st.markdown("Select a marketing channel to see its specific performance and underlying data.")
    
    all_channels = df['channel'].unique()
    selected_channel = st.selectbox('Select a Channel to Analyze:', options=all_channels)
    
    channel_df = df[df['channel'] == selected_channel]
    
    channel_spend = channel_df['spend'].sum()
    channel_revenue = channel_df['revenue'].sum()
    channel_roas = channel_revenue / channel_spend if channel_spend > 0 else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{selected_channel} Spend", f"${channel_spend:,.0f}")
    c2.metric(f"{selected_channel} Revenue", f"${channel_revenue:,.0f}")
    c3.metric(f"{selected_channel} ROAS", f"{channel_roas:.2f}x")

    st.dataframe(channel_df)