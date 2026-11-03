import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
df = pd.read_csv("data/clean_sales.csv", parse_dates=["Order Date", "Ship Date"])

# ---------- Chart 1: Yearly sales and profit ----------
yearly = df.groupby("Year")[["Sales", "Profit"]].sum()
yearly.plot(kind="bar", figsize=(8, 5), color=["#2E86AB", "#F6AE2D"])
plt.title("Yearly Sales and Profit")
plt.xlabel("Year")
plt.ylabel("Amount")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("outputs/1_yearly_sales_profit.png", dpi=150)
plt.close()

# ---------- Chart 2: Monthly sales trend ----------
monthly = df.groupby("YearMonth")["Sales"].sum()
plt.figure(figsize=(12, 5))
plt.plot(monthly.index, monthly.values, marker="o", color="#2E86AB")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(range(0, len(monthly), 6), monthly.index[::6], rotation=45)
plt.tight_layout()
plt.savefig("outputs/2_monthly_sales_trend.png", dpi=150)
plt.close()

# ---------- Chart 3: Profit by sub-category ----------
sub = df.groupby("Sub-Category")["Profit"].sum().sort_values()
colors = ["#D1495B" if v < 0 else "#2E86AB" for v in sub.values]
plt.figure(figsize=(9, 7))
plt.barh(sub.index, sub.values, color=colors)
plt.title("Profit by Sub-Category (red = loss)")
plt.xlabel("Profit")
plt.tight_layout()
plt.savefig("outputs/3_profit_by_subcategory.png", dpi=150)
plt.close()

# ---------- Chart 4: Category margin ----------
cat = df.groupby("Category")[["Sales", "Profit"]].sum()
cat["Margin %"] = cat["Profit"] / cat["Sales"] * 100
plt.figure(figsize=(7, 5))
plt.bar(cat.index, cat["Margin %"], color=["#D1495B", "#2E86AB", "#2E86AB"])
plt.title("Profit Margin by Category")
plt.ylabel("Margin %")
for i, v in enumerate(cat["Margin %"]):
    plt.text(i, v + 0.3, f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig("outputs/4_category_margin.png", dpi=150)
plt.close()

# ---------- Chart 5: Manager performance ----------
mgr = df.groupby("Manager").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
mgr["Margin %"] = mgr["Profit"] / mgr["Sales"] * 100
mgr = mgr.sort_values("Profit", ascending=False)
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
mgr[["Sales", "Profit"]].plot(kind="bar", ax=ax[0], color=["#2E86AB", "#F6AE2D"])
ax[0].set_title("Sales and Profit by Manager")
ax[0].tick_params(axis="x", rotation=20)
ax[1].bar(mgr.index, mgr["Margin %"], color="#2E86AB")
ax[1].set_title("Profit Margin % by Manager")
ax[1].tick_params(axis="x", rotation=20)
for i, v in enumerate(mgr["Margin %"]):
    ax[1].text(i, v + 0.2, f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig("outputs/5_manager_performance.png", dpi=150)
plt.close()

# ---------- Chart 6: Discount impact ----------
bins = [-0.01, 0, 0.2, 0.4, 1]
labels = ["No discount", "1-20%", "21-40%", "Above 40%"]
df["Discount Band"] = pd.cut(df["Discount"], bins=bins, labels=labels)
disc = df.groupby("Discount Band", observed=True)[["Sales", "Profit"]].sum()
disc["Margin %"] = disc["Profit"] / disc["Sales"] * 100
colors = ["#D1495B" if v < 0 else "#2E86AB" for v in disc["Margin %"]]
plt.figure(figsize=(8, 5))
plt.bar(disc.index.astype(str), disc["Margin %"], color=colors)
plt.title("Profit Margin by Discount Level")
plt.ylabel("Margin %")
plt.axhline(0, color="black", linewidth=0.8)
for i, v in enumerate(disc["Margin %"]):
    plt.text(i, v + (2 if v >= 0 else -6), f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig("outputs/6_discount_impact.png", dpi=150)
plt.close()

# ---------- Chart 7: Region sales share ----------
reg = df.groupby("Region")["Sales"].sum()
plt.figure(figsize=(6, 6))
plt.pie(reg.values, labels=reg.index, autopct="%1.1f%%", startangle=90,
        colors=["#2E86AB", "#F6AE2D", "#D1495B", "#7BC950"])
plt.title("Sales Share by Region")
plt.tight_layout()
plt.savefig("outputs/7_region_sales_share.png", dpi=150)
plt.close()

print("Done! 7 charts saved in the outputs folder.")