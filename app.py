import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import date

SHEET_MAP = {
    "Nasdaq 100": "Nasdaq100",
    "S&P 500": "S&P500",
    "Euro Stoxx 50": "Eurostoxx50",
    "FTSE 100": "FTSE100",
}

FILE_PATH = "Charts_Data.xlsx"

st.set_page_config(page_title="Market Chart Generator", layout="wide")
st.title("10 Year Market Chart Generator")

selected = st.selectbox("Select underlying", list(SHEET_MAP.keys()))

if st.button("Generate 10 Year Chart"):
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_MAP[selected])
    
    # Handle Excel serial date numbers
    if pd.api.types.is_numeric_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"], unit="D", origin="1899-12-30")
    else:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna()

    fig, ax = plt.subplots(figsize=(11, 4.3))
    ax.plot(df["Date"], df["Close"], color="#1f2a44", linewidth=2.6)

    # Spines — keep only bottom, remove left
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#9aa0a6")

    # Horizontal gridlines only
    ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.8)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)

    # Tick styling
    ax.tick_params(axis="both", which="both", length=0, labelsize=10, labelcolor="#1f2a44")

    # X axis — yearly ticks anchored to data start month, ending at today
    start_month = df["Date"].dt.month.iloc[0]
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[start_month]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.set_xlim(right=pd.Timestamp(date.today()))

    # Y axis — formatted with commas, ceiling rounded up to next 1000
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.0f}"))
    max_val = df["Close"].max()
    y_ceil = (int(max_val / 1000) + 1) * 1000
    ax.set_ylim(bottom=0, top=y_ceil)

    # Small left margin so line doesn't start flush at edge
    ax.margins(x=0.02)

    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)
