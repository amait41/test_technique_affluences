#!/usr/bin/env python3
import pandas as pd
import warnings
warnings.simplefilter("ignore")

def is_open(df_timetables, site_id, time):
    "Check if site is open"
    site = df_timetables[df_timetables.site_id == site_id]
    for index, row in site.iterrows():
        site_opening_datetime = row['opening_datetime']
        site_closing_datetime = row['closing_datetime']
        ids = row["site_id"]
    return (time > site_opening_datetime) and (time < site_closing_datetime)

def main():
    # load data
    fp_data = '/home/amait/Téléchargements/Test_technique_data_engineer_Affluences/data.csv'
    data = pd.read_csv(fp_data, delimiter=',')
    fp_time = '/home/amait/Téléchargements/Test_technique_data_engineer_Affluences/timetables.csv'
    timetables = pd.read_csv(fp_time, delimiter=',')
    
    # copy
    df_data = data.copy()
    df_timetables = timetables.copy()

    # to_datetime
    df_data.last_record_datetime = df_data.last_record_datetime.apply(pd.to_datetime)
    df_timetables.opening_datetime = df_timetables.opening_datetime.apply(pd.to_datetime)
    df_timetables.closing_datetime = df_timetables.closing_datetime.apply(pd.to_datetime)

    # add delta column
    time = pd.to_datetime("today")
    df_data['last_record_datetime2'] = time - df_data.last_record_datetime

    # add alert column
    df_data['alert'] = time - df_data.last_record_datetime
    mask0 = (df_data.last_record_datetime2 < pd.to_timedelta("0 days 02:00:00.00000"))
    mask1 = (df_data.last_record_datetime2 > pd.to_timedelta("0 days 02:00:00.00000")) & \
            (df_data.last_record_datetime2 < pd.to_timedelta("1 days 00:00:00.00000"))
    mask2 = (df_data.last_record_datetime2 > pd.to_timedelta("1 days 00:00:00.00000")) & \
            (df_data.last_record_datetime2 < pd.to_timedelta("2 days 00:00:00.00000"))
    mask3 = (df_data.last_record_datetime2 > pd.to_timedelta("2 days 00:00:00.00000"))
    df_data.loc[:,'alert'].loc[mask0] = 0
    df_data.loc[:,'alert'].loc[mask1] = 1
    df_data.loc[:,'alert'].loc[mask2] = 2
    df_data.loc[:,'alert'].loc[mask3] = 3

    # delete row without alert
    df_data = df_data[df_data.alert > 0]

    res = ''
    for index, row in df_data.iterrows():
        site_id = row['site_id']
        if is_open(df_timetables, site_id, time):
            res += f"Sensor {row['sensor_name']} with identifier {row['sensor_identifier']} triggers an alert at {time} with level {row['alert']} with last data recorded at {row['last_record_datetime']}.\n"
    
    if len(res) == 0:
        print("Pas d'anomalie.")
    else:
        print(res)


if __name__=="__main__":
    main()
