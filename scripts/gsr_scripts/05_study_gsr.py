import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


window = 10000
horizon = 50
weights = [2, 1]
span1 = 50
span2 = 200
span3 = (span2+span1)/2


def label_with_barrier(data, horizon=10, barrier_weights=[3, 1]):
    labels = pd.Series(0, index=np.arange(len(data)))
    for i in range(horizon, len(data)-horizon):
        barrier = np.std(data[i-horizon:i])
        labels[i] = label_box(
            data[i:i+horizon], 
            upper=barrier_weights[0]*barrier, 
            lower=barrier_weights[1]*barrier
            )
    return labels


def label_box(data, upper, lower):
    data = data.reset_index(drop=True)
    for d in data:
        if d > data[0]+upper:
            return 1
        if d < data[0]-lower:
            return -1
    return -1 # dont execute trade unless we reach profit take level


def main():
    gsr = pd.read_csv(f'data/gsr_{window}')['GSR']
    labels = label_with_barrier(gsr, horizon, barrier_weights=weights)

    exp1 = gsr.ewm(span=span1, adjust=False).mean()
    exp2 = gsr.ewm(span=span2, adjust=False).mean()
    macd = exp1-exp2
    exp3 = macd.ewm(span=span3, adjust=False).mean()

    label_gsr_1 = np.where(labels==1, gsr, math.nan)
    label_gsr_0 = np.where(labels==-1, gsr, math.nan)

    # plot it
    f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]}, sharex=True)
    a0.plot(gsr)
    a0.plot(exp2)
    a0.plot(exp1)
    a0.plot(label_gsr_1, marker='^', linewidth=0, color='g')
    a0.plot(label_gsr_0, marker='v', linewidth=0, color='r')

    a1.plot(macd)
    a1.plot(exp3)

    plt.show()
