import os
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

"""Make XTSConnect object by passing your 
interactive API appKey, 
secretKey and source"""


xt = XTSConnect(API_KEY, API_SECRET, source)
"""Using the xt object we created call the interactive login Request"""
response = xt.marketdata_login()

if response['type'] == 'success':
    exchangesegment = [xt.EXCHANGE_NSECM]
    response =xt.get_master(exchangeSegmentList=exchangesegment)

    file_path_temp = "EXCHANGE_NSECM.txt"
    excel_file_path = input("Enter excel file name(only file name without spache and .xlsx etc) ")
    excel_file_path = excel_file_path + ".xlsx"
    # Check if the file exists, and if it does, delete it
    if os.path.exists(file_path_temp):
        os.remove(file_path_temp)

    if os.path.exists(file_path_temp):
        os.remove(excel_file_path)

    # Now create and write the new file
    with open(file_path_temp, "w") as f:
        f.write(response["result"])

    df = pd.read_csv(file_path_temp, sep="|", low_memory=True, usecols=range(14), header=None)
    new_column_names = [
        'ExchangeSegment',
        'ExchangeInstrumentID',
        'InstrumentType',
        'Name',
        'Description',
        'Series',
        'NameWithSeries',
        'InstrumentID',
        'PriceBand.High',
        'PriceBand.Low',
        'FreezeQty',
        'TickSize',
        'LotSize',
        'Multiplier'
    ]

    # Get the current column names of the DataFrame
    df.columns=new_column_names
    # Export the DataFrame to Excel
    df.to_excel(excel_file_path, index=False)
else:
    print("There is problem while login.")


