#!/usr/bin/env python3
import pandas as pd

# load data
fp_data = '/home/amait/Téléchargements/Test_technique_data_engineer_Affluences/data.csv'
data = pd.read_csv(fp_data, delimiter=',')
fp_time = '/home/amait/Téléchargements/Test_technique_data_engineer_Affluences/timetables.csv'
timetables = pd.read_csv(fp_time, delimiter=',')

df_data = data.copy()
df_time = timetables.copy()
# applay to_datetime
today = pd.to_datetime("today")
df_data.last_record_datetime = df_data.last_record_datetime.apply(pd.to_datetime)

df_data.last_record_datetime = data.last_record_datetime.apply(pd.to_datetime)
df_data['last_record_datetime2'] = today - df_data.last_record_datetime

df_data['alert'] = today - df_data.last_record_datetime
mask0 = df_data.last_record_datetime2 < pd.to_timedelta("0 days 02:00:00.00000")
mask1 = (df_data.last_record_datetime2 >= pd.to_timedelta("0 days 02:00:00.00000")) & (df_data.last_record_datetime2 < pd.to_timedelta("1 days 00:00:00.00000"))
mask2 = (df_data.last_record_datetime2 >= pd.to_timedelta("1 days 00:00:00.00000")) & (df_data.last_record_datetime2 < pd.to_timedelta("2 days 00:00:00.00000"))
mask3 = df_data.last_record_datetime2 > pd.to_timedelta("2 days 00:00:00.00000")
df_data['alert'][mask0] = 0
df_data['alert'][mask1] = 1
df_data['alert'][mask2] = 2
df_data['alert'][mask3] = 3