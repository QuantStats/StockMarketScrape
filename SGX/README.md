Different from the first example with KLSE (Kuala Lumpur Stock Exchange) is that this scrape involves a two-step process.

The first step is a scrape to collect and store all SGX-listed company names along with their stock codes. The first step is performed by the script 'SGXListings.py'.

The print output after a run of the script is shown as follows,

![alt text](https://github.com/QuantStats/StockMarketScrape/blob/master/SGX/SGXStockTable.png)

The second step loads the stored data from the first step, then performs the rest of the scrapping process to collect the relevant financial info. The first step is performed by the script 'SGXScrape.py'.

A cross-sectional stock market data is gathered and stored after the script in the second step finishes its run. The data is stored in various file formats that can be read by a spreadsheet program. A possible application for an investor is to sort the stock by a variable of interest, say dividend yield to find the highest dividend-yielding stocks.

The script can be scheduled to run daily using _Task Scheduler_ in Windows or _Cron_ in Unix/Linux. With a daily run over time, a time-series stock market data can be obtained.

The automated processes of the script can be briefly summarized as follows:

1. Navigate to the webpage (inspect the script for details of the webpage) where financial market data are stored for each stock listing on SGX.

2. Save the stored financial data for each stock. For a sample of the stored financial data, see the file `sgx_prices.csv`. 

For each stock, the following financial data are stored:

* Name: company name and KLSE stock code.
* Divy: dividend yield in percentage.
* Div: total dividend over the past 12 months in cents.
* Price: last closing price of the stock in SGD.
* Low1: daily low of the stock price in SGD.
* High1: daily high of the stock price in SGD.
* Low52: yearly low of the stock price in SGD.
* High52: yearly high of the stock price in SGD.
* EPS: earnings per share of the stock in cents.
* PE: price-earning-ratio of the stock (unitless measure).
* Vol: average volume in a year in unit stocks.
* Cap: market capitalization in MYR, the post-text _M_ and _B_ represent million and billion respectively.

\* Note that the abbreviation SGD is Singapore dollar. A cent in the context above is a unit of SGD divided by 100.

The print output after a run of the script is shown below:

![alt text](https://github.com/QuantStats/StockMarketScrape/blob/master/SGX/SGXStockScrape.png)
