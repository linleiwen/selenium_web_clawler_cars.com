
# coding: utf-8

from selenium import webdriver
import os
from selenium.webdriver.common.by import By
driverLocation = "C:\\Users\leiwen\workspace\libs\chromedriver.exe"
import pandas as pd
import numpy as np
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import datetime as dt
from selenium.webdriver.support.select import Select
        
        
class leiwen_clawler(object):
    
    def __init__(self,
        body_style = "SUV",
        condition = "Used Cars",
        max_price = "$30,000",
        zip_code= 22202,
        distance = "100",
        year = "2008"):
        self.body_style = body_style
        self.condition = condition
        self.max_price = max_price
        self.zip_code= zip_code
        self.distance = distance
        self.year = year
        
    def test(self):      
        def mile_find(obj):
                    
                    obj["self.year"]=self.year
                    try:
                        obj["mile"] = obj["object"].find_element_by_xpath(".//span[contains(@class,'listing-row__mileage')]").text
                    except:
                        obj["mile"] = "unknown"
                        
                    try:
                        obj["name"] = obj["object"].find_element_by_xpath(".//h2[contains(@class,'cui-delta listing-row__title')]").text
                    except:
                        obj["name"] = "unknown"
                
                    try:
                        obj["price"] = obj["object"].find_element_by_xpath(".//span[contains(@class,'listing-row__price')]").text
                    except:
                        obj["price"] = "unknown" 
                
                    try:
                        obj["hyperlink"] = obj["object"].find_element_by_xpath(".//a").get_attribute('href')
                    except:
                        obj["hyperlink"] = "unknown"
                
                    try:
                        obj["deal_qualilty"] = obj["object"].find_element_by_xpath(".//div[contains(@class,'listing-row__price-badge-arrow')]//span").text
                    except:
                        obj["deal_qualilty"] = "NOT A GOOD DEAL"
                
                    try:
                        attributes = obj["object"].find_elements_by_xpath(".//ul[contains(@class,'listing-row__meta')]//li")
                        attribute = str()
                        for i in attributes:
                            attribute = attribute+ "," + i.text
                            obj["other_attributes"] = attribute[1:]
                    except:
                        obj["other_attributes"] = "unknown"
                    return obj
        


        
        # # internal variables
        
        # In[4]:
        
        
        baseUrl = "https://www.cars.com/"
        driver = webdriver.Chrome(driverLocation)
        driver.get(baseUrl)
        driver.maximize_window()
        
        
        # In[5]:
        
        
        wait = WebDriverWait(driver, 20, poll_frequency=1,
                                     ignored_exceptions=[NoSuchElementException,
                                                         ElementNotVisibleException,
                                                         ElementNotSelectableException])
        
        
        # In[6]:
        
        
        data = pd.DataFrame()
        total = 0
        page_count = 1
        
        
        # # click and send key
        
        # In[7]:
        
        
        cursor = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='search-by-body-style-tab']/label")))
        cursor.click()
        
        
        # In[8]:
        
        
        bsid = driver.find_element_by_xpath("//select[contains(@name,'bsId')]")
        sel_id = Select(bsid)
        sel_id.select_by_visible_text(self.body_style)
        
        
        # In[9]:
        
        
        co = driver.find_element_by_xpath("//select[contains(@name,'stockType')]")
        sel_co = Select(co)
        sel_co.select_by_visible_text(self.condition)
        
        
        # In[10]:
        
        
        max_ = driver.find_element_by_xpath("//select[contains(@name,'prMx')]")
        sel_max = Select(max_)
        sel_max.select_by_visible_text(self.max_price)
        
        
        # In[11]:
        
        
        dis = driver.find_element_by_xpath("//select[contains(@name,'rd')]")
        dis = Select(dis)
        dis.select_by_value(self.distance)
        
        
        # In[12]:
        
        
        zip_c = driver.find_element_by_xpath("//input[contains(@id,'zip')]")
        zip_c.clear()
        zip_c.send_keys(self.zip_code)
        
        
        # In[13]:
        
        
        search = driver.find_element_by_xpath("//input[contains(@value,'Search')]")
        search.click()
        
        
        # # landing search page now!
        
        # In[14]:
        
        
        driver.implicitly_wait(3)
        
        
        # In[15]:
        
        
        driver.execute_script("window.scrollTo(0, 50000)") 
        page_show = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body//cui-page-result-count//select")))
        Select(page_show).select_by_value("100")
        
        
        # In[16]:
        
        
        driver.implicitly_wait(3)
        
        
        # In[17]:
        
        
        self.year1 = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='srpFilters']/ul/li[3]/div[2]/div[2]/select")))
        self.year1 = Select(self.year1)
        self.year1.select_by_visible_text(self.year)
        
        
        # In[18]:
        
        
        time.sleep(3)
        
        
        # In[19]:
        
        
        self.year2 = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='srpFilters']/ul/li[3]/div[2]/div[1]/select")))
        self.year2 = Select(self.year2)
        self.year2.select_by_visible_text(self.year)
        
        
        # # anchor tag disable:https://github.com/angular/protractor/issues/577
        
        # In[ ]:
        
        
        wait = WebDriverWait(driver, 30, poll_frequency=1,
                                     ignored_exceptions=[NoSuchElementException,
                                                         ElementNotVisibleException,
                                                         ElementNotSelectableException])
        
        
        # In[ ]:
        
        
        while(True):
            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div//div[@class='listing-row__details']")))
            temp = pd.DataFrame({'object':elements})
            length = len(elements)
            print("there are "+str(length) + " records in page "+ str(page_count)+" time:" + str(dt.datetime.now()))
            next = driver.find_element_by_xpath("//a[contains(text(),'Next')]")
            
            temp = temp.apply(lambda x : mile_find(x),axis = 1).iloc[:,1:]
            data = pd.concat([data,temp],axis = 0,ignore_index = True)
            total = total + length
            if next.get_attribute('disabled') == None:
                driver.execute_script("window.scrollTo(0, 50000)") 
                next.click()
                page_count = page_count +1
            else: 
                break
        
        
        # In[ ]:
        
        
        data
        
        
        # In[ ]:
        
        
        print("there are "+str(total) + " in total")
        
        
        # In[ ]:
        
        
        data.to_csv(str(self.body_style)+" " +str(self.zip_code) +" "+ "less than " +str(self.distance) +" miles"+str(self.year) +" self.year.csv",index = False)

#demo = leiwen_clawler()
#demo.test()
