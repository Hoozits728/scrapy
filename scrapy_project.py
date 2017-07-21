from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import math
import sys
import codecs
import time

# Block images (we don't need them), open Chrome and navigate to site
#path_to_extension = r'C:\Users\6410\Desktop\lightsquaresolutions\3.13.0_0'
chrome_options=webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs", prefs)
#chrome_options.add_argument('load-extension=' + path_to_extension)
browser=webdriver.Chrome("C:\Program Files (x86)\SeleniumWrapper\chromedriver.exe", chrome_options=chrome_options)
browser.get('http://uk.farnell.com//browse-for-products')

# get level one urls and store in list
level_ones=browser.find_elements_by_class_name('filterCategoryLevelOne')
urls=[]
for level_one in level_ones:
    a_tags=level_one.find_elements_by_tag_name('a')
    for a in a_tags:
        urls.append(a.get_attribute('href'))

#for testing purposes        
#for url in urls:
#    print url

# get level two urls and store in list
urls2=[]
for url in urls:
    browser.get(url)
    level_twos=browser.find_elements_by_class_name('filterCategoryLevelOne') # oddly still named level one
    for level_two in level_twos:
        a_tags=level_two.find_elements_by_tag_name('a')
        for a in a_tags:
            urls2.append(a.get_attribute('href'))
            
#for testing purposes
for url in urls2:
    print url
    

browser.quit()    