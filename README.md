# 💳 Credit & Debit Card Portfolio Analysis

> **Author:** Shaik Parvez  
> **Category:** Data Analytics Fresher Portfolio Project  
> **Tools:** Python · Pandas · NumPy · Matplotlib · Seaborn · Plotly · Streamlit

---

## 📋 Project Description

A complete end-to-end data analytics project that explores a credit and debit card portfolio dataset to uncover business insights around card brands, card types, chip adoption, credit limits, client behaviour, and account opening trends.

The project includes exploratory data analysis, KPI calculations, professional visualizations, and an interactive Streamlit dashboard — all built using real values from the dataset.

> ⚠️ **Privacy:** Card numbers and CVV values are excluded from all analysis and the dashboard.

---

## 🎯 Business Objective

Analyze a card portfolio to help a financial institution:
- Understand the distribution of card brands, types, and chip technology
- Monitor credit limit patterns and identify high-risk outliers
- Understand client behavior (multi-card holders, account growth trends)
- Generate actionable business recommendations

---

## 📁 Dataset

| Property | Value |
|---|---|
| Filename | `cards_data-selected-columns.csv` |
| Rows | 6,146 |
| Columns | 12 (10 used after removing sensitive columns) |
| Source | Provided dataset |

### Data Dictionary

| Column | Type | Description |
|---|---|---|
| id | int | Unique card identifier |
| client_id | int | Unique client identifier |
| card_brand | str | Card brand (Visa, Mastercard, Amex, Discover) |
| card_type | str | Card type (Credit, Debit, Debit Prepaid) |
| card_number | int | ⛔ Sensitive — excluded from analysis |
| expires | str | Card expiry date (MM/YYYY) |
| cvv | int | ⛔ Sensitive — excluded from analysis |
| has_chip | str | Whether card has chip (YES/NO) |
| num_cards_issued | int | Number of cards issued to client |
| credit_limit | str | Credit limit with $ prefix |
| acct_open_date | str | Account opening date (MM/YYYY) |
| year_pin_last_changed | int | Year PIN was last changed |

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Pandas** — data manipulation
- **NumPy** — numerical computation
- **Matplotlib / Seaborn** — static visualizations
- **Plotly** — interactive charts
- **Streamlit** — dashboard
- **Jupyter Notebook** — analysis notebook
- **python-docx** — Word report generation

---

## 📂 Project Structure

```
card-portfolio-analysis/
│
├── cards_data-selected-columns.csv   # Dataset
├── ShaikParvez_CardPortfolioAnalysis.ipynb  # Main Jupyter Notebook
├── app.py                            # Streamlit Dashboard
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── ShaikParvez_ProjectReport.docx    # Word project report
│
└── (generated visualizations)
    ├── cards_by_brand.png
    ├── cards_by_type.png
    ├── chip_vs_nonchip.png
    ├── credit_limit_distribution.png
    ├── avg_cl_by_brand.png
    ├── avg_cl_by_type.png
    ├── cards_by_open_year.png
    ├── cards_per_client.png
    ├── pin_change_year.png
    ├── heatmap_cl_brand_type.png
    └── outlier_analysis.png
```

---

## ✨ Features

- ✅ Data cleaning and validation
- ✅ Credit limit parsed from `$` string to float
- ✅ Date columns converted to proper datetime format
- ✅ Sensitive columns (card number, CVV) excluded
- ✅ IQR-based outlier detection
- ✅ 10 KPIs calculated from real data
- ✅ 10 professional visualizations
- ✅ 10 business insights with real numbers
- ✅ 7 business recommendations
- ✅ Interactive Streamlit dashboard with filters
- ✅ No hardcoded analytical results

---

## 🧹 Data Cleaning Summary

| Step | Action |
|---|---|
| Sensitive columns | Dropped `card_number` and `cvv` |
| credit_limit | Stripped `$` and `,`, converted to float |
| acct_open_date | Parsed MM/YYYY → datetime |
| expires | Parsed MM/YYYY → datetime |
| has_chip | Stripped whitespace, uppercased |
| Missing values | None found |
| Duplicates | None found |
| Outliers | Detected via IQR; 235 high-limit cards identified |

---

## 📊 Key KPIs

| KPI | Value |
|---|---|
| Total Cards | 6,146 |
| Unique Clients | 2,000 |
| Total Credit Limit | $88,179,698 |
| Average Credit Limit | $14,347 |
| Median Credit Limit | $12,592.50 |
| Maximum Credit Limit | $151,223 |
| Avg Cards per Client | 3.07 |
| Credit Card % | 33.5% |
| Debit Card % | 57.1% |
| Chip-Enabled % | 89.5% |
| Non-Chip % | 10.5% |

---

## 💡 Key Insights

1. **Mastercard dominates** with 3,209 cards (52.2%), ahead of Visa at 2,326 (37.9%).
2. **Debit cards** are the most common type at 57.1% (3,511 cards).
3. **Debit cards** carry a higher average credit limit ($18,558) than Credit cards ($11,174).
4. **89.5% of cards** are chip-enabled — strong EMV compliance.
5. **79.2% of clients** hold more than one card, averaging 3.07 cards per client.
6. **2020 saw a record** 1,178 new account openings — the largest annual cohort.
7. **Credit limit is right-skewed**: mean $14,347 vs median $12,593, with 235 outlier accounts.
8. **Visa** has the highest average credit limit ($14,737) among card brands.
9. **PIN changes peaked in 2020** (1,208 cards), correlating with account opening surge.
10. **Total portfolio credit limit** is $88,179,698 across 2,000 clients.

---

## 📱 Streamlit Dashboard

The interactive dashboard provides:
- KPI summary cards (10 metrics)
- Sidebar filters (Card Brand, Card Type, Chip Status, Opening Year)
- All charts update dynamically based on filters
- Cards by Brand, Type, Chip status
- Credit Limit Distribution (histogram + KDE)
- Average Credit Limit by Brand & Type
- Account Opening Year trend
- Cards per Client distribution
- PIN Change Year trend
- Heatmap: Avg Credit Limit by Brand × Type
- Outlier analysis (box plot + scatter)
- Filtered data table
- Business insights and recommendations

---

## ⚙️ Installation

### 1. Clone / Download
```bash
git clone https://github.com/<your-username>/card-portfolio-analysis.git
cd card-portfolio-analysis
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Run the Jupyter Notebook
```bash
jupyter notebook ShaikParvez_CardPortfolioAnalysis.ipynb
```
Or open it in VS Code / JupyterLab and run all cells.

### Run the Streamlit Dashboard
```bash
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`

---

## 🔮 Future Improvements

1. Add transaction data to enable spending pattern analysis
2. Build a fraud detection model using card activity features
3. Implement churn prediction for inactive clients
4. Add geographic analysis if location data is available
5. Integrate a real-time data pipeline for live dashboard updates
6. Add credit risk scoring based on limit utilization
7. Expand to include monthly cohort analysis for retention metrics

---

## 📄 License

This project is for educational and portfolio purposes only.
