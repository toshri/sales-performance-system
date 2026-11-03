import pandas as pd

# 1. Load the sheets we need
file = "data/SuperSales_Cleaned.xlsx"
orders = pd.read_excel(file, sheet_name="Orders")
people = pd.read_excel(file, sheet_name="People")
returns = pd.read_excel(file, sheet_name="Return")

# 2. Add the manager name for each region
df = orders.merge(people, on="Region", how="left")
df = df.rename(columns={"Person": "Manager"})

# 3. Mark which orders were returned
df["Returned"] = df["Order ID"].isin(returns["Order ID"])

# 4. Create useful new columns
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)

# 5. Quick health check
print("Rows, columns:", df.shape)
print("Missing values:", df.isna().sum().sum())
print("Date range:", df["Order Date"].min().date(), "to", df["Order Date"].max().date())
print(df[["Order Date", "Region", "Manager", "Sales", "Profit", "Profit Margin %"]].head())

# 6. Save the prepared data
df.to_csv("data/clean_sales.csv", index=False)
print("Saved data/clean_sales.csv")