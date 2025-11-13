import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px 
import plotly.graph_objects as go


st.set_page_config(page_title="Stock Trader", layout="wide")
st.markdown("""
    <style>
    div[data-baseweb="input"] > div > div:nth-child(2) {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)


st.write("")
default, portfolio = st.tabs(["Stock", "Portfolio"])

#----- STOCK TAB -----
with default:
    r1c1, r1c2, r1c3 = st.columns([1,2,1])
    with r1c2:
        st.title("📈 Stock Trader")

    st.write("")
    st.write("")
    st.write("")

    r2c1, r2c2, r2c3, r2c4= st.columns([0.5,0.5,2,1])

    r3c1, r3c2 = st.columns([2,3])

    with r2c3:
        stockname = st.text_input("Enter a stock ticker symbol (e.g., AAPL, TSLA):", "").upper()

    # Define period/interval options
    period_options = {
        "1d": ("1d", "1h"),
        "5d": ("5d", "4h"),
        "1mo": ("1mo", "1d"),
        "6mo": ("6mo", "1wk"),
        "YTD": ("ytd", "1wk"),
        "1y": ("1y", "1mo"),
        "5y": ("5y", "3mo"),
        "Max": ("max", "3mo")
    }

    price_or_volume = {
        "Price": "price",
        "Volume": "volume",
        "Both": "both"
    }

    with r2c1:
        selected_pv = st.selectbox("Price/Volume:", list(price_or_volume.keys()), key="price_or_volume")
        pv_choice = price_or_volume[selected_pv]

    with r2c2:
        selected = st.selectbox("Choose period:", list(period_options.keys()))
        period, interval = period_options[selected]

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #4CAF50;  /* Green button */
            color: white;
            height: 70px;
            width: 360px;
            border-radius: 10px;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with r2c4: 
        get_stock_data = st.button("Get Stock Data", key="get_stock_data")  

    if get_stock_data:
        if stockname == "":
            st.warning("⚠️ Please enter a stock ticker symbol.")
        else:
            try:
                stock = yf.Ticker(stockname)
                current_price = stock.history(period=period)['Close'].iloc[-1]
            except Exception as e:
                st.error(f"Error retrieving data for {stockname}: Please enter a valid stock symbol")
                st.stop()
            # Download price data
            with r3c1:
                current_price = yf.download(stockname, period=period, interval=interval).round(2)
                if isinstance(current_price.index, pd.MultiIndex):
                    current_price.index = current_price.index.droplevel(0)

                if isinstance(current_price.columns, pd.MultiIndex):
                    current_price.columns = current_price.columns.droplevel(1)

                new_price = current_price['Close'].iloc[-1]
                old_price = current_price['Close'].iloc[0] 
                
                if new_price > old_price:
                    percentage = ((new_price - old_price) / old_price) * 100
                    st.markdown(
                        f"**Current Price of {stockname}: ${new_price:.2f}  "
                        f"<span style='color:green;'>↑(+{percentage:.2f}%)</span>**",
                        unsafe_allow_html=True
                    )

                elif new_price < old_price:
                    percentage = ((old_price - new_price) / old_price) * 100
                    st.markdown(
                        f"**Current Price of {stockname}: ${new_price:.2f}  "
                        f"<span style='color:red;'>↓(-{percentage:.2f}%)</span>**",
                        unsafe_allow_html=True
                    )
                else:
                    st.write(f"**Current Price of {stockname}: ${new_price:.2f}**")   
    
                st.write(f"Price Data for {stockname}:\n")
                st.write(current_price)

                if period =="1d" and interval == "1h":
                    dates = current_price.index.strftime('%H:%M').to_numpy()
                elif period == "5d" and interval == "4h":
                    dates = current_price.index.strftime('%d %H:%M').to_numpy()
                elif period == "1mo" and interval == "1d":
                    dates = current_price.index.strftime('%d %b').to_numpy()
                elif period == "6mo" and interval == "1wk":
                    dates = current_price.index.strftime('%b %d').to_numpy()
                elif period == "ytd" and interval == "1wk":
                    dates = current_price.index.strftime('%b %d').to_numpy()
                elif period == "1y" and interval == "1mo":
                    dates = current_price.index.strftime('%Y %b').to_numpy()
                elif period == "5y" and interval == "3mo":
                    dates = current_price.index.strftime('%Y-%b').to_numpy()
                else:
                    dates = current_price.index.strftime('%Y-%m-%d').to_numpy()

                close_price = current_price['Close'].to_numpy()

                # ----- VOLUME DATA PROCESSING -----
                volumeaxis = current_price['Volume'].to_numpy()

                if np.max(volumeaxis) > 1e9:
                    volumeaxis = volumeaxis / 1e9
                    volumelabel = "Volume (Billions)"
                elif np.max(volumeaxis) > 1e6:
                    volumeaxis = volumeaxis / 1e6
                    volumelabel = "Volume (Millions)"
                elif np.max(volumeaxis) > 1e3:
                    volumeaxis = volumeaxis / 1e3
                    volumelabel = "Volume (Thousands)"
                else:
                    volumelabel = "Volume"



            with r3c2:
                # BOTH PRICE + VOLUME
                if pv_choice == "both":
                    from plotly.subplots import make_subplots

                    fig = make_subplots(
                        rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        row_heights=[0.6, 0.4]
                    )

                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=close_price,
                        mode="lines",
                        name="Price"
                    ), row=1, col=1)

                    fig.add_trace(go.Bar(
                        x=dates,
                        y=volumeaxis,
                        name="Volume",
                        marker_color="orange"
                    ), row=2, col=1)

                    fig.update_layout(
                        title=f"{stockname} Price + Volume",
                        xaxis_tickangle=90,
                        height=700
                    )

                    st.plotly_chart(fig, use_container_width=True)

                # PRICE ONLY
                elif pv_choice == "price":
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=dates,
                        y=close_price,
                        mode="lines",
                        name="Price"
                    ))
                    fig.update_layout(
                        title=f"{stockname} Stock Price",
                        xaxis_tickangle=90,
                        yaxis_title="Price ($)"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # VOLUME ONLY
                elif pv_choice == "volume":
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=dates,
                        y=volumeaxis,
                        name="Volume",
                        marker_color="orange"
                    ))
                    fig.update_layout(
                        title=f"{stockname} Trading Volume",
                        xaxis_tickangle=90,
                        yaxis_title=volumelabel
                    )
                    st.plotly_chart(fig, use_container_width=True)



    st.header("Stock Options")
    if stockname:
        stock = yf.Ticker(stockname)
        options_dates = stock.options
        if options_dates:
            selected_option_date = st.selectbox("Select an option expiration date:", options_dates)
            if selected_option_date:
                option_chain = stock.option_chain(selected_option_date)
                calls = option_chain.calls
                puts = option_chain.puts

                st.subheader(f"Call Options for {stockname} expiring on {selected_option_date}")
                st.write(calls)

                st.subheader(f"Put Options for {stockname} expiring on {selected_option_date}")
                st.write(puts)
        else:
            st.info(f"No options data available for {stockname}.")  


#----- PORTFOLIO -----

with portfolio:
    r1c1, r1c2, r1c3 = st.columns([1,2,1])
    r2c1, r2c2, r2c3 = st.columns([1,2,1])

    # persistent balance
    if "balance" not in st.session_state:
        st.session_state.balance = 100000.0

    # callback for submit button
    def process_funds():
        try:
            amount = float(st.session_state.funds_input)

            if amount <= 0:
                st.session_state.status = ("warning", "Amount must be > 0.")
                return

            if st.session_state.fund_action == "Add Funds":
                st.session_state.balance += amount
            else:
                st.session_state.balance -= amount

            st.session_state.status = ("success", f"{st.session_state.fund_action} successful!")

            # clear input immediately
            st.session_state.funds_input = ""

        except ValueError:
            st.session_state.status = ("error", "Enter a valid number.")

    with r1c1:
        st.title("Portfolio Management")

    with r1c2:
        st.title(f"Current Balance: ${st.session_state.balance:,.2f}")

    with r2c1:
        st.selectbox("Manage", ["Add Funds", "Withdraw Funds"], key="fund_action")

    with r2c2:
        st.text_input("Funds Amount", key="funds_input")

    with r2c3:
        st.button("Submit", on_click=process_funds)

    if "status" in st.session_state:
        level, msg = st.session_state.status
        getattr(st, level)(msg)







#streamlit run app.py