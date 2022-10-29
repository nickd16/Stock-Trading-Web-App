import typing


"""
NOTE:
    0 -> NO-OP | 1 -> BUY | 2 -> SELL
"""


def generateLabels(prices:list) -> list:
    print(prices[:20])
    lmin, lmax, size = 0, float('-inf'), len(prices)
    labels = [0 for i in range(len(prices))]
    for i in range (1, size):
        if(prices[i]>prices[i-1]):
            lmax = i
        else:
            if lmax != float('-inf'):
                labels[lmin], labels[lmax] = 1,2
                lmax = float('-inf')
            lmin = i
    if prices[size-1] > prices[size-2] and lmax != float('-inf'):
        labels[lmin], labels[lmax] = 1,2
    return labels


def generateLabelFile(price_file:str, out_file:str) -> None:
    print(price_file)
    #get all prices
    f = open(price_file, 'r')
    info = f.readlines()[1:]
    info.reverse()
    f.close()

    converted_info = [float(line.split(',')[4]) for line in info]

    #find optimal strategy
    optimal_strategy = generateLabels(converted_info)
    optimal_strategy = " ".join(str(item) for item in optimal_strategy)
    
    #write strategy to file
    f = open(out_file, 'w')
    f.write(optimal_strategy)
    f.close()

    
