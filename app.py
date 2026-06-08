import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

DATA_SOURCES = {
    "Nasdaq 100": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTS3I741z_KTjaF5DsDIZcx302WX75asa4G5jZSnNRNO3WF_KYjmZbAphGL91unIJCnzry3hxa1BQoG/pub?gid=1612255616&single=true&output=csv",
    "S&P 500": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTS3I741z_KTjaF5DsDIZcx302WX75asa4G5jZSnNRNO3WF_KYjmZbAphGL91unIJCnzry3hxa1BQoG/pub?gid=1167979138&single=true&output=csv",
    "Euro Stoxx 50": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTS3I741z_KTjaF5DsDIZcx302WX75asa4G5jZSnNRNO3WF_KYjmZbAphGL91unIJCnzry3hxa1BQoG/pub?gid=90279551&single=true&output=csv",
    "FTSE 100": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTS3I741z_KTjaF5DsDIZcx302WX75asa4G5jZSnNRNO3WF_KYjmZbAphGL91unIJCnzry3hxa1BQoG/pub?gid=515049222&single=true&output=csv",
}

st.set_page_config(page_title="Market Chart Generator", layout="wide")
st.title("10 Year Market Chart Generator")

selected = st.selectbox("Select underlying", list(DATA_SOURCES.keys()))

if st.button("Generate 10 Year Chart"):
    df = pd.read_csv(DATA_SOURCES[selected])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna()

    fig, ax = plt.subplots(figsize=(11, 4.3))
    ax.plot(df["Date"], df["Close"], color="#1f2a44", linewidth=2.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#9aa0a6")
    ax.spines["bottom"].set_color("#9aa0a6")
    ax.grid(False)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.0f}"))
    ax.set_ylim(bottom=0)
    ax.margins(x=0)
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)
