import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver

#the main url
url = 'https://sginvestors.io/sgx/stock-listing/alpha#stocklist-j'

#the dictionary to be stored into the panda dataframe
temp_dict = dict()

#open the url
driver = webdriver.Firefox(executable_path=r'C:\your_path_here\geckodriver.exe')
driver.get(url)

html = driver.page_source
html = BeautifulSoup(html, 'lxml')

#find the company name and code
for entry in html.find_all(['span'], {'itemprop':['alternateName', 'name']}):
    match = re.search(r'name', str(entry))
    if match:
        #filter out the web label found    
        if entry.text != 'SGinvestors.io':
            temp_name = entry.text
    match = re.search(r'alternateName', str(entry))

    #the name is in the following format SGX: AAA, +2 extracts the letter after the space
    if match:
        temp_dict[temp_name] = entry.text[(entry.text).find(':')+2:]

#save the dictionary to a panda dataframe
pdtable = pd.DataFrame.from_dict(temp_dict, orient='index', columns=['Code'])

print(pdtable)

#terminate the browser            
os.system('tskill plugin-container')
driver.close()
driver.quit()

#save the data in different formats
pdtable.to_csv('sgx_listings.csv')
pdtable.to_excel('sgx_listings.xls', sheet_name='Stocks')
pdtable.to_hdf('sgx_listings.h5', key='df', mode='w')
pdtable.to_pickle('sgx_listings.pkl')

