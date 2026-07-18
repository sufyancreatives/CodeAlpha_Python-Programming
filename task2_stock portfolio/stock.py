import streamlit as st
import pandas as pd
import csv
import io

st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Outfit:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0b131a, #0c2423, #07161c);
    min-height: 100vh;
}

h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #00ff87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 2.8rem !important;
    letter-spacing: 2px;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #00ff87;
    font-size: 0.95rem;
    letter-spacing: 1.5px;
    margin-bottom: 2rem;
    font-family: 'Fira Code', monospace;
}

.metric-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 255, 135, 0.2);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.05);
    margin-bottom: 1.5rem;
}

.metric-value {
    font-size: 2.8rem;
    font-weight: 800;
    color: #00ff87;
    text-shadow: 0 0 20px rgba(0, 255, 135, 0.3);
}

.metric-label {
    font-size: 0.85rem;
    color: #9ab4c5;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #00f2fe;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(0, 242, 254, 0.15);
    padding-bottom: 0.5rem;
}

div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 20px !important;
}

div[data-testid="stNumberInput"] input, 
div[data-testid="stSelectbox"] div[role="button"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(0, 242, 254, 0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: #00ff87 !important;
    box-shadow: 0 0 10px rgba(0, 255, 135, 0.3) !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
    color: #0d1b2a !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(90deg, #00f2fe 0%, #00ff87 100%) !important;
    box-shadow: 0 0 15px rgba(0, 255, 135, 0.4) !important;
    transform: translateY(-1px) !important;
}

.table-container {
    background: rgba(255, 255, 255, 0.01);
    border-radius: 12px;
    overflow: hidden;
}

footer {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

STOCK_PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 150.0,
    "AMZN": 175.0,
    "MSFT": 400.0,
    "NVDA": 850.0,
    "META": 480.0,
    "NFLX": 600.0
}

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

st.markdown("<h1>📊 PORTFOLIO TRACKER</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">REAL-TIME INVESTMENT CALCULATOR</p>', unsafe_allow_html=True)

col_inputs, col_prices = st.columns([1.1, 0.9])

with col_inputs:
    st.markdown('<div class="card-title">⚙️ Add / Update Assets</div>', unsafe_allow_html=True)
    with st.form("portfolio_form", clear_on_submit=True):
        stock_selection = st.selectbox("Select Stock Symbol:", list(STOCK_PRICES.keys()))
        quantity_input = st.number_input("Enter Quantity:", min_value=0.0, step=1.0, format="%.2f")
        submit_btn = st.form_submit_button("Update Portfolio")

        if submit_btn:
            if quantity_input == 0:
                if stock_selection in st.session_state.portfolio:
                    del st.session_state.portfolio[stock_selection]
                    st.success(f"Removed {stock_selection} from portfolio.")
                else:
                    st.info("Quantity is 0. Nothing to remove.")
            else:
                st.session_state.portfolio[stock_selection] = quantity_input
                st.success(f"Updated {stock_selection}: {quantity_input:.2f} shares")

with col_prices:
    st.markdown('<div class="card-title">🏷️ Predefined Prices</div>', unsafe_allow_html=True)
    price_df = pd.DataFrame(list(STOCK_PRICES.items()), columns=["Stock Symbol", "Price per Share"])
    price_df["Price per Share"] = price_df["Price per Share"].apply(lambda x: f"${x:,.2f}")
    st.dataframe(price_df, hide_index=True, use_container_width=True)

st.markdown("---")

portfolio_data = []
total_portfolio_value = 0.0

for symbol, qty in st.session_state.portfolio.items():
    price = STOCK_PRICES[symbol]
    val = qty * price
    total_portfolio_value += val
    portfolio_data.append({
        "Stock": symbol,
        "Quantity": qty,
        "Share Price": price,
        "Total Value": val
    })

st.markdown(
    f'<div class="metric-card">'
    f'<div class="metric-label">Total Portfolio Value</div>'
    f'<div class="metric-value">${total_portfolio_value:,.2f}</div>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="card-title">💼 Current Holdings</div>', unsafe_allow_html=True)

if portfolio_data:
    df_portfolio = pd.DataFrame(portfolio_data)
    df_display = df_portfolio.copy()
    df_display["Share Price"] = df_display["Share Price"].apply(lambda x: f"${x:,.2f}")
    df_display["Total Value"] = df_display["Total Value"].apply(lambda x: f"${x:,.2f}")
    df_display["Quantity"] = df_display["Quantity"].apply(lambda x: f"{x:,.2f}")
    
    st.dataframe(df_display, hide_index=True, use_container_width=True)

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["Stock Symbol", "Quantity Owned", "Current Price ($)", "Total Value ($)"])
    for row in portfolio_data:
        writer.writerow([row["Stock"], row["Quantity"], row["Share Price"], row["Total Value"]])
    writer.writerow([])
    writer.writerow(["TOTAL PORTFOLIO VALUE", "", "", total_portfolio_value])
    csv_data = csv_buffer.getvalue()

    txt_buffer = io.StringIO()
    txt_buffer.write("="*50 + "\n")
    txt_buffer.write("               STOCK PORTFOLIO SUMMARY            \n")
    txt_buffer.write("="*50 + "\n")
    txt_buffer.write(f"{'Stock':<10} | {'Quantity':>8} | {'Price':>12} | {'Value':>12}\n")
    txt_buffer.write("-" * 50 + "\n")
    for row in portfolio_data:
        txt_buffer.write(f"{row['Stock']:<10} | {row['Quantity']:>8.2f} | ${row['Share Price']:>11.2f} | ${row['Total Value']:>11.2f}\n")
    txt_buffer.write("-" * 50 + "\n")
    txt_buffer.write(f"{'TOTAL PORTFOLIO VALUE:':<35} ${total_portfolio_value:>11.2f}\n")
    txt_buffer.write("="*50 + "\n")
    txt_data = txt_buffer.getvalue()

    col_csv, col_txt, col_reset = st.columns(3)
    with col_csv:
        st.download_button(
            label="📥 Download CSV Summary",
            data=csv_data,
            file_name="portfolio_summary.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_txt:
        st.download_button(
            label="📥 Download TXT Summary",
            data=txt_data,
            file_name="portfolio_summary.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_reset:
        if st.button("🗑 Reset Portfolio", use_container_width=True):
            st.session_state.portfolio = {}
            st.rerun()
else:
    st.info("Your portfolio is empty. Add a stock above to see tracker metrics!")

st.markdown(
    "<p style='text-align:center; color:#4a5f6e; font-size:0.8rem; margin-top:3rem;'>"
    "Built using Python · Streamlit · Pandas &nbsp;|&nbsp; "
    "Concepts: dictionary · basic arithmetic · file exporting"
    "</p>",
    unsafe_allow_html=True,
)
