from IPython import embed
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
import csv
import itertools
from datetime import datetime
import re

print ("*********** IMPORTS COMPLETED **********")

driver = webdriver.Chrome('chromedriver.exe')

driver.get("https://www.ser-ag.com/de/resources/notifications-market-participants/management-transactions.html#/")
print ("#########################################################")
print(driver.title)
time.sleep(1.5) # wait 5 seconds until DOM will load completly

print ("#########################################################")
Title = driver.find_element_by_class_name('ArticleTitle')
print ("#########################################################")
print (Title)

data = []

#cycle through navigation
max_page_num = 130
for i in range(max_page_num):
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    results = driver.find_elements_by_class_name('rt-tr')

    content = [x.text for x in driver.find_elements_by_class_name('rt-tr')]  # list
    time.sleep(1)

    print(content) # unformated print

    data.append(content)
    #print(data) # growing content

    driver.execute_script("window.scrollTo(0, 1800);")
    print("------------->  Scroll done")
    time.sleep(1.2)
    #embed()
    next = driver.find_elements_by_class_name('last')
    next[0].click()
    time.sleep(1.2)
    print("------------->  This page is done")

df = pd.DataFrame(data)
df = np.transpose(df)


format_data = []

for i in range(max_page_num):
    format_data.append(df[i].str.split('\n')) # , ignore_index=True not an opption

flatten = list(itertools.chain(*format_data))
flatten_df = pd.DataFrame(flatten)
flatten_df.columns = flatten_df.iloc[0] # get header right
flatten_df = flatten_df[flatten_df.EMITTENT != 'EMITTENT'] # drop all rows with heading names as values
flatten_df = flatten_df.dropna(subset=['EMITTENT']) # drop all rows that are empty, i.e. dopn't have the emittent
flatten_df['WERT'] = flatten_df['WERT'].str.replace("CHF ","", case = False) # remove CHF
flatten_df['WERT'] = flatten_df['WERT'].str.replace("'","", case = False) # remove ' for thousands (could be one operation)
flatten_df['GESAMTZAHL DER RECHTE'] = flatten_df['GESAMTZAHL DER RECHTE'].str.replace("'","", case = False) # remove ' for thousands

print ("*********** RESULTS **********")
print (flatten_df)
flatten_df.to_csv("InsiderTrades_"+datetime.now().strftime("%Y%m%d-%H%M%S")+".csv")


embed()

