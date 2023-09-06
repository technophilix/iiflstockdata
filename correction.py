import os
from datetime import datetime, timedelta

from Connect import XTSConnect
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

"""Investor client credentials"""
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
clientID = os.getenv("clientID")
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"
file_path_temp = 'OHLC.txt'
"""Make XTSConnect object by passing your 
interactive API appKey, 
secretKey and source"""

xt = XTSConnect(API_KEY, API_SECRET, source)
"""Using the xt object we created call the interactive login Request"""
response = xt.marketdata_login()

if response['type'] == 'success':

    output_excel = input("Enter the excel file name\n")

    exchangesegment = xt.EXCHANGE_NSECM

    master = xt.get_master([exchangesegment])
    rows = master['result'].strip('\n').split('\n')

    data_list = []
    for row in rows:
        row_data = row.split('|')
        data_list.append(row_data)
    df = pd.DataFrame(data_list,
                      columns=['ExchangeSegment', 'ExchangeInstrumentID', 'InstrumentType', 'Name', 'Description',
                               'Series', 'NameWithSeries', 'InstrumentID', 'PriceBand.High', 'PriceBand.Low',
                               'FreezeQty', 'TickSize', 'LotSize', 'Multiplier'])

    filtered_df = df[df['Series'] == 'EQ']

    # Select only the 'Name', 'ExchangeInstrumentID', and 'Series' columns
    selected_columns = ['Name', 'ExchangeInstrumentID', 'Series']
    result_df = filtered_df[selected_columns]
    current_time = datetime.now()
    if current_time.hour > 15 or (current_time.hour == 15 and current_time.minute >= 30):
        # Set the end_time to 3:30 PM
        end_time = current_time.replace(hour=13, minute=29, second=0, microsecond=0)
    else:
        # Set the end_time to the current time
        end_time = current_time

    # Calculate the start_time and end_time
    start_time = current_time - timedelta(minutes=1)
    end_time = current_time

    # Convert start_time and end_time to the required string format
    start_time_str = start_time.strftime('%b %d %Y %H%M%S')
    end_time_str = end_time.strftime('%b %d %Y %H%M%S')

    # Assuming you already have the filtered DataFrame 'result_df' from the previous code

    # Define the OHLC interval in seconds
    interval = 60

    # print(result_df)


    # Iterate over the rows of 'result_df' and call 'xt.get_ohlc' for each 'ExchangeInstrumentID'
    print("Please wait. It can takes some times....")
    i=0
    for index, row in result_df.iterrows():
        exchange_instrument_id = row['ExchangeInstrumentID']
        # print(i)
        percentage_completion = ((i + 1) / len(result_df.index)) * 100
        print(str(percentage_completion) + "%" + "=>")
        i=i+1
        # print(exchange_instrument_id)
        try:
            ohlc_data = xt.get_ohlc("NSECM", int(exchange_instrument_id), start_time_str, end_time_str, interval)
            rows = rows + row['Name'] + '|' + ohlc_data['result']['dataReponse']+","
            print(ohlc_data['result']['dataReponse'])

        except Exception as e:
            pass

    rows = rows.strip(',').split(',')
    data_list = []

    # print(rows)

    for row in rows:
        row_data = row.split('|')
        timestamp = int(row_data[1])  # Assuming the timestamp is in the first column
        human_readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        row_data[1] = human_readable_time
        data_list.append(row_data)
    column_names = [
        'Stock', 'Time of Fetch', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI', ''
    ]

    # Assign column names to the DataFrame
    df = pd.DataFrame(data_list, columns=column_names)
    output_excel = output_excel + end_time_str + ".xlsx"
    df.to_excel(output_excel, index=False)
else:
    print("There is problem while login.")
