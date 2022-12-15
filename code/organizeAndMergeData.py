from Historic_Crypto import HistoricalData as HD
import pandas as pd
import requests
import ujson
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
import time

def convert_UNIX_to_DateTime(unix):
    return datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S') # 

def addDateColumnToTokenPriceDataframe(tokenPriceData_df):
    tokenPriceData_df.insert(1, 'date', 0)

    for index, row in tokenPriceData_df.iterrows():
        date = str(row["time"])[0:10]
        tokenPriceData_df.loc[index, "date"] = date

    tokenPriceData_df = tokenPriceData_df.drop('time', axis=1)

    return tokenPriceData_df

def orientDatesAndCorrespondingData(tokenPriceData_df, startDate, rawTransactionData_df): 
    startDate2 = str(tokenPriceData_df.loc[0, "date"]) + " 00:00:00"
    # print(startDate2)

    # Define a format string for the date and time
    date_time_fmt = "%Y-%m-%d %H:%M:%S"
    # Convert the string to a datetime object
    startDate2 = datetime.strptime(startDate2, date_time_fmt)

    # Print the datetime object
    # print(startDate2)

    # convert the datetime object into a Unix timestamp
    startDate2_UNIX = time.mktime(startDate2.timetuple())

    # print(startDate_UNIX)
    # print(startDate2_UNIX)

    startDate = str(startDate) + " 00:00:00"
    # print(startDate)
    startDate1 = datetime.strptime(startDate, date_time_fmt)
    startDate1_UNIX = time.mktime(startDate1.timetuple())

    # print(startDate, startDate1_UNIX)

    # The transactions start date is later than the crypto data start date
    if int(startDate1_UNIX) > int(startDate2_UNIX):
        startDate_main_UNIX = startDate1_UNIX

    # The transactions start date is earlier than the crypto data start date
    else:
        startDate_main_UNIX = startDate2_UNIX

    # print the Unix timestamp
    # print(startDate_main_UNIX)

    endDate = tokenPriceData_df.loc[len(tokenPriceData_df.index)-1, "date"]
    # print(endDate)

    rawTransactionData_df['timeStamp'] = rawTransactionData_df['timeStamp'].astype(float)

    rawTransactionData_df = rawTransactionData_df.drop(rawTransactionData_df.index[rawTransactionData_df.loc[:, 'timeStamp'] < startDate_main_UNIX])

    rawTransactionData_df = rawTransactionData_df.reset_index(drop=True)

    return rawTransactionData_df

def addColumns_dateBuySellValueMovementTotalGasCost(rawTransactionData_df, listOfWallets):

    # Adding data column
    rawTransactionData_df.insert(1, 'date', 0)
    for index, row in rawTransactionData_df.iterrows():
        date = convert_UNIX_to_DateTime(row["timeStamp"])[0:10]
        rawTransactionData_df.loc[index, "date"] = date

    # Adding valueMovement and tradeType columns
    rawTransactionData_df.insert(4, 'valueMovement', 0)
    rawTransactionData_df.insert(5, 'tradeType', 0)

    for index, row in rawTransactionData_df.iterrows():
        tradeType = "n/a"
        # considered a BUY
        if row["to"] in listOfWallets:
            valueMovement = int(row["value"])/(10**18)
            tradeType = "BUY"
        # considered a SELL
        elif row["from"] in listOfWallets:
            valueMovement = -1 * (int(row["value"])/(10**18))
            tradeType = "SELL"

        rawTransactionData_df.loc[index, "valueMovement"] = valueMovement
        rawTransactionData_df.loc[index, "tradeType"] = tradeType

    rawTransactionData_df = rawTransactionData_df.drop('value', axis=1)

    # Adding totalGasCost column
    rawTransactionData_df.insert(9, 'totalGasCost', 0)

    for index, row in rawTransactionData_df.iterrows():
        totalGasCost = int(row['gas']) * int(row['gasPrice'])
        rawTransactionData_df.loc[index, "totalGasCost"] = totalGasCost

    return rawTransactionData_df

def typeCastDateIn_rawTransactionData_df(rawTransactionData_df):
    # convert the column to dataTypes
    rawTransactionData_df['date'] = rawTransactionData_df['date'].astype(str)

    rawTransactionData_df['valueMovement'] = rawTransactionData_df['valueMovement'].astype(int)

    rawTransactionData_df['gas'] = rawTransactionData_df['gas'].astype(float)

    rawTransactionData_df['gasPrice'] = rawTransactionData_df['gasPrice'].astype(float)

    rawTransactionData_df['totalGasCost'] = rawTransactionData_df['totalGasCost'].astype(int)

    return rawTransactionData_df

def addColumns_maticPriceTotalCostOCHL(rawTransactionData_df, tokenPriceData_df):

    # Adding priceUSD column
    rawTransactionData_df.insert(7, 'priceUSD', 0)

    for index, row in rawTransactionData_df.iterrows():
        # print("ran...")
        date = rawTransactionData_df.loc[index, "date"]
        # print("date:", date)
        dateRow_df = tokenPriceData_df.loc[tokenPriceData_df['date'] == date]
        # print("dateRow:\n", dateRow_df)
        dateRow_df = dateRow_df.reset_index(drop=True)
        price = (float(dateRow_df.loc[0, "open"]) + float(dateRow_df.loc[0, "close"]))/2
        # print("price:", price)

        rawTransactionData_df.loc[index, "priceUSD"] = price

    # Adding totalCostUSD column
    rawTransactionData_df.insert(8, 'totalCostUSD', 0)

    for index, row in rawTransactionData_df.iterrows():
        totalCost = float(row["valueMovement"]) * float(row["priceUSD"])
        rawTransactionData_df.loc[index, "totalCostUSD"] = totalCost

    # Adding OCdailyPriceMovementUSD and HLdailyPriceMovementUSD scolumn
    rawTransactionData_df.insert(9, 'OCdailyPriceMovementUSD', 0)
    rawTransactionData_df.insert(10, 'HLdailyPriceMovementUSD', 0)

    for index, row in rawTransactionData_df.iterrows():

        date = rawTransactionData_df.loc[index, "date"]

        maticPrice_df = tokenPriceData_df.loc[tokenPriceData_df['date'] == date]
        maticPrice_df = maticPrice_df.reset_index(drop=True)

        open = maticPrice_df.loc[0, "open"]
        close = maticPrice_df.loc[0, "close"]
        high = maticPrice_df.loc[0, "high"]
        low = maticPrice_df.loc[0, "low"]
        
        OCprice = open - close
        HLprice = high - low

        rawTransactionData_df.loc[index, "OCdailyPriceMovementUSD"] = OCprice
        rawTransactionData_df.loc[index, "HLdailyPriceMovementUSD"] = HLprice

    rawTransactionData_df = rawTransactionData_df.sort_values("timeStamp")
    rawTransactionData_df = rawTransactionData_df.reset_index(drop=True)

    return rawTransactionData_df

def createTransactionVolumeDF(rawTransactionData_df, tokenPriceData_df):

    datesList = tokenPriceData_df['date'].to_list()
    # print(len(datesList))
    # print(datesList[0:5])

    # Columns: -Index, #Date, *Num Transactions, *Value Movement, *Num BUYS, *Num Sells, *MATIC Price USD, -Total Cost USD, *OC daily price, *HL daily price

    dateToDailyTransactionInfoDict = {}

    for date in datesList:

        transaction_df = rawTransactionData_df.loc[rawTransactionData_df['date'] == date]
        transaction_df = transaction_df.reset_index(drop=True)

        # print("transaction_df\n", transaction_df, "\nend df...")

        if not transaction_df.empty:

            # loop through every row in the DataFrame and print the values
            for index, row in transaction_df.iterrows():

                valueMoved = row["valueMovement"]
                tradeType = row["tradeType"]

                if tradeType == "BUY":
                    buy = 1
                    sell = 0
                else: 
                    sell = 1
                    buy = 0

                if date not in dateToDailyTransactionInfoDict.keys():
                    # print('run if..')
                    dateToDailyTransactionInfoDict[date] = [1, valueMoved, buy, sell]

                # elif date in dateToDailyTransactionInfoDict.keys():
                else:
                    # print('run elif..')
                    currentTransactionInfo = dateToDailyTransactionInfoDict.get(date)

                    currentNumTransactions = int(currentTransactionInfo[0]) + 1
                    currentValueMoved = currentTransactionInfo[1] + valueMoved
                    currentBuyNum = currentTransactionInfo[2] + buy
                    currentSellNum = currentTransactionInfo[3] + sell

                    dateToDailyTransactionInfoDict[date] = [currentNumTransactions, currentValueMoved, currentBuyNum, currentSellNum]

                # print(date, dateToDailyTransactionInfoDict.get(date))

        else:

            dateToDailyTransactionInfoDict[date] = [0, 0, 0, 0]

        # print(date, dateToDailyTransactionInfoDict.get(date))

    # create an empty list to store the lists
    dateToDailyTransactionInfoList = []

    # iterate over the dictionary's items and create a new list with the key as the first element and the value as the second element
    for key, value in dateToDailyTransactionInfoDict.items():
        dateToDailyTransactionInfoList.append([key, value[0], value[1], value[2], value[3]])

    columnNames = ["date", "numTransactions", "valueMoved", "buyNum", "sellNum"]
    timeSeriesTransactionData_df = pd.DataFrame(dateToDailyTransactionInfoList, columns=columnNames)

    maticPriceUSD = (tokenPriceData_df["open"] + tokenPriceData_df["close"])/2
    volume = list(tokenPriceData_df["volume"])

    timeSeriesTransactionData_df["MaticPriceUSD"] = maticPriceUSD
    timeSeriesTransactionData_df["volume"] = volume

    return timeSeriesTransactionData_df