# DSCI 510 - Analyzing MATIC token crypto wallet transaction data and price data

Title: Analyzing how the transaction data from major cryptocurrency wallets on the polygon network associate with the price action of the MATIC token.

Description: The MATIC token is a cryptocurrency that operates of the Polygon layer 2 network that sits on top of the Ethereum network. Essentially, the project collects a long list of transaction data and metadata associated with each transaction for each wallet listed in the function. Once the transaction data is collected, it is merged with a price action dataset for the MATIC token. Using the data frames, a series of analysis using line graphs, scatter plots, and linear regression analyses are used to analyze and interpret the data.


# Dependencies

> A list of all of the dependencies used, including their version number:

pandas==1.4.4
requests==2.28.1
ujson==5.4.0
datetime==2.11.1
matplotlib==3.5.2
seaborn==0.11.2
scipy==1.9.1
historic-crypto==0.1.6

# Installation

To install the requirements necessary to run this project, on MacOS, open a new terminal atteh folder for which the repository was forked to, and run this line of code:

```
pip install -r requirements.txt
```

# Running the project

To run the project, there are two ways: 
1. Project may be ran as a Python Notebook (.ipynb) in VScode or IDE equivalent.
2. Project may be ran as Python scripts (.py) in terminal.

`Run as Python Notebook (Most preferable to elicit best result):`
A.	Download the file ‘masterCode.ipynb’ from the ‘/code’ folder. 
B.	Open sed file in VScode or another python notebook compiler such as Jupyter.
C.	Censure that all the dependencies are pip installed on to your device for which you are running the code on.
D.	In the same folder for which you store sed file in, create a folder called ‘visualizations’. (The plots will be saved to this folder once the code runs.)
E.	Click ‘run all’ at the top of your interpreter and let the magic happen!

`Run as Python Script:`
A.	Download the files ‘main.py, collectData.py, organizeAndMergeData.py, analyzeData.py’ from the ‘/code’ folder. Make sure to pip install the ‘requirements.txt’ file.
B.	In the same folder for which you store sed file in, create a folder called ‘visualizations’. (The plots will be saved to this folder once the code runs.)
C.	Open a terminal at the folder for which the code is stored in and run the command ‘python main.py’. And let the magic happen. 

```
python code/main.py
```

# Methodology

The code is broken down into 3 parts:
1. Collect Data: Collecting the token price data from the Historic_Crypto Python library and the crypto wallets transaction data from the Etherscan API.
2. Organize and Merge Data: Combing and orienting the data from the two datasources into two dataframes: 1/ time series data for transaction information per day 2/ transaction data that provides metadata on each transaction that has taken place in a certain date/time range
3. Analyze and Visualize Data: The process of creating 7 figures for which 4 linear regression models were conducted on 8 variables. 

> What kind of analyses or visualizations did you do? (Similar to Homework 2 Q3, but now you should answer based on your progress, rather than just your plan)  

I created 7 visualizations for which I performed a linear regression analysis on the first 4 of the 7 visualization variables. 

- The first 4 visualization are scatter plots with linear regssion lines and ranges. 
- The final 3 visualization are overlapping line graphs. 


# Visualization

- `Which visualization methods did we use`
    - Scatter Plots and layered line graphs are the visualization methods
- `Why did we chose this particular way of visualizing data`
    - This particualr way of visualization provides us with two variations as to analyze the relationship between two variables to determine if there is an association between the two. 
- `What insights are revealed through the means of this visualization`
    - Overall, there are no statstically significant correlations or association in the data between transaction data and token price data of the MATIC token.
    - However, there is somewhat of a realtionship between the rate at which token rpice chnages and the amount of volume of the token moving suggesting that teh greater the toekn price moveds in a day, the more volume fo that token moved in a day. (Which essentially proves the exsistence of a competive stock market.)

Figure visualizations are as followed:

`Scatter Plots with Linear Regression Models:` 
- Fig 1. Along the x-axis is the absolute value of the total amount of MATIC moved (bought or sold) for a give day in USD. Along the y-axis is the price of MATIC in USD for a given corresponding day. The R-value is 0.0078 stating that there is no significant correlation between these two variables.
- Fig 2. Along the x-axis is the price of MATIC in USD for a given day. Along the y-axis is the gas price cost in wei for the corresponding given day. The R-value for the data is 0.026, therefore, there is to a significant correlation in the data.
- Fig 3. Along the x-axis is the daily price difference between the high and low for a given day. Along the y-axis is the absolute value of the daily price difference between the open and close for the corresponding given day. The R-value is 0.77 with a P-value < 0.05, therefore, there is reasonable statistical correlation between the two variables.
- Fig 4. Along the x-axis is the number of buys for a given day and along the y-axis is the number of sells for the corresponding given day. The R-value is 0.75 and the P-value < 0.05, therefore, we can infer that there is a reasonable statistical correlation between the two variables.

`Overlapping Line Graphs`
- Fig 5. This line plot depicts the price of MATIC to the magnitude of x100000000 and the volume of token movement for the corresponding day. There seems to be a slight resemblance between the volume moved and the peak price of the MATIC token.
- Fig 6. This line plot depicts the price of MATIC to the magnitude of x100000000 and the absolute value token cost moved for the corresponding day.
- Fig 7. This line plot depicts the number of buys against the number of sells for a corresponding day. There seems to be an association between the number of buys and number of sells for a particular day.

# Conclusion: 

From the data, regression models, and visualizations, there seems to be very little significant association between the transaction data for the major crypto wallets trading MATIC, and the pricing and price action of the MATIC token. Although there are two figure that seem to have a significant correlation, they do not provide a unique predicter for when to purchase or sell the MATIC token. Overall, it goes to show how unpredictable the cryptocurrency market is and even with the best traded crypto wallets, even they do not have a formula for when to buy and sell the MATIC token so that it is the most profitable. 

# Future Work

> Given more time, what is the direction that you would want to take this project in?  

Given more time, I would search for more granular data on the transaction history of a specific crypto wallet. Preferable, I’d like to gather more transaction while also knowing the current amount of MATIC token that is in a crypto wallet at a specific date and time. I would that be able to analyze the existence of (or lack of a) relationship between the crypto wallet MATIC token balance and the pricing of the MATIC token relative to its previous pricing. 
