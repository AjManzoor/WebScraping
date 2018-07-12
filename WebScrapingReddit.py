import selenium.webdriver as webdriver
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
import sys
import string

def clean_string(text):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    clean_reddit_item = text
    clean_reddit_item = clean_reddit_item.translate(non_bmp_map)
    table = str.maketrans({key: None for key in string.punctuation})
    clean_reddit_item = clean_reddit_item.translate(table)
    clean_reddit_item = clean_reddit_item.lower()
    return clean_reddit_item

    
def get_results():

    
    all_results = []
    new_url = "https://www.old.reddit.com/r/StarWars"
    browser = webdriver.Firefox()
    browser.get(new_url)
    time.sleep(2)
    for x in range(0,10):
        reddit_items = browser.find_elements_by_class_name("title.may-blank ")
        for reddit_item in reddit_items:
            clean_text = clean_string(reddit_item.text)
            all_results.append(clean_text) 
        elem = browser.find_element_by_xpath('.//span[@class = "next-button"]//a')
        elem.click()
        
    browser.close()
    os.system("taskkill /im geckodriver.exe")

    return (all_results)


print(get_results())



    
