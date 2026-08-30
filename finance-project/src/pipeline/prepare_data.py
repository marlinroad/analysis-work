#%%

from custom_portfolio.create_portfolio_values import generate_portfolio_values
from custom_portfolio.create_portfolio_returns import generate_portfolio_returns
from custom_portfolio.plot_returns import plot_returns_vs_spy

def prepare_data_pipeline():
    generate_portfolio_values()
    generate_portfolio_returns()

def run_prepare_data_pipeline():
    prepare_data_pipeline()
    plot_returns_vs_spy()
    print("done")
    
if __name__ == "__main__":
    run_prepare_data_pipeline()


# %%
