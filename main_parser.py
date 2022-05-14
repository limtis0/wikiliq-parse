import pandas as pd
import selenium.common.exceptions

from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup

import parse_product

from time import sleep

categories = [
    'Name',
    'Country',
    'Brand',
    'Categories',
    'Tasting Notes',
    'ABV',
    'Base Ingredient',
    'Years Aged',
    'Rating',
    'Rate Count',
    'Price',
    'Volume',
    'Description',
]

# Pandas config
brands = pd.read_csv('brands.csv')
df = pd.DataFrame(index=range(brands['product_count'].sum()), columns=categories)

# Selenium config
driver_path = 'chromedriver.exe'
brave_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

option = webdriver.ChromeOptions()
option.binary_location = brave_path

driver = webdriver.Chrome(driver_path, options=option)

item_count = 0
try:
    for link, count in zip(brands['href'], brands['product_count']):
        products = []
        driver.get(link)
        try:
            button = driver.find_element(By.CLASS_NAME, 'view-all')
            button.click()
            sleep(3)
        except selenium.common.exceptions.NoSuchElementException:
            pass

        while len(products) != count:
            if len(products) != 0:
                sleep(3)
            brand_page = BeautifulSoup(driver.page_source, 'html.parser')
            products = brand_page.findAll('a', class_='prod-card')

        for product in products:
            page = requests.get(product['href'])
            product_page = BeautifulSoup(page.text, 'lxml')

            info = {key: None for key in categories}
            for ind, val in parse_product.yield_data(product_page):
                info[ind] = val
            print(info)

            df.iloc[item_count] = info
            item_count += 1
except Exception as e:
    print(e)
    df.to_csv('emergency_save.csv')
    pass

print(df.head(5))
df.to_csv('data.csv')
