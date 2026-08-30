#%%
from pipeline.fetch_data import fetch_all
from pipeline.prepare_data import run_prepare_data_pipeline
from analysis.analysis_pipeline import run_analysis_pipeline

def run_pipeline():
    fetch_all()
    run_prepare_data_pipeline()
    run_analysis_pipeline()
    print("Pipeline execution completed.")

if __name__ == "__main__":
    run_pipeline()
# %%
