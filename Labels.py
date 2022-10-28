import numpy as np

def generateLabels(prices):
    lmin, lmax, size = 0, float('-inf'), len(prices)
    labels = np.zeros((1,size))
    for i in range (1, size):
        print(labels[0])
        if(prices[i]>prices[i-1]):
            lmax = i
        else:
            if lmax != float('-inf'):
                labels[0][lmin], labels[0][lmax] = 1,2
                lmax = float('-inf')
            lmin = i
    if prices[size-1] > prices[size-2] and lmax != float('-inf'):
        labels[0][lmin], labels[0][lmax] = 1,2
    return labels[0]

