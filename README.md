# stock_screener_r-d_py
 - A Python tool to display stocks trading data with dividend/earning values of the earning/dividend release day
 - The program is tested with Python3.6.6, tabulate0.8.7, bs40.0.1
 - The program requires three inputs: dividend_earning_list.py dividends(or earnings) date(in the form m/d/yyyy)
 - The program outputs a table listing Dividends/Earnings, Notes, Names(stock name), Prices(current trading prices), Changes(price changes), Percentages(percenatge changes), Open(opening prices), Close(closing prices), 52Highs(53 week hightest prices), 52Lows(52 week lowest prices), 52Perf(52 week price performance), Volumes(trading volume)
 - The "Earnings" is the earning surprises which is the difference between expected earnings and actual earnings
 - The Notes: "+ or -", current price increased or decreased; "\*/", current price is within 5% of 52 week high; "/\*", current price is within 5% of 52 week low
 - The program is created for users to monitor the stock trading performance on the day the earnings are released or on the day dividends are distributed
 - The data is extracted from Fidality website
