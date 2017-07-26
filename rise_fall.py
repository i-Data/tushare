# import the libraries
import tushare as ts
# import pandas as pd
# import numpy as np


# get normal stock code
ind = ts.get_industry_classified()
# is_st = ts.get_st_classified()
# stop = ts.get_terminated()
# pause = ts.get_suspended()

def fall_counts(stock):

    data = ts.get_k_data(stock)

    p_change = []

    for i in range(1, len(data.close)):
        p_change.append((data.close.loc[i] - data.close.loc[i - 1]) / data.close.loc[i - 1])

    r_p_change = []
    for i in reversed(p_change):
        r_p_change.append(i)

    a = 0
    for i in range(len(r_p_change)):
        if r_p_change[i] < 0:
            a += 1
            if a > (2/3) * i and a > 40:
                print(stock)
                break

for i in ind.code:
    fall_counts(i)