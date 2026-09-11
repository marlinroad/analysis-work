#%%

from custom_portfolio.create_portfolio_values import generate_portfolio_values
from custom_portfolio.create_portfolio_returns import generate_portfolio_returns

def prepare_data_pipeline():
    generate_portfolio_values()
    generate_portfolio_returns()

def run_prepare_data_pipeline():
    prepare_data_pipeline()
    print("prepare data done")
    
if __name__ == "__main__":
    run_prepare_data_pipeline()


# %%
