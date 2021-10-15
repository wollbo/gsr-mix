import pandas as pd
import numpy as np

window = 10000

def main():

    xau = pd.read_csv(f'data/xau_{window}', index_col=0)[::-1]
    xag = pd.read_csv(f'data/xag_{window}', index_col=0)[::-1]

    xau = xau.drop_duplicates(subset=['XA/USD'], keep='first')
    xag = xag.drop_duplicates(subset=['XA/USD'], keep='first') # may drop randomly identical rows, however improbable

    earliest = max(xau['updated_at'].iloc[0], xag['updated_at'].iloc[0])
    latest = min(xau['updated_at'].iloc[-1], xag['updated_at'].iloc[-1]) # keep common intervals

    i_xau = 0
    i_xag = 0

    gsr_df = pd.DataFrame(columns=xau.columns)

    for i in range(earliest, latest):
        if xau['updated_at'].iloc[i_xau] == i or xag['updated_at'].iloc[i_xag] == i:
            idx = np.argmin([xau['updated_at'].iloc[i_xau], xag['updated_at'].iloc[i_xag]])
            gsr_df = gsr_df.append([[xau.iloc[i_xau], xag.iloc[i_xag]][idx]])
            gsr_df['XA/USD'].iloc[-1] = xau['XA/USD'].iloc[i_xau]/xag['XA/USD'].iloc[i_xag]

        if xau['updated_at'].iloc[i_xau] < i:
            i_xau += 1

        if xag['updated_at'].iloc[i_xag] < i:
            i_xag += 1

    gsr_df = gsr_df.reset_index(drop=True).rename(columns={'XA/USD': 'GSR'})
    gsr_df.to_csv(f'data/gsr_{window}', index=False)
