import pandas as pd
import numpy as np
import google.generativeai as genai
import google.api_core.exceptions
import json
import os
from datetime import datetime, timezone

# --- Part 1: Data Cleaning and Feature Engineering ---

class D2CDataPipeline:
    """Cleans the raw D2C dataset and engineers key performance metrics."""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def run(self, output_filepath: str) -> pd.DataFrame:
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
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        self.df.to_csv(output_filepath, index=False)
        print(f"Data pipeline complete. Processed data saved to '{output_filepath}'.")
        return self.df

# --- Part 2: Insight and Report Generation ---

class InsightGenerator:
    """Generates structured insights with confidence scores and a markdown report."""
    def __init__(self, processed_df: pd.DataFrame, llm_model):
        self.df = processed_df
        self.model = llm_model
        self.insights = []

    def _normalize_value(self, value, min_val, max_val):
        if max_val == min_val: return 1.0
        return (value - min_val) / (max_val - min_val)

    def analyze(self):
        print("Analyzing data for key insights...")
        channel_perf = self.df.groupby('channel').agg(avg_roas=('roas', 'mean'), total_spend=('spend', 'sum')).sort_values(by='avg_roas', ascending=False)
        if not channel_perf.empty:
            top_channel = channel_perf.iloc[0]
            confidence = self._normalize_value(top_channel['total_spend'], channel_perf['total_spend'].min(), channel_perf['total_spend'].max())
            self.insights.append({
                "insight_id": "FUN-001", "type": "Funnel", "title": "Top Channel by ROAS",
                "recommendation": f"Consider reallocating budget towards the '{top_channel.name}' channel, which has the highest ROAS ({top_channel['avg_roas']:.2f}x).",
                "confidence": {"score": round(confidence, 2), "justification": f"Based on a total spend of ${top_channel['total_spend']:,.2f} for this channel."}
            })
        high_potential = self.df[(self.df['search_volume'] >= self.df['search_volume'].median()) & (self.df['average_position'] > 5)].sort_values(by='search_volume', ascending=False)
        if not high_potential.empty:
            top_opp = high_potential.iloc[0]
            confidence = self._normalize_value(top_opp['search_volume'], self.df['search_volume'].min(), self.df['search_volume'].max())
            self.insights.append({
                "insight_id": "SEO-001", "type": "SEO", "title": "High-Volume, Poorly Ranked Category",
                "recommendation": f"Focus SEO efforts on '{top_opp['category']}' to capture significant organic traffic (Monthly Volume: {int(top_opp['search_volume']):,}).",
                "confidence": {"score": round(confidence, 2), "justification": f"Based on a high search volume of {int(top_opp['search_volume']):,} per month."}
            })

    def save_insights_to_json(self, output_filepath: str):
        if not self.insights: return
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        final_output = {"report_generated_utc": datetime.now(timezone.utc).isoformat(), "insights": self.insights}
        with open(output_filepath, 'w') as f: json.dump(final_output, f, indent=4)
        print(f"Saved structured insights to '{output_filepath}'.")

    def generate_and_save_markdown_report(self, output_filepath: str):
        print("Generating AI-powered Markdown report...")
        if not self.insights: return
        prompt_text = "\n\n".join([json.dumps(insight, indent=2) for insight in self.insights])
        prompt = f"You are an expert marketing analyst... Data:\n{prompt_text}\n\nInstructions:\nGenerate a report..."
        # --- ENHANCED ERROR HANDLING ---
        try:
            response = self.model.generate_content(prompt)
            markdown_report = response.text
            with open(output_filepath, 'w', encoding='utf-8') as f: f.write(markdown_report)
            print(f"Successfully saved executive report to '{output_filepath}'.")
        except google.api_core.exceptions.PermissionDenied as e:
            print("!!! PERMISSION DENIED ERROR !!!")
            print("This is likely an API key issue. Please check your Gemini API key in Streamlit Secrets.")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred during report generation: {e}")
            raise e

# --- Main Execution Function ---

def run_full_d2c_pipeline(api_key: str):
    print("--- Running Full D2C Analysis Pipeline ---")
    
    # --- ENHANCED ERROR HANDLING ---
    try:
        print("\n--- Initializing Gemini API ---")
        if not api_key: raise ValueError("API key is missing.")
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        print("Gemini API configured successfully.")

        print("\n--- Running Data Cleaning and Feature Engineering ---")
        data_pipeline = D2CDataPipeline(file_path='Data/Kasparro_Phase5_D2C_Synthetic_Dataset.csv')
        processed_df = data_pipeline.run(output_filepath='output/processed_d2c_data.csv')
        
        insight_gen = InsightGenerator(processed_df=processed_df, llm_model=gemini_model)
        insight_gen.analyze()
        insight_gen.save_insights_to_json(output_filepath='output/d2c_insights.json')
        insight_gen.generate_and_save_markdown_report(output_filepath='output/D2C_executive_report.md')
        
        print("\n--- Full D2C Analysis Pipeline Finished Successfully ---")

    except google.api_core.exceptions.PermissionDenied as e:
        print("!!! PERMISSION DENIED ERROR !!!")
        print("This is likely an API key issue. Please double-check your Gemini API key in Streamlit Secrets.")
        # Re-raise the exception so the Streamlit app can catch it
        raise e
    except FileNotFoundError as e:
        print(f"!!! FILE NOT FOUND ERROR: {e} !!!")
        print("Please ensure the 'Data' folder and its CSV file are correctly named and located in your GitHub repository.")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred in the pipeline: {e}")
        raise e

