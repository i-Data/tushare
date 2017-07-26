import tushare as ts
import pandas as pd

# get normal stock code
ind = ts.get_industry_classified()
# is_st = ts.get_st_classified()
# stop = ts.get_terminated()
# pause = ts.get_suspended()

# ind.to_csv(ind, sep='\t')


ind.to_csv('ind.txt', sep='\t')