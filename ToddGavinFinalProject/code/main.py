from collectData import etherScanAPI_MultiWallet_Call, createTransactionsData_df, getStartAndEndDate, getCryptoHistoricalData
from organizeAndMergeData import addDateColumnToTokenPriceDataframe, orientDatesAndCorrespondingData, addColumns_dateBuySellValueMovementTotalGasCost, typeCastDateIn_rawTransactionData_df, addColumns_maticPriceTotalCostOCHL, createTransactionVolumeDF
from analyzeData import create_scatter_plot, create_line_plot, getDataForVisualizations

# Import Libraries
from Historic_Crypto import HistoricalData as HD
import pandas as pd
import requests
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats

# Execute Main function
if __name__ == '__main__':

    # Collect Data ***************************
    print("Running Collect Data....")
    listOfWallets = [
        '0x9507c04b10486547584c37bcbd931b2a4fee9a41',
        '0x5666ed92c83af9dab61601c87bf7769ad57103f9',
        '0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0',
        '0xed28b1c47375cd23aa6428544f4feaeaf3ee4e7b',
        '0xf977814e90da44bfa03b6295a0616a897441acec',
        '0xb72b8c812376b5f8436d6854d41646a88aa88422',
        '0x885f16e177d45fc9e7c87e1da9fd47a9cfce8e13',
        '0x4c569c1e541a19132ac893748e0ad54c7c989ff4'
    ]
    rawTransactionData = etherScanAPI_MultiWallet_Call(listOfWallets)
    rawTransactionData_df = createTransactionsData_df(rawTransactionData)
    startDate, endDate = getStartAndEndDate(rawTransactionData_df)
    tokenPriceData_df = getCryptoHistoricalData("MATIC-USD", startDate, endDate)

    # Organize and Merge Data ***************************
    print("Running Organize and Merge Data....")
    tokenPriceData_df = addDateColumnToTokenPriceDataframe(tokenPriceData_df)
    rawTransactionData_df = orientDatesAndCorrespondingData(tokenPriceData_df, startDate, rawTransactionData_df)
    rawTransactionData_df = addColumns_dateBuySellValueMovementTotalGasCost(rawTransactionData_df, listOfWallets)
    rawTransactionData_df = typeCastDateIn_rawTransactionData_df(rawTransactionData_df)
    rawTransactionData_df = addColumns_maticPriceTotalCostOCHL(rawTransactionData_df, tokenPriceData_df)
    # Output the DataFrame to a CSV file
    rawTransactionData_df.to_csv('rawTransactionData_df.csv', index=True)

    timeSeriesTransactionData_df = createTransactionVolumeDF(rawTransactionData_df, tokenPriceData_df)
    # Output the DataFrame to a CSV file
    timeSeriesTransactionData_df.to_csv('timeSeriesTransactionData_df.csv', index=True)

    # Analyze Data and Visualize Data ***************************
    print("Running Analyze Data and Visualize Data....")
    maticPriceUSD, gasPriceUSD, numGas, OCdailyPrice, ABSOCdailyPrice, HLdailyPrice, totalCostUSD, ABStotalCostUSD, gasPrice, maticPriceUSDv2, maticPriceUSDx100000000, volume, ABSValueMovedUSD, buyNum, sellNum = getDataForVisualizations(rawTransactionData_df,timeSeriesTransactionData_df)

    create_scatter_plot(ABStotalCostUSD, maticPriceUSD, "ABS Total Cost USD VS MATIC Price USD", "Absolute Value of Total USD Moved", "MATIC Price USD", "Fig 1. Along the x-axis is the absolute value fo the total amount\n of MATIC moved (bought or sold) for a give day in USD.\n Along the y-axis is the price of MATIC in USD for a given\n corresponding day. The R-value is 0.0078 stating that there is\n no signifciant correlation between these two variables.")

    create_scatter_plot(maticPriceUSD, gasPriceUSD, "MATIC Price USD VS Gas Price", "MATIC Price USD", "Gas Price (Wei)", "Fig 2. Along the x-axis is the price of MATIC in USD\n for a given day. Along the y-axis is the gas price cost in\n wei for the corresponding given day. The R-value for the data is\n 0.026, therefore, there is nto a signficant correlation in the data.")

    create_scatter_plot(HLdailyPrice, ABSOCdailyPrice, "HL Daily Price VS ABS OC Daily Price", "High-Low Daily Price Difference USD", "ABS Open-CLose Price Difference USD", "Fig 3. Along the x-axis is the daily price difference between\n the high and low for a given day. Along the y-axis is the absolute\n value of the daily price difference between the open and close\n for the corresponding given day. The R-value is 0.77 with a\n P-value < 0.05, therefore, there is reasonable statistical\n correlation between the two variables. ")

    create_scatter_plot(buyNum, sellNum, "Buy Num VS Sell Num", "Buy Number", "Sell Number", "Fig 4. Along the x-axis is the number of buys for a given day\n and along the y-axis is the number of sells for the corresponding given day.\n The R-value is 0.75 and the P-value < 0.05, therefore, we can infer\n that there is a reasonable statistical correlation between the two varaibles.")

    create_line_plot(maticPriceUSDx100000000, "maticPriceUSD", volume, "volume", "maticPriceUSDx100000000 VS Volume", "Days since start date", "Magnitude", "Fig 5. This line plot depicts the price of MATIC to the magnitude\n of x100000000 and the volume of token movement for the\n corresponding day. There seems to be a slight resemblance between\n the volume moved and the peak prie of the MATIC token.")

    create_line_plot(maticPriceUSDx100000000, "maticPriceUSD", ABSValueMovedUSD, "ABSValueMovedUSD", "maticPriceUSDx100000000 VS ABS Value Moved USD", "Days since start date", "Magnitude", "Fig 6. This line plot depicts the price of MATIC to the magnitude\n of x100000000 and the absolute value token cost moved for\n the corresponding day.")

    create_line_plot(buyNum, "buyNum", sellNum, "sellNum", "Buy Num vs Sell Num", "Days since start date", "Magnitude", "Fig 7. This line plot depicts the number of buys against\n the number of sells for a corresponding day. There seems to\n be an association between the number of\n buys and number of sells for a particular day.")

    print("Code finished running...")