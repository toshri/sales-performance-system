# Sales Performance & Revenue Optimization System

A Python-based system that analyzes sales data to evaluate revenue, profit, sales growth, product performance, and employee (regional manager) productivity. It generates charts and a written report with recommendations to improve sales efficiency and profitability.

## Tools Used
Python, Pandas, NumPy, Matplotlib, Seaborn, OpenPyXL

## Dataset
Superstore sales data (2014-2017): 9,994 order lines, with sheets for orders, regional managers, and returns.

## Project Structure
- `data/` - raw Excel dataset and the prepared `clean_sales.csv`
- `prepare_data.py` - loads the data, merges managers, adds Year/Month/Margin columns
- `analysis.py` - calculates revenue, profit, growth, product and manager performance
- `charts.py` - creates 7 charts
- `report.py` - generates the written report with recommendations
- `outputs/` - charts (.png), result tables (.csv), and `sales_report.md`

## How to Run
1. Install libraries: `python -m pip install pandas numpy matplotlib seaborn openpyxl`
2. Run in this order:
   - `python prepare_data.py`
   - `python analysis.py`
   - `python charts.py`
   - `python report.py`

## Key Findings
- Total sales of about 2.30M with a 12.5% profit margin.
- Sales grew 29.5% in 2016 and 20.4% in 2017.
- Discounts above 20% are about 14% of order lines but cause about 89% of all losses.
- Furniture has only a 2.5% margin; Tables, Bookcases, and Supplies lose money.
- Anna Andreadi (West) has the highest margin (14.9%); Kelly Williams (Central) has the lowest (7.9%) and the highest average discount.

## Recommendations
Cap discounts at 20%, review Central region discount practice, re-price loss-making sub-categories, push high-margin products, share West region best practice, and reduce returns.