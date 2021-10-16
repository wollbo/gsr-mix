#!/usr/bin/python3
from brownie import GSRConsumer
import pandas as pd


window = 10000

def find_window_entries(df, query='get_historical_xau', window=100):
    """Returns df with the latest len(window) values for the selected query"""
    price_feed_contract = GSRConsumer[-1]
    try:
        df_old = pd.read_csv(f'data/{query.rsplit("_")[-1]}_{window}')
        first_round = int(df_old["round_id"][0])
        print('trying to use old data')
    except:
        print('no old data available')
        first_round = 0
    i = 1  # round_ids are not necessarily incremental
    tup = (df['round_id'].iloc[-1],)
    while len(df) < window and first_round < tup[0]:
        tup = getattr(price_feed_contract, query)(df['round_id'].iloc[-1]-i)
        if tup[3]:  # time_stamp != 0
            df = df.append(pd.DataFrame([tup], columns=df.columns))
            i = 1
        else:
            i += 1
    if tup[0] <= first_round:
        df = df.append(df_old[1:window-len(df)])
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


    
