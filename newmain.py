import os
import time
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
    result_df = pd.read_excel('mainstocks.xlsx', sheet_name='498 Stocks v2')
    current_time = datetime.now()

    if current_time.weekday() == 5 or current_time.weekday() == 6:
        print("You can not run this program on Saturday or Sunday.")
    else:
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
        interval = 60
        i = 0
        rows=''
        exchange_instrument_id = []
        for index, row in result_df.iterrows():
            exchange_instrument_id.append(int(row['ExchangeInstrumentID']))
            i = i + 1
        try:
            ohlc_data = xt.get_ohlc("NSECM", [13061,474], start_time_str, end_time_str, interval)

        except Exception as e:
            print(e)

        print(ohlc_data)

        # rows = rows.strip(',').split(',')
        # data_list = []
        #
        # for row in rows:
        #     row_data = row.split('|')
        #     data_list.append(row_data)
        # column_names = [
        #     'Stock', 'Time of Fetch', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI', ''
        # ]
        #
        # # Assign column names to the DataFrame
        # df = pd.DataFrame(data_list, columns=column_names)
        # output_excel = output_excel + "_"+ end_time_str + ".xlsx"
        # df.to_excel(output_excel, index=False)
else:
    print("There is problem while login.")
