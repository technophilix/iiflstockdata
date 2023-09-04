import os
from datetime import datetime

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
file_path_temp='OHLC.txt'
"""Make XTSConnect object by passing your 
interactive API appKey, 
secretKey and source"""


xt = XTSConnect(API_KEY, API_SECRET, source)
"""Using the xt object we created call the interactive login Request"""
response = xt.marketdata_login()

if response['type'] == 'success':

    output_excel = input("Enter the excel file name")
    output_excel = output_excel+ ".xlsx"
    exchangesegment = xt.EXCHANGE_NSECM
    response = xt.get_ohlc("NSECM", 22, 'Aug 22 2023 091500', 'Aug 22 2023 153000', 60)
    data = response['result']['dataReponse']
    rows = data.strip(',').split(',')
    for row in data_list:
        timestamp = int(row[0])  # Assuming the timestamp is in the first column
        human_readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        row[0] = human_readable_time
    df = pd.DataFrame([row.split('|') for row in rows])
    column_names = [
        'TIME', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI'
    ]

    # Assign column names to the DataFrame
    df.columns = column_names
    df.to_excel(output_excel, index=False)
else:
    pass



