import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from math import nan as nan

#load the stock listings
listings = pd.read_csv('sgx_listings.csv')

#the dictionary to be stored into the panda dataframe
temp_dict = dict()

class Stock:
    def __init__(self, name):
        
        #initializations of variables (attributes) to be scraped
        #see below for the description of each variable
        self.Name = name
        self.Divy = nan
        self.Div = nan
        self.Price = nan
        self.Low1 = nan
        self.High1 = nan
        self.Low52 = nan
        self.High52 = nan
        self.EPS = nan
        self.PE = nan
        self.Vol = nan
        self.Cap = nan

    def scrape_and_assign(self, com_code):

        #get the company info url by company code
        com_url = 'https://sg.finance.yahoo.com/quote/'
        com_url = com_url+str(com_code)+'.SI?p=533.SI&.tsrc=fin-srch-v1'
        
        #process the company info page source in beautiful soup
        html = requests.get(com_url)
        html = BeautifulSoup(html.text, 'lxml')

        #get the web snippet where the key financial info are stored
        #snippet = html
        snippet = BeautifulSoup(str(html.find_all('div', id='quote-summary')), 'lxml')

        #assigning financial info        
        #price (last closing price (in SGD))
        temp = snippet.find(attrs={"data-test":'PREV_CLOSE-value'})

        if temp is None:
            pass

        else:
            self.Price = temp.text

            #EPS (earnings per share (in cents))
            temp = snippet.find(attrs={'data-test':'EPS_RATIO-value'})
            if Stock.check_str(temp.text):
                self.EPS = temp.text

            #PE (price-earning ratio)
            temp = snippet.find(attrs={'data-test':'PE_RATIO-value'})
            if Stock.check_str(temp.text):
                self.PE = temp.text
      
            #divy (dividend yield (in %))
            temp = snippet.find(attrs={'data-test':'DIVIDEND_AND_YIELD-value'})
            temp = temp.text
            temp_divy = temp[temp.find('(')+1:temp.find(')')]
            if Stock.check_str(temp_divy):
                #take out the % sign
                self.Divy = re.sub('%', '', temp_divy)
       
            #div (total dividend (in cents) past 12 months)
            temp_div = temp[0:temp.find('(')-1]
            if Stock.check_str(temp_div):    
                self.Div = temp_div

            #1range (daily low and high)
            temp = snippet.find(attrs={'data-test':'DAYS_RANGE-value'})
            if Stock.check_str(temp.text):
                temp = re.split('-', temp.text, 1)
                self.Low1 = (temp[0]).strip()
                self.High1 = (temp[1]).strip()
            else:
                self.Low1 = 'N/A'
                self.High1 = 'N/A'
                
            #52range (yearly low and high)
            temp = snippet.find(attrs={'data-test':'FIFTY_TWO_WK_RANGE-value'})
            if Stock.check_str(temp.text):
                temp = re.split('-', temp.text, 1)
                self.Low52 = (temp[0]).strip()
                self.High52 = (temp[1]).strip()
            else:
                self.Low52 = 'N/A'
                self.High52 = 'N/A'

            #Vol (average volume in a year (in unit stock))
            temp = snippet.find(attrs={'data-test':'AVERAGE_VOLUME_3MONTH-value'})
            if Stock.check_str(temp.text):
                self.Vol = temp.text

            #Cap (market capitalization (in SGD))
            temp = snippet.find(attrs={'data-test':'MARKET_CAP-value'})
            if Stock.check_str(temp.text):
                self.Cap = temp.text
                
    #@staticmethod
    def check_str(to_check):

        if(re.search(r'\d', to_check) is not None):
            return True

for j in range(0, len(listings.index)):
    #print to see the which listing is being scrapred currently
    #this is done to track progress
    print(j+1)
    stock_name = listings.iat[j, 0]
    stock_code = listings.iat[j, 1]
    stock_name_code = stock_name+' ('+stock_code+')'

    
    astock = Stock(stock_name_code)
    astock.scrape_and_assign(stock_code)

    #assigning the data vector for storage
    data = [*(vars(astock).values())]
    #data[0] is the com_name with code, #data[1:] are financial info
    temp_dict[data[0]] = data[1:]

    #delete the instance
    del astock

#save the dictionary to a panda dataframe
pdtable = pd.DataFrame.from_dict(temp_dict, orient='index', columns=\
                       ['Divy', 'Div', 'Price', 'Low1', 'High1', 'Low52', 'High52', 'EPS', 'PE', 'Vol', 'Cap'])

print(pdtable)

#save the data in different formats
pdtable.to_csv('sgx_prices.csv')
pdtable.to_excel('sgx_prices.xls', sheet_name='Stocks')
pdtable.to_hdf('sgx_prices.h5', key='df', mode='w')
pdtable.to_pickle('sgx_prices.pkl')

