AI-Powered D2C Market Intelligence Dashboard
Overview
This project is an end-to-end AI-powered market intelligence system designed to analyze Direct-to-Consumer (D2C) performance data. It automates the entire workflow from raw data ingestion to generating actionable business insights, executive reports, and creative marketing content using the Google Gemini API.

The system is presented through a user-friendly, interactive web dashboard built with Streamlit, allowing non-technical users to explore data and leverage AI-driven recommendations. This project specifically fulfills the "Phase 5 Extension" of the Applied AI Engineer assignment, demonstrating the ability to build and adapt a flexible data pipeline for a new vertical.

🚀 Live Demo
[Placeholder for your deployed Streamlit Community Cloud URL]

✨ Key Features
Automated Data Pipeline: A robust Python script (pipeline.py) that handles data loading, cleaning, feature engineering (ROAS, CAC, CTR), and processing in a single, executable run.

AI-Powered Insight Generation: Leverages the Google Gemini API to analyze the processed data and generate high-level insights on marketing funnel performance and SEO opportunities.

Confidence Scoring: Each AI-generated insight is accompanied by a confidence score, calculated based on the statistical significance of the underlying data (e.g., ad spend, search volume), making the recommendations more trustworthy.

Automated Report Generation: Automatically creates a professional, human-readable executive_report.md file summarizing the key findings and recommendations.

AI Creative Content Generation: Uses data-driven insights to prompt the Gemini API for creative marketing copy, including catchy ad headlines and compelling SEO meta descriptions.

Interactive Dashboard: A clean, modern, and user-friendly web interface built with Streamlit that allows users to:

View high-level KPIs at a glance.

Explore AI-generated insights and their justifications.

Trigger the entire data pipeline to refresh the report on-demand.

Download the executive summary.

Perform a "deep dive" by filtering performance data for specific marketing channels.

🛠️ Technology Stack
Backend & Data Processing: Python, Pandas, NumPy

Web Framework: Streamlit

Generative AI: Google Gemini API (google-generativeai)

Configuration: TOML

Deployment: Streamlit Community Cloud

⚙️ Setup and Installation
To run this project locally, please follow these steps:

1. Clone the Repository
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

2. Create a Virtual Environment (Recommended)
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Install all required Python packages from the requirements.txt file.

pip install -r requirements.txt

4. Configure Your API Key
The application uses a .streamlit/secrets.toml file to securely manage the Gemini API key for local development.

Create a folder named .streamlit in the root of the project directory.

Inside this folder, create a file named secrets.toml.

Add your Gemini API key to this file as shown below:

# .streamlit/secrets.toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"

▶️ How to Run
Once the setup is complete, you can launch the Streamlit application from your terminal.

Make sure you are in the root directory of the project.

Run the following command:

streamlit run app.py

Your web browser will automatically open with the dashboard. From there, you can click the "Update Report from Source Data" button in the sidebar to run the full data pipeline and generate your first report.

📁 File Structure
├── .streamlit/
│   └── secrets.toml        
├── Data/
│   └── Kasparro_Phase5_D2C_Synthetic_Dataset.csv 
├── output/                 
│   ├── processed_d2c_data.csv
│   ├── d2c_insights.json
│   └── D2C_executive_report.md
├── app.py                  # The main Streamlit dashboard application
├── D2C.py                  # Core script for data processing and AI analysis
├── requirements.txt        # Python dependencies for the project
└── README.md               
