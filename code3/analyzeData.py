from Historic_Crypto import HistoricalData as HD
import pandas as pd
import requests
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats

def performLinearRegression(data1, data2):
    a = data1
    b = data2

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(a, b)
    
    print("R_value:",r_value**2)
    print("P_value:",p_value)

def create_scatter_plot(data1, data2, title, xlabel, ylabel, figureText):

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.figtext(0.5, -0.2, figureText, wrap=True, horizontalalignment='center', fontsize=12)

    # Use seaborn to plot the scatter plot
    sns.scatterplot(data1, data2)
    # Fit a regression line to the data and plot it on the scatter plot
    sns.regplot(data1, data2)

    plt.savefig("visualizations/"+title+".png", dpi=300, bbox_inches = "tight")

    # Show the plot
    plt.show()

    performLinearRegression(data1, data2)

def create_line_plot(data1, data1Label, data2, data2Label, title, xlabel, ylabel, figureText):

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.figtext(0.5, -0.2, figureText, wrap=True, horizontalalignment='center', fontsize=12)

    # Create the plot
    plt.plot(data1, color="orange", label=data1Label)
    plt.plot(data2, color="blue", label=data2Label)

    # Add a legend to the plot
    plt.legend()

    # add a description to the graph
    # text = textwrap.wrap(description, width=40)
    # plt.text(0, 20,'\n'.join(text), fontsize=10, ha='left', va='bottom')

    # plots bar chart of keys (x) against values (y)
    plt.savefig("visualizations/"+title+".png", dpi=300, bbox_inches = "tight")

def getDataForVisualizations(rawTransactionData_df,timeSeriesTransactionData_df):

    # rawTransactionData_df
    maticPriceUSD = list(rawTransactionData_df["priceUSD"])

    gasPriceUSD = list(rawTransactionData_df["gasPrice"])

    numGas = list(rawTransactionData_df["gas"])
    numGas = [float(abs(x)) for x in numGas]

    OCdailyPrice = list(rawTransactionData_df["OCdailyPriceMovementUSD"])
    ABSOCdailyPrice = [float(abs(x)) for x in OCdailyPrice]

    HLdailyPrice = list(rawTransactionData_df["HLdailyPriceMovementUSD"])

    totalCostUSD = list(rawTransactionData_df["totalCostUSD"])
    ABStotalCostUSD = [float(abs(x)) for x in totalCostUSD]

    gasPrice = list(rawTransactionData_df["gasPrice"])

    # timeSeriesTransactionData_df
    maticPriceUSDv2 = list(timeSeriesTransactionData_df["MaticPriceUSD"])
    maticPriceUSDx100000000 = [(float(x)*100000000) for x in maticPriceUSDv2]

    volume = list(timeSeriesTransactionData_df["volume"])

    ABSValueMovedUSD = list(timeSeriesTransactionData_df["valueMoved"])
    ABSValueMovedUSD = [float(abs(x)) for x in ABSValueMovedUSD]

    buyNum = list(timeSeriesTransactionData_df["buyNum"])

    sellNum = list(timeSeriesTransactionData_df["sellNum"])

    return maticPriceUSD, gasPriceUSD, numGas, OCdailyPrice, ABSOCdailyPrice, HLdailyPrice, totalCostUSD, ABStotalCostUSD, gasPrice, maticPriceUSDv2, maticPriceUSDx100000000, volume, ABSValueMovedUSD, buyNum, sellNum