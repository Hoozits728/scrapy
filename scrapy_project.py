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
for url in urls:
    browser.get(url)
    # some pages have a show all button you need to click
    try:
        show_all=browser.find_elements_by_link_text('Show All Products')
        show_all.click()
    # others do not and simply begin listing their products
    finally:
        while True: # loop until no more pages
            # some data can be found here with no need to visit the product page
            table=browser.find_element_by_id('sProdList')
            trs=table.find_elements_by_tag_name('tr')
            for tr in trs:
                try:
                    product_url=tr.find_element_by_class_name('productImage').find_element_by_tag_name('a').get_attribute('href')
                except:
                    product_url=''
                try:
                    brand_name=tr.find_element_by_class_name('productImage').find_element_by_tag_name('a').get_attribute('title')
                except:
                    brand_name=''
                try:
                    unit_price=tr.find_element_by_class_name('listPrice').find_element_by_class_name('hVal').value
                except:
                    unit_price=0
                try:
                    manufacturer=tr.find_element_by_class_name('description').find_element_by_class_name('hVal').value
                except:
                    manufacturer=''
                try:
                    manufacturer_part=tr.find_element_by_class_name('description').find_element_by_tag_name('a').get_attribute('title')
                except:
                    manufacturer_part=''
                # other info will come from the product page itself
                browser.get(product_url)
                overview_elements=browser.find_element_by_class_name('productOverview')
                divs=overview_elements.find_elements_by_tag_name('div')
                overview=''
                for div in divs:
                    overview += div.text + '\n'
                dds=browser.find_elements_by_tag_name('dd')
                product_information = {}
                for dd in dds:
                    key=dd.find_element_by_tag_name('a').find_attribute('href').split('?')[1].split(':')[0]
                    val=dd.find_element_by_tag_name('a').find_attribute('href').splite('?')[1].split(':')[1]
                    product_information.update({str(key) : str(val)})
                legislation=browser.get_element_by_id('pdpSection_ProductLegislation')
                dds=legislation.get_elements_by_tag_name('dd')
                cnt_dds=0
                for dd in dds:
                    if cn_dds == 1:
                        tariff=dd.text
                    elif cnt_dds == 0:
                        country=dd.text    
                    cnt_dds += 1
                technical_data=browser.find_element_by_id('technicalData')
                lis=technical_data.find_elements_by_tag_name('li')
                doc_files=''
                file_urls=''
                for li in lis:
                    doc_files += li.text + ' '            
                    file_urls += li.find_element_by_tag_name('a').get_attribute('href') + ' '        
                img_url=browser.find_element_by_id('productMainImage').get_attribute('src')
            trail=browser.find_element_by_id('breadcrumb')
            ul=trail.get_element_by_tag_name('ul')
            lis=ul.get_elements_by_tag_name('li')
            li_cnt=0
            trail_string=''
            for li in lis:
                if li_cnt < 3:
                    trail_string += trail_string + li.text + ' > '                
            # there might be many pages to get through
            try:
                next_page=browser.find_element_by_class_name('paginNext').find_element_by_tag_name('a')
                next_page.click()
            except:
                break # if no next page to click then we are done with this product
                                
browser.quit()    