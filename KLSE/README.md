The script `KLSEScrape.py` scrapes financial market data from all stock listings on KLSE (Kuala Lumpur Stock Exchange).

A cross-sectional stock market data is gathered and stored after the script finishes its run. The data is stored in various file formats that can be read by a spreadsheet program. A possible application for an investor is to sort the stock by a variable of interest, say dividend yield to find the highest dividend-yielding stocks.

The script can be scheduled to run daily using _Task Scheduler_ in Windows or _Cron_ in Unix/Linux. With a daily run over time, a time-series of stock market data can be obtained.

The automated processes of the script can be briefly summarized as follows:

1. Navigate to the web page (inspect the script for details of the web page) where financial market data are stored for each stock listing on KLSE.

2. Click on each tab from: 0-9, A, B, ..., Z and retrieve all stock listings on each tab.

3. After all the stock listings are retrieved, the script navigates to the individual link of each stock. The script then scrapes and stores financial data from each stock listing. Repeat this process until every stock is scraped on the stock listings.

4. Save the stored financial data for each stock. For a sample of the stored financial data, see the file `klse_prices.csv`. 

For each stock, the following financial data are stored:

* Name: company name and KLSE stock code.
* Divy: dividend yield in percentage.
* Div: total dividend over the past 12 months in cents.
* Price: last closing price of the stock in MYR.
* Low7: weekly low of the stock price in MYR.
* High7: weekly high of the stock price in MYR.
* Low52: yearly low of the stock price in MYR.
* High52: yearly high of the stock price in MYR.
* EPS: earnings per share of the stock in cents.
* PE: price-earning-ratio of the stock (unitless measure).
* ROE: return on equity in percentage.
* NTA: net tangible assets in MYR.
* Vol: average volume in a year in unit stocks.
* Cap: market capitalization in MYR, the post-text _m_ and _b_ represent million and billion respectively.

\* Note that the abbreviation MYR is Malaysian Ringgt. A cent in the context above is a unit of MYR divided by 100.

The print output after a run of the script is shown below:

![alt text](https://github.com/QuantStats/StockMarketScrape/blob/master/KLSE/Images/KLSEStockScrape.png)
