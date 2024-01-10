from datetime import datetime, timedelta
import pandas as pd

###############################################

# This file includes code on transforming the M4
# data-set's time-series in digestable format
# for the application

###############################################

# Requires M4-info.csv to run 
info_df = pd.read_csv('../Dataset/M4-info.csv')

def create_datetime_list(starting_date, desired_length):
    new_date = datetime.strptime(starting_date, '%d-%m-%y %H:%M')

    dates_list = [new_date]
    i = 0
    while i < desired_length:
        # Increment the starting_date by the number of years
        new_date = new_date + timedelta(days=365.25)
        # Update the values in the data_df column
        dates_list.append(new_date.strftime('%d-%m-%y %H:%M'))
        
        i+=1

    return dates_list


def create_df_with_datetimes(df, counter):
    
    timeseries_name = df['V1'][counter]

    # print(df['V1'][counter])
    
    desired_row= info_df[info_df['M4id'] == timeseries_name]
    starting_date = info_df.loc[desired_row.index[0],'StartingDate']
    
    # starting_date = info_df[info_df['M4id']==timeseries_name]['StartingDate']
    
    # print(starting_date)

    new_row = df.loc[counter]
    new_row_df = pd.DataFrame(new_row)
    new_row_df.reset_index(inplace=True)
    new_row_df.columns = ['timestamp','target']

    # To reduce the number of rows and eliminate overflow when calculating future values
    new_row_df = new_row_df.dropna()
    new_row_df = new_row_df[1:]

    # To know how many years to go forward
    number_of_rows = len(new_row_df['timestamp'])

    dates_list = create_datetime_list(starting_date=starting_date, desired_length=number_of_rows)

    number_of_dates = len(dates_list)
    # Replace V2,V3,V4 etc. with dates!
    for i in range(number_of_dates):
        new_row_df['timestamp'][i] = dates_list[i]


    # print(f'New dataframe! \n {new_row_df}')

    # Return the newly created dataframe!
    return new_row_df