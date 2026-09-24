"""
app.py — Credit & Debit Card Portfolio Analysis
Streamlit Dashboard
Author: Shaik Parvez
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Card Portfolio Analysis",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #57606a;
        margin-bottom: 1.5rem;
    }
    .kpi-container {
        background: #f7f8fa;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #57606a;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a2e;
        border-left: 4px solid #3b82d4;
        padding-left: 0.6rem;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .insight-card {
        background: #f0f4ff;
        border-left: 4px solid #3b82d4;
        border-radius: 4px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: #1f2328;
    }
    .rec-card {
        background: #f0fff4;
        border-left: 4px solid #22c55e;
        border-radius: 4px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: #1f2328;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data loading & caching
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("cards_data-selected-columns.csv")
    # Drop sensitive columns
    df.drop(columns=["card_number", "cvv"], inplace=True, errors="ignore")
    # Clean credit_limit
    df["credit_limit"] = df["credit_limit"].str.replace(r"[\$,]", "", regex=True).astype(float)
    # Parse dates
    df["acct_open_date"] = pd.to_datetime(df["acct_open_date"], format="%m/%Y", errors="coerce")
    df["expires"] = pd.to_datetime(df["expires"], format="%m/%Y", errors="coerce")
    df["acct_open_year"] = df["acct_open_date"].dt.year
    # Standardize chip column
    df["has_chip"] = df["has_chip"].str.strip().str.upper()
    return df


df_full = load_data()
today = pd.Timestamp.today()

# ─────────────────────────────────────────────
# Sidebar Filters
# ─────────────────────────────────────────────
st.sidebar.markdown("## 🔍 Filters")
st.sidebar.markdown("---")

all_brands = sorted(df_full["card_brand"].unique().tolist())
sel_brands = st.sidebar.multiselect(
    "Card Brand", options=all_brands, default=all_brands
)

all_types = sorted(df_full["card_type"].unique().tolist())
sel_types = st.sidebar.multiselect(
    "Card Type", options=all_types, default=all_types
)

chip_options = {"All": None, "Chip-Enabled Only": "YES", "Non-Chip Only": "NO"}
chip_sel = st.sidebar.radio("Chip Status", options=list(chip_options.keys()), index=0)

min_year = int(df_full["acct_open_year"].min())
max_year = int(df_full["acct_open_year"].max())
year_range = st.sidebar.slider(
    "Account Opening Year", min_value=min_year, max_value=max_year,
    value=(min_year, max_year)
)

# Apply filters
df = df_full[
    df_full["card_brand"].isin(sel_brands) &
    df_full["card_type"].isin(sel_types) &
    df_full["acct_open_year"].between(year_range[0], year_range[1])
].copy()

if chip_options[chip_sel] is not None:
    df = df[df["has_chip"] == chip_options[chip_sel]]

st.sidebar.markdown("---")
st.sidebar.info(f"**{len(df):,}** cards match current filters")

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">💳 Credit & Debit Card Portfolio Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive dashboard — Shaik Parvez | Dataset: cards_data-selected-columns.csv</div>', unsafe_allow_html=True)

if len(df) == 0:
    st.warning("No data matches the selected filters. Please adjust the sidebar.")
    st.stop()

# ─────────────────────────────────────────────
# KPI Calculations
# ─────────────────────────────────────────────
total_cards = len(df)
unique_clients = df["client_id"].nunique()
total_cl = df["credit_limit"].sum()
avg_cl = df["credit_limit"].mean()
median_cl = df["credit_limit"].median()
max_cl = df["credit_limit"].max()
avg_cpp = round(total_cards / unique_clients, 2) if unique_clients > 0 else 0
credit_pct = round(df[df["card_type"] == "Credit"].shape[0] / total_cards * 100, 1)
chip_pct = round(df[df["has_chip"] == "YES"].shape[0] / total_cards * 100, 1)
expired_pct = round(df[df["expires"] < today].shape[0] / total_cards * 100, 1)

# ─────────────────────────────────────────────
# KPI Cards Row 1
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
kpis_row1 = [
    ("Total Cards", f"{total_cards:,}"),
    ("Unique Clients", f"{unique_clients:,}"),
    ("Total Credit Limit", f"${total_cl:,.0f}"),
    ("Average Credit Limit", f"${avg_cl:,.0f}"),
    ("Median Credit Limit", f"${median_cl:,.0f}"),
]
for col, (label, value) in zip([col1, col2, col3, col4, col5], kpis_row1):
    col.markdown(
        f'<div class="kpi-container"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("")

col6, col7, col8, col9, col10 = st.columns(5)
kpis_row2 = [
    ("Max Credit Limit", f"${max_cl:,.0f}"),
    ("Avg Cards / Client", f"{avg_cpp}"),
    ("Credit Card %", f"{credit_pct}%"),
    ("Chip-Enabled %", f"{chip_pct}%"),
    ("Expired Cards %", f"{expired_pct}%"),
]
for col, (label, value) in zip([col6, col7, col8, col9, col10], kpis_row2):
    col.markdown(
        f'<div class="kpi-container"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ─────────────────────────────────────────────
# Charts Row 1: Brand & Type
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Card Distribution</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    brand_cnt = df["card_brand"].value_counts().reset_index()
    brand_cnt.columns = ["Card Brand", "Count"]
    brand_cnt["Percentage"] = (brand_cnt["Count"] / total_cards * 100).round(1)
    fig_brand = px.bar(
        brand_cnt, x="Card Brand", y="Count",
        text=brand_cnt.apply(lambda r: f'{r["Count"]:,} ({r["Percentage"]}%)', axis=1),
        color="Card Brand",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Cards by Card Brand",
    )
    fig_brand.update_traces(textposition="outside")
    fig_brand.update_layout(showlegend=False, title_font_size=14,
                             yaxis_tickformat=",", margin=dict(t=50, b=20))
    st.plotly_chart(fig_brand, use_container_width=True)

with col_b:
    type_cnt = df["card_type"].value_counts().reset_index()
    type_cnt.columns = ["Card Type", "Count"]
    fig_type = px.pie(
        type_cnt, names="Card Type", values="Count",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Cards by Card Type",
        hole=0.35,
    )
    fig_type.update_traces(textinfo="percent+label")
    fig_type.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                            legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig_type, use_container_width=True)

# ─────────────────────────────────────────────
# Charts Row 2: Chip & Credit Limit Distribution
# ─────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    chip_cnt = df["has_chip"].map({"YES": "Chip-Enabled", "NO": "Non-Chip"}).value_counts().reset_index()
    chip_cnt.columns = ["Chip Status", "Count"]
    fig_chip = px.pie(
        chip_cnt, names="Chip Status", values="Count",
        color_discrete_map={"Chip-Enabled": "#3b82d4", "Non-Chip": "#f87171"},
        title="Chip-Enabled vs Non-Chip Cards",
        hole=0.35,
    )
    fig_chip.update_traces(textinfo="percent+label+value")
    fig_chip.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                            legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig_chip, use_container_width=True)

with col_d:
    fig_hist = px.histogram(
        df, x="credit_limit", nbins=50,
        title="Credit Limit Distribution",
        color_discrete_sequence=["#3b82d4"],
        labels={"credit_limit": "Credit Limit ($)"},
    )
    fig_hist.add_vline(x=avg_cl, line_dash="dash", line_color="red",
                       annotation_text=f"Mean: ${avg_cl:,.0f}", annotation_position="top right")
    fig_hist.add_vline(x=median_cl, line_dash="dash", line_color="orange",
                       annotation_text=f"Median: ${median_cl:,.0f}", annotation_position="top left")
    fig_hist.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                            xaxis_tickprefix="$", xaxis_tickformat=",")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# Charts Row 3: Average Credit Limit
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Credit Limit Analysis</div>', unsafe_allow_html=True)

col_e, col_f = st.columns(2)

with col_e:
    avg_brand = df.groupby("card_brand")["credit_limit"].mean().sort_values(ascending=False).reset_index()
    avg_brand.columns = ["Card Brand", "Avg Credit Limit"]
    fig_avg_brand = px.bar(
        avg_brand, x="Card Brand", y="Avg Credit Limit",
        text=avg_brand["Avg Credit Limit"].apply(lambda x: f"${x:,.0f}"),
        color="Card Brand",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Average Credit Limit by Brand",
    )
    fig_avg_brand.update_traces(textposition="outside")
    fig_avg_brand.update_layout(showlegend=False, title_font_size=14,
                                 yaxis_tickprefix="$", yaxis_tickformat=",",
                                 margin=dict(t=50, b=20))
    st.plotly_chart(fig_avg_brand, use_container_width=True)

with col_f:
    avg_type = df.groupby("card_type")["credit_limit"].mean().sort_values(ascending=False).reset_index()
    avg_type.columns = ["Card Type", "Avg Credit Limit"]
    fig_avg_type = px.bar(
        avg_type, x="Card Type", y="Avg Credit Limit",
        text=avg_type["Avg Credit Limit"].apply(lambda x: f"${x:,.0f}"),
        color="Card Type",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Average Credit Limit by Card Type",
    )
    fig_avg_type.update_traces(textposition="outside")
    fig_avg_type.update_layout(showlegend=False, title_font_size=14,
                                yaxis_tickprefix="$", yaxis_tickformat=",",
                                margin=dict(t=50, b=20))
    st.plotly_chart(fig_avg_type, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# Charts Row 4: Trends
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Trends & Client Analysis</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    yr_cnt = df["acct_open_year"].value_counts().sort_index().reset_index()
    yr_cnt.columns = ["Year", "Count"]
    fig_yr = px.bar(
        yr_cnt, x="Year", y="Count",
        color_discrete_sequence=["#3b82d4"],
        title="Cards by Account Opening Year",
        labels={"Count": "Number of Cards"},
    )
    fig_yr.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                          yaxis_tickformat=",", xaxis=dict(tickangle=-45))
    st.plotly_chart(fig_yr, use_container_width=True)

with col_h:
    cpp = df.groupby("client_id")["id"].count().reset_index()
    cpp.columns = ["client_id", "num_cards"]
    cpp_dist = cpp["num_cards"].value_counts().sort_index().reset_index()
    cpp_dist.columns = ["Num Cards", "Num Clients"]
    fig_cpp = px.bar(
        cpp_dist, x="Num Cards", y="Num Clients",
        text="Num Clients",
        color_discrete_sequence=["#7c5cd8"],
        title="Number of Clients by Cards Held",
    )
    fig_cpp.update_traces(textposition="outside")
    fig_cpp.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                           yaxis_tickformat=",")
    st.plotly_chart(fig_cpp, use_container_width=True)

col_i, col_j = st.columns(2)

with col_i:
    pin_yr = df["year_pin_last_changed"].value_counts().sort_index().reset_index()
    pin_yr.columns = ["Year", "Count"]
    fig_pin = px.bar(
        pin_yr, x="Year", y="Count",
        color_discrete_sequence=["#22c55e"],
        title="Cards by PIN Last Changed Year",
        labels={"Count": "Number of Cards"},
    )
    fig_pin.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                           yaxis_tickformat=",", xaxis=dict(tickangle=-45))
    st.plotly_chart(fig_pin, use_container_width=True)

with col_j:
    # Heatmap via plotly
    pivot = df.groupby(["card_brand", "card_type"])["credit_limit"].mean().unstack(fill_value=0)
    fig_heat = px.imshow(
        pivot,
        text_auto=".0f",
        color_continuous_scale="Blues",
        title="Avg Credit Limit — Brand × Card Type",
        labels=dict(color="Avg Credit Limit ($)"),
        aspect="auto",
    )
    fig_heat.update_layout(title_font_size=14, margin=dict(t=50, b=20))
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# Outlier Analysis
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Outlier Analysis — Credit Limit</div>', unsafe_allow_html=True)

Q1 = df["credit_limit"].quantile(0.25)
Q3 = df["credit_limit"].quantile(0.75)
IQR_val = Q3 - Q1
upper_fence = Q3 + 1.5 * IQR_val
outlier_df = df[df["credit_limit"] > upper_fence]

col_k, col_l = st.columns(2)

with col_k:
    fig_box = px.box(
        df, y="credit_limit", color="card_brand",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Credit Limit Box Plot by Brand",
        labels={"credit_limit": "Credit Limit ($)"},
    )
    fig_box.update_layout(title_font_size=14, margin=dict(t=50, b=20),
                           yaxis_tickprefix="$", yaxis_tickformat=",")
    st.plotly_chart(fig_box, use_container_width=True)

with col_l:
    fig_scatter = go.Figure()
    normal_data = df[df["credit_limit"] <= upper_fence]
    fig_scatter.add_trace(go.Scatter(
        x=list(range(len(normal_data))),
        y=normal_data["credit_limit"],
        mode="markers",
        marker=dict(size=3, color="#3b82d4", opacity=0.4),
        name="Normal",
    ))
    fig_scatter.add_trace(go.Scatter(
        x=list(range(len(outlier_df))),
        y=outlier_df["credit_limit"],
        mode="markers",
        marker=dict(size=8, color="red", opacity=0.8),
        name=f"Outliers ({len(outlier_df)})",
    ))
    fig_scatter.update_layout(
        title=f"Credit Limit Outliers Highlighted (Upper Fence: ${upper_fence:,.0f})",
        title_font_size=13,
        yaxis_title="Credit Limit ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",",
        margin=dict(t=50, b=20),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# Data Summary Table
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Data Summary</div>', unsafe_allow_html=True)

col_m, col_n = st.columns(2)
with col_m:
    st.dataframe(
        df[["id", "client_id", "card_brand", "card_type", "has_chip",
            "credit_limit", "acct_open_year", "year_pin_last_changed"]]
        .head(100)
        .reset_index(drop=True),
        use_container_width=True,
        height=300,
    )

with col_n:
    summary = df["credit_limit"].describe().rename({
        "count": "Count", "mean": "Mean", "std": "Std Dev",
        "min": "Min", "25%": "25th Pct", "50%": "Median",
        "75%": "75th Pct", "max": "Max"
    }).to_frame("Credit Limit ($)")
    summary["Credit Limit ($)"] = summary["Credit Limit ($)"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(summary, use_container_width=True, height=300)

st.markdown("---")

# ─────────────────────────────────────────────
# Business Insights
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Key Business Insights</div>', unsafe_allow_html=True)

brand_vc = df_full["card_brand"].value_counts()

insights = [
    f"Mastercard dominates with {brand_vc.get('Mastercard', 0):,} cards ({brand_vc.get('Mastercard', 0)/len(df_full)*100:.1f}%), followed by Visa at {brand_vc.get('Visa', 0):,} ({brand_vc.get('Visa', 0)/len(df_full)*100:.1f}%).",
    f"Debit cards are the most prevalent card type ({df_full[df_full['card_type']=='Debit'].shape[0]/len(df_full)*100:.1f}%), indicating a debit-heavy client base.",
    f"Debit cards carry a significantly higher average credit limit (${df_full[df_full['card_type']=='Debit']['credit_limit'].mean():,.0f}) than Credit cards (${df_full[df_full['card_type']=='Credit']['credit_limit'].mean():,.0f}).",
    f"89.5% of cards ({df_full[df_full['has_chip']=='YES'].shape[0]:,}) are chip-enabled, showing strong EMV compliance.",
    f"79.2% of clients hold multiple cards, averaging {round(len(df_full)/df_full['client_id'].nunique(), 2)} cards per client.",
    f"2020 saw a record {df_full[df_full['acct_open_year']==2020].shape[0]:,} new account openings — the single largest annual cohort in the dataset.",
    f"Credit limit distribution is right-skewed: mean ${df_full['credit_limit'].mean():,.0f} vs median ${df_full['credit_limit'].median():,.0f}, with {len(df_full[df_full['credit_limit'] > df_full['credit_limit'].quantile(0.75) + 1.5*(df_full['credit_limit'].quantile(0.75)-df_full['credit_limit'].quantile(0.25))]):,} outliers.",
    f"Visa (${df_full[df_full['card_brand']=='Visa']['credit_limit'].mean():,.0f}) and Mastercard (${df_full[df_full['card_brand']=='Mastercard']['credit_limit'].mean():,.0f}) have similar average credit limits, both above Amex and Discover.",
    f"PIN changes peaked in 2020 with {df_full[df_full['year_pin_last_changed']==2020].shape[0]:,} updates, correlating with the new-account spike.",
    f"Total portfolio credit limit: ${df_full['credit_limit'].sum():,.0f} across {df_full['client_id'].nunique():,} clients.",
]

for ins in insights:
    st.markdown(f'<div class="insight-card">💡 {ins}</div>', unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# Business Recommendations
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Business Recommendations</div>', unsafe_allow_html=True)

recs = [
    "🔐 Upgrade the 10.5% non-chip cards to EMV-compliant chip cards to reduce fraud exposure.",
    "📊 Leverage the 79.2% multi-card client base for targeted cross-selling of premium products.",
    "🔍 Investigate the 2020 account-opening surge to identify repeatable growth strategies.",
    "⚠️ Conduct regular credit reviews on high-limit outlier accounts (up to $151,223) to manage default risk.",
    "🌟 Launch targeted campaigns to grow Amex (6.5%) and Discover (3.4%) shares in the portfolio.",
    "💳 Promote credit card adoption — only 33.5% of cards are credit cards, leaving significant revenue potential.",
    "🔑 Implement periodic PIN-change reminders for accounts that have not changed PINs since before 2015.",
]

for rec in recs:
    st.markdown(f'<div class="rec-card">{rec}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#57606a; font-size:0.8rem;'>"
    "Credit & Debit Card Portfolio Analysis · Shaik Parvez · Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
