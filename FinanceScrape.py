import pandas as pd
import re
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from math import nan as nan

#the main url
url = 'https://www.malaysiastock.biz/Listed-Companies.aspx'

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
        self.Low7 = nan
        self.High7 = nan
        self.Low52 = nan
        self.High52 = nan
        self.EPS = nan
        self.PE = nan
        self.ROE = nan
        self.NTA = nan
        self.Vol = nan
        self.Cap = nan

    def scrape_and_assign(self, com_code):

        #get the company info url by company code
        com_url = 'https://www.malaysiastock.biz/Corporate-Infomation.aspx?securityCode='
        com_url = com_url+str(com_code)
        
        #process the company info page source in beautiful soup
        html = requests.get(com_url)
        html = BeautifulSoup(html.text, 'lxml')

        #get the web snippet where the key financial info are stored
        snippet = BeautifulSoup(str(html.find_all('div', class_='roundCourner')), 'lxml')

        #assigning financial info        
        #price (last closing price (in MYR))
        temp = snippet.find(id='MainContent_lbQuoteLast')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.Price = temp

        #EPS (earnings per share (in cents))
        temp = snippet.find(id='MainContent_lbFinancialInfo_EPS')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.EPS = temp

        #PE (price-earning ratio)
        temp = snippet.find(id='MainContent_lbFinancialInfo_PE')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.PE = temp

        #ROE (return on equity (in %))
        temp = snippet.find(id='MainContent_lbFinancialInfo_ROE')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.ROE = temp

        #div (total dividend (in cents) past 12 months)
        temp = snippet.find(id='MainContent_lbFinancialInfo_Div')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.Div = temp

        #divy (dividend yield (in %))
        temp = snippet.find(id='MainContent_lbFinancialInfo_DY')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.Divy = temp

        #7range (weekly low and high)
        temp = snippet.find(id='MainContent_lb4WeeksRange')
        temp = re.split('-', temp.text, 1)
        self.Low7 = (temp[0]).strip()
        self.High7 = (temp[1]).strip()

        #52range (yearly low and high)
        temp = snippet.find(id='MainContent_lbYearRange')
        temp = re.split('-', temp.text, 1)
        self.Low52 = (temp[0]).strip()
        self.High52 = (temp[1]).strip()

        #NTA (net tangible assets (in MYR))
        temp = snippet.find(id='MainContent_lbFinancialInfo_NTA')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.NTA = temp

        #Vol (average volume in a year (in unit stock))
        temp = snippet.find(id='MainContent_lbAvgYearVol')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.Vol = temp

        #Cap (market capitalization (in MYR))
        temp = snippet.find(id='MainContent_lbFinancialInfo_Capital')
        temp = re.sub(r'[:*^\s]', '', temp.text)
        self.Cap = temp
        

        
#27 elements = 26 letters from the alphabets + 1 from 0-9   
for j in range(1, 28):

    text_to_click = 'td.filteringSelection:nth-child('+str(j)+') > a:nth-child(1)'

    driver = webdriver.Firefox(executable_path=r'C:\your_path_here\geckodriver.exe')
    driver.get(url)

    #an explicit wait for the click text to load
    element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, text_to_click)))

    #click on the popup 'continue' button to proceed if it appears
    try:
        driver.find_element_by_css_selector(text_to_click).click()

    except ElementClickInterceptedException:
        driver.find_element_by_css_selector('#pgjs-continue').click()
        driver.find_element_by_css_selector(text_to_click).click()
        

    #a company listing run from 2 (min) to 98 (max) by css_selector
    #some pages have listings less than 98, in that case use 'except' to break
    #the range is chosen to be 123, that is over 98 to ensure the code is robust
    #to accommodate for future listings
    for k in range(2, 123):
        try:
            #get company name
            temp = driver.find_element_by_css_selector('#MainContent_tStock > tbody:nth-child(1) > tr:nth-child('+str(k)+') > td:nth-child(1) > h3:nth-child(1) > a:nth-child(1)')
            temp = temp.get_attribute('innerText')
            com_name = temp.strip()

            #get company code from company name
            com_code = temp[temp.find("(")+1:temp.find(")")]

            #create a stock class instance
            astock = Stock(com_name)
            astock.scrape_and_assign(com_code)

            #assigning the data vector for storage
            data = [*(vars(astock).values())]
            #data[0] is the com_name with code, #data[1:] are financial info
            temp_dict[data[0]] = data[1:]

            #delete the instance
            del astock

        except NoSuchElementException:  
             break
            
    #terminate the browser            
    os.system('tskill plugin-container')
    driver.close()
    driver.quit()


#save the dictionary to a panda dataframe
pdtable = pd.DataFrame.from_dict(temp_dict, orient='index', columns=\
                       ['Divy', 'Div', 'Price', 'Low7', 'High7', 'Low52', 'High52', 'EPS', 'PE', 'ROE', 'NTA', 'Vol', 'Cap'])

print(pdtable)

#save the data in different formats
pdtable.to_csv('klse_prices.csv')
pdtable.to_excel('klse_prices.xls', sheet_name='Stocks')
pdtable.to_hdf('klse_prices.h5', key='df', mode='w')
pdtable.to_pickle('klse_prices.pkl')
