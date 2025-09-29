import streamlit as st
import pandas as pd
import json
import os
from D2C import run_full_d2c_pipeline  # Import the function

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="AI Market Intelligence Dashboard",
    page_icon="🤖"
)

# --- Custom CSS for a more professional look ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem; padding-bottom: 2rem; padding-left: 5rem; padding-right: 5rem;
    }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF; border: 1px solid #CCCCCC; padding: 20px;
        border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    .st-expander {
        border: 1px solid #CCCCCC; border-radius: 10px; padding: 10px; background-color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)


# --- Sidebar for Controls ---
with st.sidebar:
    st.title("⚙️ Controls")
    st.divider()

    st.header("🔄 Data Pipeline")
    if st.button("Update Report from Source Data"):
        # Check if the secret is configured in Streamlit Cloud/secrets.toml
        if "GEMINI_API_KEY" not in st.secrets or not st.secrets["GEMINI_API_KEY"]:
            st.error("GEMINI_API_KEY not found or not set. Please add it to your Streamlit secrets.")
        else:
            # Get the key from secrets
            api_key_from_secrets = st.secrets['GEMINI_API_KEY']
            with st.spinner("Running full analysis pipeline... This may take a moment."):
                try:
                    # Pass the key to the pipeline function
                    run_full_d2c_pipeline(api_key=api_key_from_secrets)
                    st.success("Pipeline executed successfully! The report is updated.")
                    st.info("Reloading app to display new data...")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error("An error occurred during pipeline execution:")
                    st.exception(e)
    
    st.divider()

    # --- NEW: Report Download Section ---
    st.header("📄 Report Download")
    report_path = 'output/D2C_executive_report.md'
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as file:
            report_content = file.read()
        st.download_button(
            label="Download Executive Report",
            data=report_content,
            file_name="D2C_executive_report.md",
            mime="text/markdown"
        )
    else:
        st.info("Executive report not found. Click 'Update Report' to generate it.")
    
    st.divider()
    st.header("🔍 Deep Dive Explorer")


# --- Main Application Title ---
st.title("🤖 AI-Powered Market Intelligence Dashboard")
st.markdown("An interactive dashboard for D2C performance metrics and AI-generated insights.")


# --- Cached function to load data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('output/processed_d2c_data.csv')
        with open('output/d2c_insights.json', 'r') as f:
            insights = json.load(f)
        return df, insights
    except FileNotFoundError:
        return None, None

# Load the data
df, insights_data = load_data()

if df is None or insights_data is None:
    st.warning("Data files not found in 'output/' folder. Click the 'Update Report' button in the sidebar to generate them.")
else:
    # --- Section 1: High-Level KPIs ---
    st.header("📈 Overall Performance Metrics", divider='rainbow')
    
    total_spend = df['spend'].sum()
    total_revenue = df['revenue'].sum()
    overall_roas = total_revenue / total_spend if total_spend > 0 else 0

    col1, col2, col3 = st.columns(3, gap="large")
    col1.metric("Total Ad Spend", f"${total_spend:,.0f}")
    col2.metric("Total Revenue", f"${total_revenue:,.0f}")
    col3.metric("Overall ROAS", f"{overall_roas:.2f}x")

    # --- Section 2: AI-Generated Insights ---
    st.header("🧠 AI-Generated Insights", divider='rainbow')
    
    if insights_data and 'insights' in insights_data:
        for insight in insights_data['insights']:
            emoji = "🎯" if insight['type'] == 'Funnel' else "🔍"
            confidence_score = insight['confidence']['score']
            with st.expander(f"{emoji} {insight['title']} (Confidence: {confidence_score:.0%})"):
                st.markdown(f"**Recommendation:** {insight['recommendation']}")
                # ADDED LINE: Display the justification as well
                st.markdown(f"_*Justification: {insight['confidence']['justification']}_")
    
    # --- Section 3: Deep Dive Explorer (in Sidebar) ---
    all_channels = df['channel'].unique()
    selected_channel = st.sidebar.selectbox(
        'Select a Channel to Analyze:',
        options=all_channels
    )
    
    st.header(f"📊 Deep Dive: {selected_channel}", divider='rainbow')
    
    channel_df = df[df['channel'] == selected_channel]
    
    c1, c2, c3 = st.columns(3, gap="large")
    c1.metric(f"Spend", f"${channel_df['spend'].sum():,.0f}")
    c2.metric(f"Revenue", f"${channel_df['revenue'].sum():,.0f}")
    c3.metric(f"ROAS", f"{channel_df['revenue'].sum() / channel_df['spend'].sum() if channel_df['spend'].sum() > 0 else 0:.2f}x")

    st.dataframe(channel_df)

