import numpy as np
import pandas as pd
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


def derivative(data):
    # numerical approximation to first derivative
    return data.iloc[-1]-data.iloc[-2]


def second_derivative(data): # data[i:i-3]
    # numerical approximation to second derivative
    return (2*data.iloc[-1] - 5*data.iloc[-2] + 4*data.iloc[-3] - data.iloc[-4])/(1**2)


def predict_MA(data, ewm1, ewm2):
    # sell if above first MA and derivative=0, second derivative=-
    # buy if below first MA and derivative=0, second derivative=+
    threshold = 0.001
    labels = [0]*4
    for i in range(4,len(data)):
        d = derivative(ewm1[i-4:i])
        d2 = second_derivative(ewm1[i-4:i])
        if np.abs(d) < threshold and ewm1[i]>ewm2[i]:
            if d2 < 0:
                labels.append(-1)
            else:
                labels.append(0)
        elif np.abs(d) < threshold and ewm1[i]<ewm2[i]:
            if d2 > 0:
                labels.append(1)
            else:
                labels.append(0)
        else:
            labels.append(0)
    return pd.Series(labels, index=np.arange(len(labels)))


def main():
    gsr = pd.read_csv(f'data/gsr_{window}')['GSR']
    #labels = label_with_barrier(gsr, horizon, barrier_weights=weights)

    exp1 = gsr.ewm(span=span1, adjust=False).mean()
    exp2 = gsr.ewm(span=span2, adjust=False).mean()

    labels = predict_MA(gsr, exp1, exp2)

    macd = exp1-exp2
    exp3 = macd.ewm(span=span3, adjust=False).mean()
    derv = pd.Series([derivative(exp1[i-1:i+1]) for i in range(2,len(exp1))], index=np.arange(len(exp1)-2))
    derv2 = pd.Series([second_derivative(exp1[i-4:i+1]) for i in range(4,len(exp1))], index=np.arange(len(exp1)-4))

    label_gsr_1 = np.where(labels==1, gsr, math.nan)
    label_gsr_0 = np.where(labels==-1, gsr, math.nan)

    # plot it
    f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]}, sharex=True)
    a0.plot(gsr)
    a0.plot(exp2)
    a0.plot(exp1)
    a0.plot(label_gsr_1, marker='^', linewidth=0, color='g')
    a0.plot(label_gsr_0, marker='v', linewidth=0, color='r')

    #a1.plot(macd)
    #a1.plot(exp3)
    a1.plot(derv)
    a1.plot(derv2)

    plt.show()
