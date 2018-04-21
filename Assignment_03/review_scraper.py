# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 13:17:56 2018
@author: Nitin
"""


#a-section.celwidget
import random
import requests
#import csv
import json
import time
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import html
import json,re
from dateutil import parser as dateparser
from time import sleep

#Define URL:

url = """https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM"""

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'


headers = {'User-Agent': user_agent}
page = requests.get(url, headers = headers)
parser = html.fromstring(page.content)



#Chrome web driver for selenium

driver = webdriver.Chrome(executable_path=r'C:\Users\Nitin\Desktop\Desktop FOlder\chromedriver.exe')

#Accessing the url via selenium automated browser

driver.get(url)


#Sorting according to most recent and verified reviews
#review.find('a',{'class':'a-link-normal'}).text
time.sleep(random.randint(4,6))
sortby_dropdown = driver.find_element_by_xpath('//*[@id="a-autoid-4-announce"]').click()
time.sleep(random.randint(3,5))
sortby_recent = driver.find_element_by_xpath('//*[@id="sort-order-dropdown_1"]').click()
time.sleep(random.randint(1,5))
filterby_dropdown = driver.find_element_by_xpath('//*[@id="a-autoid-5-announce"]').click()
time.sleep(random.randint(1,3))
filterby_verified = driver.find_element_by_xpath('//*[@id="reviewer-type-dropdown_1"]').click()
time.sleep(random.randint(2, 5))


#Defining xpath

xpath_title   = './/a[@data-hook="review-title"]'
xpath_author  = './/a[@data-hook="review-author"]'
xpath_date    = './/span[@data-hook="review-date"]'
xpath_body    = './/span[@data-hook="review-body"]'

rating_list = []
title_list = []
author_list = []
date_list = []
body_list = []
helpful_list = []

page=0
while(page < 3):
        
    data_div = driver.find_element_by_id('cm_cr-review_list')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(data_html, "html5lib")
    for item in soup:
        rating_amazon = item.find_all('i', attrs={'data-hook': 'review-star-rating'})
        rating = [x.text.strip() for x in rating_amazon]
        rating_list.append(rating)
    
    title_amazon = driver.find_elements_by_xpath(xpath_title)
    title = [x.text for x in title_amazon]
    title_list.append(title)

    author_amazon  = driver.find_elements_by_xpath(xpath_author)
    author = [x.text for x in author_amazon]
    author_list.append(author)

    date_amazon = driver.find_elements_by_xpath(xpath_date)
    date = [x.text for x in date_amazon]
    date_list.append(date)

    body_amazon  = driver.find_elements_by_xpath(xpath_body)
    body = [x.text for x in body_amazon]
    body_list.append(body)

    time.sleep(random.randint(1,3))
    
    next_page = driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[8]/a').click()
        
    # Wait for browsing
    time.sleep(random.randint(1,3))
    page +=1;

page = 0
while (page < 84):
    time.sleep(random.randint(1, 5))
    data_div = driver.find_element_by_id('cm_cr-review_list')
    data_html = data_div.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(data_html, "html5lib")
    for item in soup:
        rating_amazon = item.find_all('i', attrs={'data-hook': 'review-star-rating'})
        rating = [x.text.strip() for x in rating_amazon]
        rating_list.append(rating)
    
    title_amazon = driver.find_elements_by_xpath(xpath_title)
    title = [x.text for x in title_amazon]
    title_list.append(title)

    author_amazon  = driver.find_elements_by_xpath(xpath_author)
    author = [x.text for x in author_amazon]
    author_list.append(author)

    date_amazon = driver.find_elements_by_xpath(xpath_date)
    date = [x.text for x in date_amazon]
    date_list.append(date)

    body_amazon  = driver.find_elements_by_xpath(xpath_body)
    body = [x.text for x in body_amazon]
    body_list.append(body)

    time.sleep(random.randint(1,3))
    
    next_page = driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[9]/a').click()
        
    # Wait for browsing
    time.sleep(random.randint(1,3))
    page +=1;
    
    
driver.close()

#Modifying data to import output to .json file
def magic(dumy):
    new_dumy = []
    super_dumy = []
    for i in dumy:
        #new_dumy.append(';'.join(i))
        new_dumy.append(';'.join(str(j) for j in i))
       # values = ','.join(str(v) for v in value_list)
           #new_dumy = ';'.join([str(i) for i in new_dumy])    
    super_dumy = ';'.join(new_dumy).split(';')
    return super_dumy


rating_list_new = magic(rating_list)
title_list_new = magic(title_list)
author_list_new = magic(author_list)
date_list_new = magic(date_list)
body_list_new = magic(body_list)


import pandas as pd

dic = {"rating": rating_list_new,
       "title": title_list_new,
       "author": author_list_new,
       "date": date_list_new,
       "body": body_list_new}


df = pd.DataFrame.from_dict(dic, orient='index')
df = df.T
df = df.drop(df.index[870:])

df.to_json('C:/Users/Nitin/Desktop/Desktop FOlder/Study Material/Semester 2/BIA 660/Assgnmnt/Assignment 3/reviews.json',lines=True,orient='records')
#df.to_csv('C:/Users/Nitin/Desktop/Desktop FOlder/Study Material/Semester 2/BIA 660/Assgnmnt/Assignment 3/reviews.csv')
print(df)
