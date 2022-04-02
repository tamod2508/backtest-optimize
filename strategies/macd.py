import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df_original: pd.DataFrame, macd_fast: int, macd_slow: int, macd_signal: int, take_profit: float, stop_loss: float):

    df = df_original.copy()
    pnl = 0
    max_pnl = 0
    trade_side = 0
    entry_price = None
    max_drawdown = 0

    df['ema_fast'] = df['close'].ewm(span=macd_fast).mean()  # Get the fast ema
    df['ema_slow'] = df['close'].ewm(span=macd_slow).mean()  # Get the slow ema
    df['line'] = df['ema_fast'] - df['ema_slow']  # the macd line is the difference between the fast with the slow ema
    df['signal'] = df['line'].ewm(span=macd_signal).mean().fillna(0)  # Get the macd signal
    df['ema'] = df['close'].ewm(span=200).mean().fillna(0)  # Create the 200 hundred ema period

    df.drop(["ema_fast", "ema_slow"], axis=1, inplace=True)

    for index, row in df.iterrows():

        # Check if the candle is above or below the 200 ema
        entry_condition = row['close'] > row['ema'] if row['line'] > row['signal'] else row['close'] < row['ema']

        if entry_condition:
            if trade_side == 0:
                entry_price = row['close']

                # Verify if macd line is above or below the signal line, and if they are above or below the zero line of the histogram
                if row['line'] > row['signal'] and row['line'] < 0 and row['signal'] < 0:
                    trade_side = 1
                elif row['line'] < row['signal'] and row['line'] > 0 and row['signal'] > 0:
                    trade_side = -1

        if trade_side == 1:
            if row["close"] >= entry_price * (1 + take_profit / 100) or row["close"] <= entry_price * (
                    1 - stop_loss / 100):
                pnl += (row["close"] / entry_price - 1) * 100
                trade_side = 0
                entry_price = None
        elif trade_side == -1:
            if row["close"] <= entry_price * (1 - take_profit / 100) or row["close"] >= entry_price * (
                    1 + stop_loss / 100):
                pnl += (entry_price / row["close"] - 1) * 100
                trade_side = 0
                entry_price = None

        max_pnl = max(max_pnl, pnl)
        max_drawdown = max(max_drawdown, max_pnl - pnl)

    return pnl, max_drawdown



