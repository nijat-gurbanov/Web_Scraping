# Download required libraries
from numpy import number
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import psutil

# Getting the start time of the program
total_start_time = time.time()

# Create a boolean variable for checking if the number of extracted pages are more 100
minrequirement = bool(True)

# Create an empty variable for counting the number of scraped pages
scraped_pages = 0

# BaseURL of Yahoo Finance website
URL = "https://finance.yahoo.com/"

# Start the Driver
driver = webdriver.Firefox()

# Hit the url of Yahoo Finance
driver.get(URL)

# Click on 'I agree' button
driver.find_element(by = By.XPATH, value = "//button[@value='agree']").click()

# Click Cryptocurrencies button to go to that section
driver.find_element(by = By.XPATH, value = "//a[@title='Cryptocurrencies']").click()

# Make the Driver wait untill the table of cryptocurrencies load
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "scr-res-table")))

# Web page fetched from driver is parsed using Beautiful Soup
LinkHTMLPage = BS(driver.page_source, 'html.parser')

# Add 1 to scraped_pages for all new scraped pages
scraped_pages += 1

# Table is searched using class and stored in another variable
Table = LinkHTMLPage.find('tbody')

# List of all the rows is store in a variable 'Rows'
Rows = Table.find_all('tr', class_=re.compile("^simpTblRow"))

# Create a blank list for storing the name of cryptocurrencies 
cryptos = []

# Store the name of cryptocurrencies from each row
for i in range(0, len(Rows)):
    # Store each element of Rows as Values
    Values = Rows[i].find_all('td')
    # Get the name of the cryptocurrencies
    RowValue = Values[1].text
    # Add the name to the cryptos table
    cryptos.append(RowValue)

    i = i + 1

# Click next button to load next 25 cryptocurrencies
driver.find_element(by = By.XPATH, value = "//button[@class='Va(m) H(20px) Bd(0) M(0) P(0) Fz(s) Pstart(10px) O(n):f Fw(500) C($linkColor)']").click()

# Make the Driver wait 3 seconds for loading new table
time.sleep(3)

# Repeat the same process untill we get the name of 100 cryptocurrencies
########################################################################
scraped_pages += 1
LinkHTMLPage = BS(driver.page_source, 'html.parser')
Table = LinkHTMLPage.find('tbody')
Rows = Table.find_all('tr', class_=re.compile("^simpTblRow"))
for i in range(0, len(Rows)):
    Values = Rows[i].find_all('td')
    RowValue = Values[1].text
    cryptos.append(RowValue)
    i = i + 1
driver.find_element(by = By.XPATH, value = "//button[@class='Va(m) H(20px) Bd(0) M(0) P(0) Fz(s) Pstart(10px) O(n):f Fw(500) C($linkColor)']").click()
time.sleep(3)
scraped_pages += 1
LinkHTMLPage = BS(driver.page_source, 'html.parser')
Table = LinkHTMLPage.find('tbody')
Rows = Table.find_all('tr', class_=re.compile("^simpTblRow"))
for i in range(0, len(Rows)):
    Values = Rows[i].find_all('td')
    RowValue = Values[1].text
    cryptos.append(RowValue)
    i = i + 1
driver.find_element(by = By.XPATH, value = "//button[@class='Va(m) H(20px) Bd(0) M(0) P(0) Fz(s) Pstart(10px) O(n):f Fw(500) C($linkColor)']").click()
time.sleep(3)
scraped_pages += 1
LinkHTMLPage = BS(driver.page_source, 'html.parser')
Table = LinkHTMLPage.find('tbody')
Rows = Table.find_all('tr', class_=re.compile("^simpTblRow"))
for i in range(0, len(Rows)):
    Values = Rows[i].find_all('td')
    RowValue = Values[1].text
    cryptos.append(RowValue)
    i = i + 1

crypto_end_time = time.time()
########################################################################################

# Create a blank list to store the details of cryptocurrencies
Table = []

# Empty list for storing RAM and CPU usage
cpu_details = psutil.cpu_percent(4)
ram_details = psutil.virtual_memory()[2]

# Create a blank list to store the time ofeach extraction
details_start_time = []
details_end_time = []



# Getting the details of cryptocurrencies and repeat the process untill we get the details of each cryptocurrencies
for i in range(len(cryptos)):
    # Getting the start time of each extraction
    details_start_time.append(time.time())
    
    # Enter name of cryptocurrency in searchbox
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "header-desktop-search-button")))
    driver.find_element(by = By.XPATH, value = "//input[@placeholder = 'Search for news, symbols or companies']").send_keys(cryptos[i])
    
    # Click on Search icon and wait for 2 seconds
    driver.find_element(by = By.XPATH, value = "//button[@id= 'header-desktop-search-button']").click()
    time.sleep(3)

    scraped_pages += 1

    # Web page fetched from driver is parsed using Beautiful Soup
    LinkHTMLPage = BS(driver.page_source, 'html.parser')

    # Empty dictionary to store data present in each row
    Elements = {}
    try:
        # Extract values, replace thousands seperator and store them in dictionary
        Elements["Name"] = LinkHTMLPage.find("h1", class_ = "D(ib) Fz(18px)").text
        Elements["Previous Close"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[0].text.replace(',', '')
        Elements["Open"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[1].text.replace(',', '')
        Elements["Day's Range"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[2].text.replace(',', '')
        Elements["52 Week Range"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[3].text.replace(',', '')
        Elements["Start Date"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[4].text.replace(',', '')
        Elements["Market Cap"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[6].text.replace(',', '')
        Elements["Circulating Supply"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[7].text.replace(',', '')
        Elements["Volume"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[9].text.replace(',', '')
        Elements["Volume (24hr)"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[10].text.replace(',', '')
        Elements["Volume (24hr) All Currencies"] = LinkHTMLPage.find_all("td", class_ = "Ta(end) Fw(600) Lh(14px)")[11].text.replace(',', '')
        
        # Add the dictionary to the Table variable
        Table.append(Elements)
    except:
        print("Row Number: " + str(i))
    
    finally:
        i+=1
        # Getting the end time of each extraction
        details_end_time.append(time.time())

# Close Driver
driver.close()

total_end_time = time.time()

# Create a Data Frame from our Table for further use
Table = pd.DataFrame(Table)

# Set a boolean value to determine if number of pages extracted are more than 100 or not
if scraped_pages <100: 
    minrequirement = bool(False)
else:
    minrequirement = bool(True)

# Print the Table
print(Table)

print("Scraped pages are more than 100: ", minrequirement)
print("Number of pages scraped: ", scraped_pages)
print("Total running time is %.2f seconds." % (total_end_time - total_start_time))
print("Extracting the name of cryptocurrencies take %.2f seconds." % (crypto_end_time - total_start_time))
print("CPU usage is %s%%; RAM usage is %s%%" %  (cpu_details, ram_details))

for i in range(len(cryptos)):
    print("Extraction time of page number %s is %.2f seconds." % (i+1, details_end_time[i] - details_start_time[i]))
#############################################################################################################################

# Simple analysis
Table['Open'] = pd.to_numeric(Table['Open'],errors = 'coerce')

Max_coin = Table.iloc[Table["Open"].idxmax(),0]
print(Max_coin, " has the maximum opening value in among 100 scraped cryptocurrencies")
Min_coin = Table.iloc[Table["Open"].idxmin(),0]
print(Min_coin, " has the minimum opening value in among 100 scraped cryptocurrencies")
