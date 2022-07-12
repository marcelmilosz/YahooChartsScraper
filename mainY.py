import yfinance as yf   
import pandas as pd
import os 
import plotly.graph_objects as go
import numpy as np

from datetime import *
from calendar import c
from plotly.subplots import make_subplots

# All stocks that we want to put on charts (PUT YOURS HERE FROM: https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI)
STOCKS = ['BTC-USD', '^DJI']  

lStocks = len(STOCKS)               # Just a len of those stocks :D

STARTING_DATE   = '2014-01-01'
ENDING_DATE     = '2022-07-01'
TODAY_DATE      = date.today().strftime("%Y-%m-%d")

### ALL ABOUT DISPLAYING TIME INTERVAL (NOT IMPORTANT)
sy, sm, sd = STARTING_DATE.split("-")
ey, em, ed = ENDING_DATE.split("-")
dSTARTING_DATE = date(int(sy), int(sm), int(sd))
dENDING_DATE = date(int(ey), int(em), int(ed))


daysDiff = abs(dSTARTING_DATE-dENDING_DATE).days
yearDiff = int(ey) - int(sy)
monthDiff = 0
if yearDiff == 0:
    monthDiff = int(em) - int(sm)

if int(em) > int(sm):
    monthDiff = int(em) - int(sm)
elif int(em) < int(sm):
    yearDiff -= 1
    monthDiff = int(sm) - int(em)


print("\n")
print("==" * 20)


print(f"Creating {lStocks} charts of: ")
for s in STOCKS:
    print(f" - {s}")

print(f"\nStarting date: {STARTING_DATE}")
print(f"Ending date: {ENDING_DATE}")
print(f"Today date: {TODAY_DATE}")
print(f"The time interval: ")
print(f" Years: {yearDiff}")
print(f" Monts: {monthDiff}")
print(f" Days: {daysDiff}")


print("==" * 20)
print("\n")

def getDataFromXlsx(stock, printInfo = False):

    '''
    This function opens specific file.xlsx and reads everything from it

    stock: str | name of file (yahoo Symbol) ^DJI, TSLA, TWTR etc.
    printInfo: bool | just to print additional info about file data 

    return: pandas data frame
    '''

    if printInfo:

        try:
            print(f"\nGetting data from Excels/stock-{stock} to pandas arr")
            xlsx_data = pd.read_excel(f"Excels/stock-{stock}.xlsx")
            return xlsx_data

        except Exception as E:
            print("\nSomething went wrong with 'getDataFromXlsx()'")
            print(f"\nCannot get data from Excels/stock{stock}.xlsx..")
            print(f"Input: stock = {stock}")
            print(f"Error msg: \n{E}")

            return 0

    else:
        try:
            # print(f"\nGetting data from Excels/stock-{stock} to pandas arr")
            xlsx_data = pd.read_excel(f"Excels/stock-{stock}.xlsx")
            return xlsx_data

        except Exception as E:
            print("\nSomething went wrong with 'getDataFromXlsx()'")
            print(f"\nCannot get data from Excels/stock{stock}.xlsx..")
            print(f"Input: stock = {stock}")
            print(f"Error msg: \n{E}")

            return 0

def getDataFromYahoo(stock, fromDay, toDay):
    '''
    We take data from yfinance using current self stock name

    stock: str | name of file (yahoo Symbol) ^DJI, TSLA, TWTR etc.
    fromDay: str starting Date '2017-01-01'
    toDay  : str ending Date '2017-01-01'
    
    return: pandas array
    '''

    try:
        print(f"\n** Getting {stock} data **")
        Data = yf.download(stock, fromDay, toDay)
        lData = len(Data)

        print("First 3 rows..") 
        print(Data[0:3])

        print(f"Rows: {lData}")

        return Data

    except Exception as E:
        print("\nSomething went wrong with 'getDataFromYahoo()'")
        print(f"Input: stock = {stock}, fromDay = {fromDay}, toDay = {toDay}")
        print(f"Error msg: {E}\n")

        return 0
        
def saveDataToXlsx(data, stock):
    '''
    This function saves data captured from yahoo to xlsx with appropriate file name

    data: pandas data frame | all captured from getDataFromYahoo()
    stock: str | name of file (yahoo Symbol) ^DJI, TSLA, TWTR etc.

    return: None
    '''

    if len(data) > 0:
        print(f"\nSaving {stock} data to Excel!")
        data.to_excel(f"Excels/stock-{stock}.xlsx", sheet_name='Sheet1') 
    else:
        print(f"Something went wrong in 'saveDataToXlsx()'")
        print(f"Stock = {stock}\nData = {data}")

def putAllOnPlot(stocks, downloadAll = False):

    '''
    This function does all everything. Reads data from XLSX, puts every single xlsx as chart in .html 
    If we have only two STOCKS, then additionaly it calculates correlation for us

    stock: str | name of file (yahoo Symbol) ^DJI, TSLA, TWTR etc.
    downloadAll: If we want to update already downloaded xlsx files (Usefull if we changed Starting / Ending dates)

    return: None
    '''

    print("\nLets put all those stocks together!")
    print(f"List: {stocks}")

    lStocks = len(stocks)
    currentXlsx = os.listdir("Excels/")
    missingXlsx = []

    DFS = []

    # IF we want to download all XLSX again (update or different dates)
    if downloadAll:
        for stock in stocks:
            yh = getDataFromYahoo(stock, STARTING_DATE, ENDING_DATE)
            saveDataToXlsx(yh, stock)
            DFS.append(getDataFromXlsx(stock))
    else:
        
        # Checking what we already have downloaded!
        print("\nBelow are files that we already downloaded:")
        

        for i in range(0, lStocks):

            fName = "stock-" + stocks[i] + ".xlsx"
            if fName in currentXlsx:
                print(f" - {fName}")
                DFS.append(getDataFromXlsx(stocks[i], False))
            else:
                missingXlsx.append(stocks[i])

        if len(missingXlsx) > 0:
            print(f"\nWe are missing: {missingXlsx}")
            print("Downloading them right now!")

            for missing_stock in missingXlsx:
                yh = getDataFromYahoo(missing_stock, STARTING_DATE, ENDING_DATE)
                saveDataToXlsx(yh, missing_stock)
                DFS.append(getDataFromXlsx(missing_stock))

            print("\nDownloaded all missing XLSX!")

    print("\nI added all your stocks to array variable, now trying to plot them!")

    # We are adding plots here
    try:
        fig = make_subplots(rows=len(stocks), cols=1)

        fig.update_layout(
            font_family="Arial",
            font_color="black",
            title="Plot Title",
            xaxis_title="Date",
            yaxis_title="Price",
            title_font_family="Times New Roman",
            title_font_color="black",
            legend_title_font_color="black"
        )

        for i in range(0, len(stocks)):
            DATES = (DFS[i].iloc[:, 0]).tolist()   # First column is date!
            df = DFS[i]['Close'].tolist()
            # print(df[0:10])
            fig.add_trace(go.Scatter(x=DATES, y=df, name=stocks[i]), row=(i + 1), col=1)

        
        # Calculating correlation (If user added only two STOCKS)
        title_text = "Check your charts!"

        if len(DFS) == 2:
            arr1 = DFS[0]['Close'].tolist()
            arr2 = DFS[1]['Close'].tolist()

            diffLen = len(max(list(arr1), list(arr2)))

            arr1 = np.array(arr1[0: diffLen])
            arr2 = np.array(arr2[0: diffLen])

            print("\nCalculating correlation..")

            corr = np.corrcoef(arr1, arr2)
            corrT = round(corr[0][1], 2)

            title_text = f"Correlation is equal = {corrT}%\n"
            additional_text = ""
            if corrT >= 0.5:
                additional_text = "Strong correlation!"
            elif corrT < 0.5 and corrT >= 0.3:
                additional_text = "Moderate correlation!"
            elif corrT < 0.3 and corrT > 0:
                additional_text = "Small correlation.. "
            else:
                additional_text = "No correlation at all!"

            title_text += additional_text

        print(f"{title_text}\n")
        figHeight = lStocks * 350
        fig.update_layout(height=figHeight, width=1720, title_text=title_text)
        fig.show()
        

    except Exception as E:
        print("\nSomething went wrong while putting stuff on plot! putAllOnPlot()")
        print(f"Error message: \n{E}\n")


putAllOnPlot(STOCKS, False)



# Gdybyś chciał nałożyć dwa ploty na jeden figure
# fig = go.Figure()

# fig.add_trace(go.Scatter(x=DATES, y=TSLA, name="TSLA"))
# fig.add_trace(go.Scatter(x=DATES, y=TWTR, name="TWTR"))

# fig.update_layout(height=600, width=1900, title_text="Compare this shit")
# fig.show()

 
















































# c = charty("SI=F")
# c.getStockInfo(STARTING_DATE, ENDING_DATE)
# c.saveStockToXlsx()
# c.getXlsxData()



# x = pd.read_excel(f"Excels/cry.xlsx")

# DATES = x.iloc[:, 0]
# TSLA = x['TSLA']
# AAPL = x['AAPL']
# TWTR = x['TWTR']

# figure, axis = plt.subplots(3)
# axis[0].plot(DATES, TSLA)
# axis[0].set_title("TSLA")

# axis[1].plot(DATES, AAPL)
# axis[1].set_title("AAPL")

# axis[2].plot(DATES, TWTR)
# axis[2].set_title("TWTR")



# plt.plot(DATES, TSLA, color='r', label='TSLA')
# plt.plot(DATES, AAPL, color='g', label='AAPL')
# plt.plot(DATES, AAPL, color='b', label='TWTR')
# plt.show()
