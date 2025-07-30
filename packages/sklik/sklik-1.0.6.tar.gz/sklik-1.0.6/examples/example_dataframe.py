import os

import pandas as pd
from dotenv import load_dotenv

import sklik
from sklik.object import Account

# Initialize the Sklik API with your token
load_dotenv()

token = os.getenv("SKLIK_TOKEN")
sklik.SklikApi.init(token)

account_id = os.getenv("SKLIK_ACCOUNT_ID")
account = Account(int(account_id))

# Configure report parameters
service = "campaigns"  # Other options: "groups", "ads", "keywords"
since = "2025-06-18"
until = "2025-07-15"
fields = ["id", "name", "status", "impressions", "clicks", "totalMoney"]
granularity = "monthly"  # Other options: "weekly", "monthly", "quarterly", "yearly", "total"

# Create the report
report = sklik.create_report(
    account,
    service,
    fields,
    since,
    until,
    granularity
)

# Collect all report items in a list
report_data = []
for item in report:
    report_data.append(item)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(report_data)

# Display basic information about the DataFrame
print(f"DataFrame shape: {df.shape}")
print("\nDataFrame columns:")
print(df.columns.tolist())
print("\nDataFrame head:")
print(df.head())

# Example: Basic data analysis
if not df.empty:
    print("\nBasic statistics:")
    # Convert numeric columns to appropriate types if needed
    numeric_columns = ["impressions", "clicks", "totalMoney"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Example: Calculate total spend
    if "totalMoney" in df.columns:
        print("\nTotal spend by campaign:")
        print(df.groupby("name")["totalMoney"].sum().sort_values(ascending=False))

    # Example: Calculate CTR (Click-Through Rate)
    if "impressions" in df.columns and "clicks" in df.columns:
        df["ctr"] = (df["clicks"] / df["impressions"]) * 100
        print("\nAverage CTR by campaign:")
        print(df.groupby("name")["ctr"].mean().sort_values(ascending=False))

# Example: Save DataFrame to CSV file
# df.to_csv("sklik_report.csv", index=False)
print("\nTo save the DataFrame to a CSV file, uncomment the line: df.to_csv('sklik_report.csv', index=False)")
