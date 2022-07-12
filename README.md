# yahooChartsScraper
This program gets data from Yahoo, you chose what charts you want to get (giving symbols of them). 

You can use this to get some specific charts from yahoo to compare and analyze them 
For example, we can look at bitcoin, nasdaq and sp500 on single window. 

There are only two variables that you need to change

STOCK where you input yahoo symbols to get chart 
STOCK = ['BTC-USD', '^DJI', '^IXIC']

STARTING_DATE and ENDING_DATE which are strings with format 'yy-mm-dd' to specify the time interval

We take data from: https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch

![chart](https://user-images.githubusercontent.com/61027817/178531903-88e6961e-336e-42c4-be1e-6fdf844b1bea.PNG)


IF STOCK gets only two symbols (len = 2) then we get additional correlation information 


![corr](https://user-images.githubusercontent.com/61027817/178533356-ede1b0e2-7778-4572-b12f-b8e35dfe6603.PNG)
