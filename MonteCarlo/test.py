import pandas as pd
import numpy as np

def get_data():
    file_path = "MTFCDataMasterSheet.xlsx"
    df = pd.read_excel(file_path, sheet_name="DailyPrice")
    return df

# Get and print the table
df = get_data()
print(df.to_string())  # Prints all rows and columns without truncation

# Monte Carlo Simulation for each stock
sims = 10000

# AAPL
aapl = df["AAPL"]
aapl_returns = aapl.pct_change()
print(aapl_returns)
