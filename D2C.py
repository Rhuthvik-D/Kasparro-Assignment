import pandas as pd
import numpy as np
import google.generativeai as genai
import json
import os
from datetime import datetime, timezone

# --- Part 1: Data Cleaning and Feature Engineering ---

class D2CDataPipeline:
    """
    Cleans the raw D2C dataset and engineers key performance metrics.
    Refactored from the D2C.ipynb notebook.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def run(self, output_filepath: str) -> pd.DataFrame:
        """Executes the full data processing pipeline."""
        print("Step 1: Loading data...")
        self.df = pd.read_csv(self.file_path)
        
        print("Step 2: Cleaning and standardizing data...")
        column_mapping = {
            'spend_usd': 'spend', 'revenue_usd': 'revenue', 'seo_category': 'category',
            'avg_position': 'average_position', 'monthly_search_volume': 'search_volume'
        }
        self.df.rename(columns=column_mapping, inplace=True)

        print("Step 3: Engineering features...")
        self.df['ctr'] = self.df.apply(lambda r: r['clicks'] / r['impressions'] if r['impressions'] > 0 else 0, axis=1)
        self.df['conversions'] = self.df['first_purchase']
        self.df['cac'] = self.df.apply(lambda r: r['spend'] / r['conversions'] if r['conversions'] > 0 else 0, axis=1)
        self.df['roas'] = self.df.apply(lambda r: r['revenue'] / r['spend'] if r['spend'] > 0 else 0, axis=1)

        # Save the processed data
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        self.df.to_csv(output_filepath, index=False)
        print(f"Data pipeline complete. Processed data saved to '{output_filepath}'.")
        return self.df

# --- Part 2: Insight and Report Generation ---

class InsightGenerator:
    """
    Generates structured insights with confidence scores and a markdown report.
    Refactored from the D2C.ipynb notebook.
    """
    def __init__(self, processed_df: pd.DataFrame, llm_model):
        self.df = processed_df
        self.model = llm_model
        self.insights = []

    def _normalize_value(self, value, min_val, max_val):
        if max_val == min_val: return 1.0
        return (value - min_val) / (max_val - min_val)

    def analyze(self):
        """Analyzes data to find key insights."""
        print("Analyzing data for key insights...")
        # Top ROAS Channel
        channel_perf = self.df.groupby('channel').agg(avg_roas=('roas', 'mean'), total_spend=('spend', 'sum')).sort_values(by='avg_roas', ascending=False)
        if not channel_perf.empty:
            top_channel = channel_perf.iloc[0]
            confidence = self._normalize_value(top_channel['total_spend'], channel_perf['total_spend'].min(), channel_perf['total_spend'].max())
            self.insights.append({
                "insight_id": "FUN-001", "type": "Funnel", "title": "Top Channel by ROAS",
                "recommendation": f"Consider reallocating budget towards the '{top_channel.name}' channel, which has the highest ROAS ({top_channel['avg_roas']:.2f}x).",
                # CORRECTED STRUCTURE: Confidence is now a dictionary
                "confidence": {
                    "score": round(confidence, 2),
                    "justification": f"Based on a total spend of ${top_channel['total_spend']:,.2f} for this channel."
                }
            })

        # Top SEO Opportunity
        high_potential = self.df[(self.df['search_volume'] >= self.df['search_volume'].median()) & (self.df['average_position'] > 5)].sort_values(by='search_volume', ascending=False)
        if not high_potential.empty:
            top_opp = high_potential.iloc[0]
            confidence = self._normalize_value(top_opp['search_volume'], self.df['search_volume'].min(), self.df['search_volume'].max())
            self.insights.append({
                "insight_id": "SEO-001", "type": "SEO", "title": "High-Volume, Poorly Ranked Category",
                "recommendation": f"Focus SEO efforts on '{top_opp['category']}' to capture significant organic traffic (Monthly Volume: {int(top_opp['search_volume']):,}).",
                # CORRECTED STRUCTURE: Confidence is now a dictionary
                "confidence": {
                    "score": round(confidence, 2),
                    "justification": f"Based on a high search volume of {int(top_opp['search_volume']):,} per month."
                }
            })

    def save_insights_to_json(self, output_filepath: str):
        if not self.insights: return
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        final_output = {
            "report_generated_utc": datetime.now(timezone.utc).isoformat(),
            "insights": self.insights
        }
        with open(output_filepath, 'w') as f: json.dump(final_output, f, indent=4)
        print(f"Saved structured insights to '{output_filepath}'.")

    def generate_and_save_markdown_report(self, output_filepath: str):
        """Generates a Markdown report using an LLM and saves it to a file."""
        print("Generating AI-powered Markdown report...")
        if not self.insights:
            print("No insights available to generate a report.")
            return

        prompt_text = "\n\n".join([json.dumps(insight, indent=2) for insight in self.insights])
        
        prompt = f"""
        You are an expert marketing analyst. Based on the following structured JSON data,
        write a concise executive summary in Markdown format.

        **Data:**
        {prompt_text}

        **Instructions:**
        Generate a report with the following sections:
        - **### Executive Summary**: A brief, high-level paragraph summarizing the key findings.
        - **### 🎯 Top Recommendations**: A bulleted list of the most important, actionable recommendations from the data.
        """
        try:
            response = self.model.generate_content(prompt)
            markdown_report = response.text
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_report)
            print(f"Successfully saved executive report to '{output_filepath}'.")
        except Exception as e:
            print(f"An error occurred while generating the report: {e}")


# --- Part 3: Creative Content Generation ---

class CreativeGenerator:
    """
    Generates AI-powered marketing copy based on data insights.
    Refactored from the D2C.ipynb notebook.
    """
    def __init__(self, processed_df: pd.DataFrame, llm_model):
        self.df = processed_df
        self.model = llm_model

    def generate_ad_headline(self):
        print("\n--- Generating Ad Headlines ---")
        best_roas_category = self.df.loc[self.df['roas'].idxmax()]
        prompt = f"Generate 5 catchy ad headlines for our D2C brand's '{best_roas_category['category']}' category, which has an excellent ROAS of {best_roas_category['roas']:.2f}x."
        response = self.model.generate_content(prompt)
        print("Generated Ad Headlines:\n", response.text)

    def generate_seo_meta_description(self):
        print("\n--- Generating SEO Meta Description ---")
        high_potential = self.df[(self.df['search_volume'] >= self.df['search_volume'].median()) & (self.df['average_position'] > 5)].sort_values(by='search_volume', ascending=False)
        if not high_potential.empty:
            best_seo_opp = high_potential.iloc[0]
            prompt = f"Write a compelling SEO meta description (under 160 characters) for our '{best_seo_opp['category']}' page. It has a huge search volume of {int(best_seo_opp['search_volume']):,} but a poor rank."
            response = self.model.generate_content(prompt)
            print("Generated SEO Meta Description:\n", response.text)

# --- Main Execution Function ---

def run_full_d2c_pipeline(api_key: str):
    """
    Executes the entire D2C analysis pipeline from start to finish.
    Requires a Gemini API key to be passed as an argument.
    """
    # --- Step 1: Run Data Cleaning and Feature Engineering ---
    print("--- Running Data Cleaning and Feature Engineering ---")
    data_pipeline = D2CDataPipeline(file_path='Data/Kasparro_Phase5_D2C_Synthetic_Dataset.csv')
    processed_df = data_pipeline.run(output_filepath='output/processed_d2c_data.csv')

    # --- Step 2: Initialize LLM ---
    print("\n--- Initializing Gemini API ---")
    if not api_key:
        raise ValueError("A valid Gemini API key must be provided.")
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel('gemini-2.5-pro')

    # --- Step 3: Generate Insights and Markdown Report ---
    insight_gen = InsightGenerator(processed_df=processed_df, llm_model=gemini_model)
    insight_gen.analyze()
    insight_gen.save_insights_to_json(output_filepath='output/d2c_insights.json')
    insight_gen.generate_and_save_markdown_report(output_filepath='output/D2C_executive_report.md')

    # --- Step 4: Execute Creative Content Generation ---
    creative_gen = CreativeGenerator(processed_df=processed_df, llm_model=gemini_model)
    creative_gen.generate_ad_headline()
    creative_gen.generate_seo_meta_description()
    
    print("\n--- Full D2C Analysis Pipeline Finished Successfully ---")

# This allows the script to be run directly for testing purposes
if __name__ == '__main__':
    print("--- Running pipeline.py directly for local testing ---")
    try:
        import toml
        secrets_path = os.path.join('.streamlit', 'secrets.toml')
        if not os.path.exists(secrets_path):
            raise FileNotFoundError("Could not find .streamlit/secrets.toml file for local testing.")
        
        secrets = toml.load(secrets_path)
        local_api_key = secrets.get("GEMINI_API_KEY")
        
        if not local_api_key or local_api_key == "your_actual_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY not set in .streamlit/secrets.toml. Please add it.")
            
        run_full_d2c_pipeline(api_key=local_api_key)

    except ImportError:
        print("\nERROR: 'toml' library not found. Please run 'pip install toml' to test this script locally.")
    except Exception as e:
        print(f"\nAn error occurred during local execution: {e}")

