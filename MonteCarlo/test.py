import pandas as pd
from sklearn.linear_model import LinearRegression

def get_data():
    file_path = "/Users/anshu/Downloads/MTFCDataMasterSheet.xlsx"
    df = pd.read_excel(file_path, sheet_name="Analysis")  # Read the sheet into a DataFrame
    return df

# Get and print the table
df = get_data()
print(df.to_string())  # Prints all rows and columns without truncation

# Fit a linear regression model for cells with NM data
for col in df.columns:
    for row in df[col]:
        if row == "NM":
            # Fit a linear regression model
            model = LinearRegression()
            model.fit(3,8)
            print(model.coef_)
