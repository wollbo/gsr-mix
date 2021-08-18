#!/usr/bin/python3
from brownie import GSRConsumer
import pandas as pd


window = 60

def find_window_entries(df, query='get_historical_xau', window=100):
    """Returns df with the latest len(window) values for the selected query"""
    price_feed_contract = GSRConsumer[-1]
    print(df['round_id'].iloc[-1])
    i = 1  # round_ids are not necessarily incremental
    while len(df) < window:
        tup = getattr(price_feed_contract, query)(df['round_id'].iloc[-1]-i)
        if tup[3]:  # time_stamp != 0
            df = df.append(pd.DataFrame([tup], columns=df.columns))
            i = 1
        else:
            i += 1
    return df.reset_index(drop=True)


def main():
    price_feed_contract = GSRConsumer[-1]
    print(f"Reading data from {price_feed_contract.address}")
    cols = ['round_id', 'XA/USD', 'started_at', 'updated_at', 'answered_in']
    xau_df = pd.DataFrame([price_feed_contract.get_latest_xau()], columns=cols)
    xag_df = pd.DataFrame([price_feed_contract.get_latest_xag()], columns=cols)
    
    xau_df = find_window_entries(xau_df, query='get_historical_xau', window=window)
    xau_df.to_csv(f'data/xau_{window}', index=False)

    xag_df = find_window_entries(xag_df, query='get_historical_xag', window=window)
    xag_df.to_csv(f'data/xag_{window}', index=False)


    
