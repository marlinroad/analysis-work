# financeproject
## Prerequisites and running the pipeline
- FF3 daily factors csv (data\F-F_Research_Data_Factors_daily.csv)
- Momentum daily factors csv (data\F-F_Momentum_Factor_daily.csv)
- Alpaca API keys to config\alpaca_config.json (see sample json in config)

Replace sample in portfolio_transactions.csv to as preferred

Edit data

Run pipeline\run.py

Report:
python .\src\create_report.py

Tests:
python -m pytest tests\

## Sample portfolio report
![Report](output/analysis.png)