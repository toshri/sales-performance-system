import pandas as pd

df = pd.read_csv("data/clean_sales.csv", parse_dates=["Order Date", "Ship Date"])

# ---------- Calculate the numbers ----------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
margin = total_profit / total_sales * 100
orders = df["Order ID"].nunique()

yearly = df.groupby("Year")[["Sales", "Profit"]].sum()
first_year, last_year = yearly.index.min(), yearly.index.max()
sales_cagr = ((yearly.loc[last_year, "Sales"] / yearly.loc[first_year, "Sales"]) ** (1 / (last_year - first_year)) - 1) * 100
last_growth = yearly["Sales"].pct_change().iloc[-1] * 100

cat = df.groupby("Category")[["Sales", "Profit"]].sum()
cat["Margin"] = cat["Profit"] / cat["Sales"] * 100
worst_cat = cat["Margin"].idxmin()
best_cat = cat["Margin"].idxmax()

sub = df.groupby("Sub-Category")[["Sales", "Profit"]].sum().sort_values("Profit")
loss_subs = sub[sub["Profit"] < 0]
best_sub = sub["Profit"].idxmax()

mgr = df.groupby(["Manager", "Region"]).agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum"), Avg_Discount=("Discount", "mean")
)
mgr["Margin"] = mgr["Profit"] / mgr["Sales"] * 100
mgr = mgr.sort_values("Margin", ascending=False)
top_mgr, top_reg = mgr.index[0]
low_mgr, low_reg = mgr.index[-1]

loss_total = df.loc[df["Profit"] < 0, "Profit"].sum()
heavy = df["Discount"] > 0.2
loss_from_heavy = df.loc[(df["Profit"] < 0) & heavy, "Profit"].sum()
heavy_row_share = heavy.mean() * 100
nodisc_margin = df.loc[df["Discount"] == 0, "Profit"].sum() / df.loc[df["Discount"] == 0, "Sales"].sum() * 100
loss_rows_pct = (df["Profit"] < 0).mean() * 100
returned_pct = df.drop_duplicates("Order ID")["Returned"].mean() * 100

# ---------- Write the report ----------
lines = []
add = lines.append

add("# Sales Performance & Revenue Optimization Report")
add("")
add(f"**Data period:** {df['Order Date'].min().date()} to {df['Order Date'].max().date()}  ")
add(f"**Records analysed:** {len(df):,} order lines across {orders:,} orders")
add("")
add("## 1. Overall Performance")
add(f"- Total sales: {total_sales:,.0f}")
add(f"- Total profit: {total_profit:,.0f}")
add(f"- Overall profit margin: {margin:.1f}%")
add(f"- Orders returned: {returned_pct:.1f}% of all orders")
add("")
add("## 2. Sales Growth")
for y, row in yearly.iterrows():
    add(f"- {y}: sales {row['Sales']:,.0f}, profit {row['Profit']:,.0f}")
add(f"- Average yearly sales growth ({first_year} to {last_year}): {sales_cagr:.1f}%")
add(f"- Sales growth in {last_year}: {last_growth:.1f}%")
add("")
add("## 3. Product Performance")
add(f"- Most profitable category by margin: {best_cat} ({cat.loc[best_cat, 'Margin']:.1f}%)")
add(f"- Weakest category by margin: {worst_cat} ({cat.loc[worst_cat, 'Margin']:.1f}%)")
add(f"- Most profitable sub-category: {best_sub} ({sub.loc[best_sub, 'Profit']:,.0f} profit)")
add("- Loss-making sub-categories:")
for name, row in loss_subs.iterrows():
    add(f"  - {name}: {row['Profit']:,.0f}")
add("")
add("## 4. Employee (Regional Manager) Productivity")
add("The data links each regional manager to one region, so productivity is measured at manager level.")
add("")
add("| Manager | Region | Sales | Profit | Margin | Avg Discount |")
add("|---|---|---|---|---|---|")
for (m, r), row in mgr.iterrows():
    add(f"| {m} | {r} | {row['Sales']:,.0f} | {row['Profit']:,.0f} | {row['Margin']:.1f}% | {row['Avg_Discount'] * 100:.1f}% |")
add("")
add(f"{top_mgr} ({top_reg}) has the highest margin; {low_mgr} ({low_reg}) has the lowest.")
add("")
add("## 5. Performance Gaps")
add(f"- {loss_rows_pct:.1f}% of order lines lose money.")
add(f"- Orders with no discount earn a {nodisc_margin:.1f}% margin.")
add(f"- Discounts above 20% make up only {heavy_row_share:.1f}% of order lines but cause {loss_from_heavy / loss_total * 100:.0f}% of all losses.")
add("")
add("## 6. Recommendations")
add(f"1. **Cap discounts at 20%.** Heavy discounting is the main cause of losses. Require manager approval for any discount above 20%.")
add(f"2. **Fix {low_mgr}'s region ({low_reg}).** Its average discount of {mgr.loc[(low_mgr, low_reg), 'Avg_Discount'] * 100:.1f}% is the highest of the four regions and its margin is the lowest. Review discount practice there first.")
add(f"3. **Review loss-making sub-categories** ({', '.join(loss_subs.index)}). Re-price them, cut discounts, or renegotiate supplier costs.")
add(f"4. **Push high-margin products.** Focus marketing and sales effort on {best_sub} and the sub-categories with margins above 25%.")
add(f"5. **Share best practice.** Use {top_mgr}'s approach in {top_reg} as the model for other regions.")
add(f"6. **Reduce returns.** About {returned_pct:.1f}% of orders are returned; track the reasons to protect profit.")
add("")
add("## 7. Limitations")
add("- The dataset has only four managers, so employee productivity is measured by region.")
add("- Analysis is based on historical data and does not prove cause and effect.")

with open("outputs/sales_report.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\n".join(lines))
print("\nReport saved to outputs/sales_report.md")