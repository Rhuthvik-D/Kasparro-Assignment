
# AI-Powered Market Intelligence System

This repository contains the solution for the Applied AI Engineer assignment focused on building an AI-powered market intelligence system. The project ingests, cleans, and analyzes marketing and sales data to generate actionable insights using Large Language Models (LLMs). The final output is an interactive web dashboard built with Streamlit that displays key metrics and AI-generated recommendations.

## Key Features

* **Automated Data Pipelines**: Scripts for cleaning and feature engineering on both the Google Play Store dataset and a synthetic D2C dataset.
* **LLM Integration**: Utilizes the Gemini API to analyze processed data and generate a detailed executive summary with actionable recommendations.
* **Structured & Actionable Outputs**: Generates cleaned datasets (CSV), structured insights with confidence scores (JSON), and automated reports (Markdown).
* **Interactive Dashboard**: A user-friendly Streamlit application to visualize key performance indicators, explore AI-generated insights, and re-run the analysis pipeline on demand.
* **Phase 5 Extension**: Fully implements the D2C funnel and SEO analysis, including the generation of AI-powered creative outputs as part of the final report.

 **[Access the Dashboard](https://kasparro-assignment.streamlit.app/)**

## Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    Create a `requirements.txt` file with the following content and run the installation command.
    ```
    # requirements.txt
    streamlit
    pandas
    numpy
    google-generativeai
    ```
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Data Files**
    * Create a `Data/` directory in the root of the project.
    * Place `googleplaystore.csv` and `Kasparro_Phase5_D2C_Synthetic_Dataset.csv` inside this directory.

5.  **Configure API Key**
    * Create a `.streamlit/` directory in the root of the project.
    * Inside it, create a file named `secrets.toml` and add your Gemini API key:
    ```toml
    # .streamlit/secrets.toml
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

## How to Run

1.  **Clean the Google Play Dataset (Optional)**
    To generate the `cleaned_google_play.csv` file, run the cells in the `Google_play_data_clean.ipynb` notebook.

2.  **Launch the Streamlit Dashboard**
    Run the following command in your terminal from the project's root directory:
    ```bash
    streamlit run app.py
    ```

3.  **Generate a New Report**
    Once the application is running, navigate to the sidebar and click the **"Update Report from Source Data"** button. This will trigger the full D2C pipeline in `D2C.py`, which:
    * Reads and cleans the D2C dataset.
    * Engineers features like ROAS (Return on Ad Spend) and CAC (Customer Acquisition Cost).
    * Generates strategic insights.
    * Calls the Gemini API to write a new executive report.
    * Saves all artifacts to the `output/` directory and refreshes the dashboard.

## Code Modules Overview

* `app.py`: This script contains the Streamlit application. It serves as the main user interface, displaying KPIs, AI-generated insights, and providing controls to run the data pipeline.
* `D2C.py`: The core logic for the D2C analysis (Phase 5). It includes the `D2CDataPipeline` class for data cleaning and feature engineering, and the `InsightGenerator` class, which analyzes the data and uses the Gemini model to produce insights and a markdown report.
* `Google_play_data_clean.ipynb`: A Jupyter Notebook dedicated to the initial cleaning of the Google Play Store dataset. It handles missing values, converts data types, and removes duplicates to prepare the data for analysis.

## Assignment Deliverables Checklist

-   **Clean combined dataset (CSV/JSON)**: Fulfilled by `output/cleaned_google_play.csv` and `output/processed_d2c_data.csv`.
-   **Insights JSON file**: Fulfilled by `output/d2c_insights.json`.
-   **Executive report (Markdown/PDF/HTML)**: Fulfilled by `output/D2C_executive_report.md`.
-   **CLI/Streamlit interface to query insights**: Fulfilled by `app.py`.
-   **Phase 5 Extension: Funnel + SEO insights + creative outputs**: Fulfilled by the D2C pipeline (`D2C.py`) and the final report it generates.

