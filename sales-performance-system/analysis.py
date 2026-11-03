import pandas as pd

df = pd.read_csv("data/clean_sales.csv", parse_dates=["Order Date", "Ship Date"])

# ---------- 1. Overall performance (KPIs) ----------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
print("=== OVERALL ===")
print(f"Total Sales : {total_sales:,.0f}")
print(f"Total Profit: {total_profit:,.0f}")
print(f"Profit Margin: {total_profit / total_sales * 100:.1f}%")
print(f"Total Orders: {df['Order ID'].nunique():,}")

# ---------- 2. Sales growth by year ----------
yearly = df.groupby("Year")[["Sales", "Profit"]].sum().round(0)
yearly["Sales Growth %"] = (yearly["Sales"].pct_change() * 100).round(1)
yearly["Profit Growth %"] = (yearly["Profit"].pct_change() * 100).round(1)
print("\n=== YEARLY GROWTH ===")
print(yearly)

# ---------- 3. Product performance ----------
category = df.groupby("Category")[["Sales", "Profit"]].sum().round(0)
category["Margin %"] = (category["Profit"] / category["Sales"] * 100).round(1)
print("\n=== CATEGORY ===")
print(category)

sub = df.groupby("Sub-Category")[["Sales", "Profit"]].sum().round(0)
sub["Margin %"] = (sub["Profit"] / sub["Sales"] * 100).round(1)
sub = sub.sort_values("Profit", ascending=False)
print("\n=== SUB-CATEGORY (best to worst profit) ===")
print(sub)

top_products = df.groupby("Product Name")["Profit"].sum().sort_values(ascending=False)
print("\n=== TOP 5 PRODUCTS BY PROFIT ===")
print(top_products.head(5).round(0))
print("\n=== BOTTOM 5 PRODUCTS BY PROFIT (losses) ===")
print(top_products.tail(5).round(0))

# ---------- 4. Employee (regional manager) productivity ----------
mgr = df.groupby(["Manager", "Region"]).agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Avg_Discount=("Discount", "mean"),
).round(2)
mgr["Margin %"] = (mgr["Profit"] / mgr["Sales"] * 100).round(1)
mgr["Sales per Order"] = (mgr["Sales"] / mgr["Orders"]).round(0)
print("\n=== MANAGER PERFORMANCE ===")
print(mgr.sort_values("Profit", ascending=False).to_string())

# ---------- 5. Performance gaps: does discount hurt profit? ----------
bins = [-0.01, 0, 0.2, 0.4, 1]
labels = ["No discount", "1-20%", "21-40%", "Above 40%"]
df["Discount Band"] = pd.cut(df["Discount"], bins=bins, labels=labels)
disc = df.groupby("Discount Band", observed=True)[["Sales", "Profit"]].sum().round(0)
disc["Margin %"] = (disc["Profit"] / disc["Sales"] * 100).round(1)
print("\n=== DISCOUNT IMPACT ===")
print(disc)

loss_rows = (df["Profit"] < 0).sum()
print(f"\nLoss-making rows: {loss_rows} ({loss_rows / len(df) * 100:.1f}% of all)")

# ---------- Save tables for the report ----------
yearly.to_csv("outputs/yearly_growth.csv")
category.to_csv("outputs/category_performance.csv")
sub.to_csv("outputs/subcategory_performance.csv")
mgr.to_csv("outputs/manager_performance.csv")
disc.to_csv("outputs/discount_impact.csv")
print("\nSaved tables to the outputs folder.")
