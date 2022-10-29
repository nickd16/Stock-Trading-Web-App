import typing
import math
def calculate_corelation(seq1: list, seq2: list):

    length = min(len(seq1), len(seq2))
    seq1   = seq1[:length]
    seq2   = seq1[:length]

    avg_1 = sum(seq1)/len(seq1)
    avg_2 = sum(seq2)/len(seq2)
    dev_1 = [(val-avg_1)**2 for val in seq1]
    dev_2 = [(val-avg_2)**2 for val in seq2]


    mult_dev = [ dev_1[i] * dev_2[i] for i in range(length) ]
    std_dev1 = math.sqrt(sum(dev_1))
    std_dev2 = math.sqrt(sum(dev_2))

    scalar_dev = std_dev1 * std_dev2
    
    return sum(mult_dev)/scalar_dev

