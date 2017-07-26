# import the libraries
import tushare as ts
import pandas as pd
import numpy as np

# get the data
data = ts.get_k_data('600848')

# make a new column
data['new_col'] = list(zip(data.date, data.close))

# make a new list
turple_data = list(zip(data.date, data.open, data.close, data.high, data.low, data.volume))

#########################################################
length = len(turple_data)

# create empty lists
dates_oc = []
down_list = []
ratio_top_oc_list = []
ratio_middle_oc_list = []
ratio_buttom_oc_list = []

dates_co = []
up_list = []
ratio_top_co_list = []
ratio_middle_co_list = []
ratio_buttom_co_list = []

# populate the lists
for i in range(length):
    if turple_data[i][1] > turple_data[i][2]:
        ratio_top_oc = (turple_data[i][3] - turple_data[i][1]) / (turple_data[i][3] - turple_data[i][4])
        ratio_middle_oc = (turple_data[i][1] - turple_data[i][2]) / (turple_data[i][3] - turple_data[i][4])
        ratio_bottom_oc = (turple_data[i][2] - turple_data[i][4]) / (turple_data[i][3] - turple_data[i][4])

        dates_oc.append(turple_data[i][0])
        down_list.append('down')
        ratio_top_oc_list.append(ratio_top_oc)
        ratio_middle_oc_list.append(ratio_middle_oc)
        ratio_buttom_oc_list.append(ratio_bottom_oc)

        # print(turple_data[i][0],'down',ratio_top_oc, ratio_middle_oc, ratio_bottom_oc)

    elif turple_data[i][1] < turple_data[i][2]:
        ratio_top_co = (turple_data[i][3] - turple_data[i][2]) / (turple_data[i][3] - turple_data[i][4])
        ratio_middle_co = (turple_data[i][2] - turple_data[i][1]) / (turple_data[i][3] - turple_data[i][4])
        ratio_buttom_co = (turple_data[i][1] - turple_data[i][4]) / (turple_data[i][3] - turple_data[i][4])

        dates_co.append(turple_data[i][0])
        up_list.append('up')
        ratio_top_co_list.append(ratio_top_co)
        ratio_middle_co_list.append(ratio_middle_co)
        ratio_buttom_co_list.append(ratio_buttom_co)
        # print(turple_data[i][0],'up',ratio_top_co, ratio_middle_co, ratio_buttom_co)

# make dataframe of days dropping
oc_down = pd.DataFrame(
{'dates': dates_oc,
 'up/down': down_list,
 'ratio_top': ratio_top_oc_list,
 'ratio_middle': ratio_middle_oc_list,
 'ratio_buttom': ratio_buttom_oc_list})

# make dataframe of days raising
co_up = pd.DataFrame(
{'dates': dates_co,
 'up/down': up_list,
 'ratio_top': ratio_top_co_list,
 'ratio_middle': ratio_middle_co_list,
 'ratio_buttom': ratio_buttom_co_list})

# produce final data as result, and get the dates according to the final data
frames = [oc_down, co_up]
result = pd.concat(frames)
result = result.sort_values(by='dates')
result = result.reset_index(drop=True)
three_years_dates = list(result.dates)

# produce star dates with next increase more than a certain number
close = list(data.new_col)
length = len(close)

change = []

for i in range(length - 4):
    ratio = (close[i + 4][1] - close[i][1]) / close[i][1]
    if ratio > 0.10:
        change.append(close[i])

change_dates = []

for i in range(len(change)):
    change_dates.append(change[i][0])

star_dates = pd.DataFrame({'dates': change_dates})

# get the final dates we need for following calculation
final = pd.merge(result, star_dates, left_on = 'dates', right_on = 'dates', how = 'inner')
final_dates = list(final.dates)
final_dates = final_dates[3:]

# get dates index in three years period
dates_index = []

for i in final_dates:
    for j in three_years_dates:
        if i == j:
            dates_index.append(three_years_dates.index(j))
            dates_index

# get 5 days index before star dates
positions = []
for i in dates_index:
    for j in range(5):
        i -= 1
        positions.append(i)
        positions.sort()

# get 5 days list and dataframe
five_dates = []
for i in positions:
    five_dates.append(three_years_dates[i])
df_five_dates = pd.DataFrame({'dates':five_dates})

# get the final data for the 5 days before star dates
final_data = pd.merge(result, df_five_dates, left_on = 'dates', right_on = 'dates', how = 'inner')

# analysing the final data
print(final_data.describe())