from Historic_Crypto import HistoricalData as HD
import pandas as pd
import requests
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats

def etherScanAPICall(wallet_address):
    API_KEY = 'JATAZ8XWIBGBTY15YJJEABCDPIF8SCK7S3'
    MATIC_CONTRACT_ADDRESS = '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0'
    # WALLET_ADDRESS = '0x9507c04b10486547584c37bcbd931b2a4fee9a41'
    url = 'https://api.etherscan.io/api?'

    parameters = {
        'module':'account',
        'action':'tokentx',
        'contractaddress':MATIC_CONTRACT_ADDRESS,
        'address':wallet_address,
        'page':'1',
        'offset':'10000',
        'startblock':'0',
        'endblock':'27025780',
        'sort':'asc',
        'apikey':API_KEY
    }

    responseJSON = requests.request("GET", url, params=parameters).json()

    print("# of Transactions:",len(responseJSON.get("result")))

    # with open("transactionsResponse.json", "w") as write_file:
    #     json.dump(responseJSON, write_file, indent=4, sort_keys = True)

    return responseJSON

def etherScanAPI_MultiWallet_Call(listOfWalletAddresses):

    totalTransactionDataList = []

    for wallet in listOfWalletAddresses:
        walletTransactionData = etherScanAPICall(wallet)
        totalTransactionDataList = totalTransactionDataList + walletTransactionData.get("result")

    return totalTransactionDataList

def createTransactionsData_df(rawTransactionData):

    # Create a DataFrame from the list of dictionaries
    rawTransactionData_df = pd.DataFrame(rawTransactionData)

    rawTransactionData_df = rawTransactionData_df.sort_values("timeStamp")
    rawTransactionData_df = rawTransactionData_df.reset_index(drop=True)

    rawTransactionData_df = rawTransactionData_df.drop('nonce', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('tokenName', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('tokenDecimal', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('input', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('confirmations', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('transactionIndex', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('blockNumber', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('hash', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('blockHash', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('gasUsed', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('cumulativeGasUsed', axis=1)
    rawTransactionData_df = rawTransactionData_df.drop('contractAddress', axis=1)

    # Print the names of all the columns in the dataframe
    # print(rawTransactionData_df.columns)

    return rawTransactionData_df

def convert_UNIX_to_DateTime(unix):
    return datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S') # 

def getStartAndEndDate(rawTransactionData_df):
    # Get the first row of the dataframe
    startDate_UNIX = rawTransactionData_df.loc[0, "timeStamp"]
    # Get the last row of the dataframe
    endDate_UNIX = rawTransactionData_df.loc[len(rawTransactionData_df.index)-1, "timeStamp"]

    startDate = str(convert_UNIX_to_DateTime(startDate_UNIX))[0:10]
    endDate = str(convert_UNIX_to_DateTime(endDate_UNIX))[0:10]

    return startDate, endDate

def getCryptoHistoricalData(token, startDate, endDate):
    data = HD(token,86400,startDate+"-00-00",endDate+"-00-00").retrieve_data()
    # data.to_csv('tokenPriceData.csv')
    data = data.reset_index(drop=False)
    data['volume'] = data['volume'].astype(float)
    return data