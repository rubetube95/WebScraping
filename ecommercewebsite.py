from selenium import webdriver #selenium is a library used for browser-based automation/scraping
#for more on selenium - https://selenium-python.readthedocs.io/getting-started.html
from selenium.webdriver.common.keys import Keys #importing the Keys class allows you to use keys in the keyboard like RETURN, F1, ALT etc.
from webdriver_manager.chrome import ChromeDriverManager #importing module to help deploy chrome. 

import time #importing time class allows for you to pause before submitting a form/completing an action - makes the automation seem more human-like
from bs4 import BeautifulSoup # package for parsing HTML and XML documents. It creates a parse tree for parsed pages that can be used to extract data from HTML - super useful for web scraping
import csv 
import re
#regular expressions/regex - allows you do to a cntrl + F equivalent on code 
#sequence of characters that define a search pattern. Usually such patterns are used by string-searching algorithms 
# for "find" or "find and replace" operations on strings, or for input validation.
# used for matching text e.g. if the string has a number in it return age or address etc
#just google regular expressions and look at the images to get an idea. 

driver = webdriver.Chrome(ChromeDriverManager().install()) #This class is used to automatically search for and download the latest version of chrome 

driver.get("https://www.currys.ie/ieen/tv-and-home-entertainment/televisions/televisions/301_3002_30002_xx_xx/1_50/relevance-desc/xx-criteria.html")
#Calling the URL
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

def process_products(): #creating a method that will be callable later
    clean_product_list = []
    #python allows for both single and double inverted commas - both have the same function
    products = soup.find_all("article",{"class":"product result-prd"}) #calling the parent HTMl element/container from which the data resides
    
    for product in products: #basic for loop to go through all the child data in that container
        data_dict = {}
        desc = product.find("div",{"class":"desc"})
        #within the bracket above. The div is the outer element. That can be span, strong, article, a, etc.
        data_dict['product_brand']  = desc.find("span",{"data-product":"brand"}).text.strip()
        data_dict['product_name']   = desc.find("span",{"data-product":"name"}).text.strip()
        data_dict['product_price']  = desc.find("strong",{"class":"price"}).text.strip()
        data_dict['product_url']    = desc.find("a")["href"]   

        clean_product_list.append(data_dict)
    return clean_product_list

master_list = []

for i in range(2,6): #for loop that will cycle through each page of the 5 pages of products. Since the url above starts on page 1, we need this loop to start on page 2 (so we don't get duplicate date)
    print(i)
    driver.get(f"https://www.currys.ie/ieen/tv-and-home-entertainment/televisions/televisions/301_3002_30002_xx_xx/{i}_50/relevance-desc/xx-criteria.html")
    #please note the use of the letter 'f' before the URL above. Without it, the variable 'i' won't be recognised 
    html = driver.page_source
    clean_product_data = process_products()
    master_list.extend(clean_product_data)

import pandas as pd #panda allows for parsing of various file formats - in this case, exporting to CSV. One can also import
df = pd.DataFrame(master_list)
df.to_csv('PCWorld.csv')
