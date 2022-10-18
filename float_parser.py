import pickle
import os 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import requests
import bs4
from bs4 import BeautifulSoup ,SoupStrainer
import re
#from skins_db import *
#from Inventory_calculator import *
from time import sleep
#float_url = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M3857918122210629888A27080312015D9828099214580827419"


class Float_parser():
    def set_max_fv(user,max_value):
        user.max_float = max_value
        return user.max_float


    def get_reviev_link(user,url):
        float_links = []
        user.driver = webdriver.Chrome()
        user.driver.get(url)
        buttons = user.driver.find_elements(By.CLASS_NAME,"market_actionmenu_button")
        for btn in buttons:
            user.driver.execute_script("arguments[0].click();", btn)
            popup = user.driver.find_element(By.CSS_SELECTOR,"#market_action_popup_itemactions > a")
            href = popup.get_attribute('href')
            #print(href)
            float_links.append(href)
        return float_links
    
    def float_request(user,float_url):
        float_values = []
        for i in range(len(float_url)):
            #print(float_url[i])
            reqest_url = f'https://api.csgofloat.com/?url={float_url[i]}' 
            parse_session = requests.Session()
            get_page = parse_session.get(reqest_url)
            get_page.text
            parser = BeautifulSoup(get_page.text,'html.parser')
            parser = str(parser)
            parser = parser.split(",")
            for i in range(len(parser)): 
                if 'floatvalue' in parser[i]:
                    float_pos = i

            value = parser[float_pos].split(":")[1]
            print(str(value))
            #sleep(2)
            
            float_values.append(float(value))
        return float_values




def get_fv_list(url):
    float = Float_parser()
    float_url = float.get_reviev_link(url)
    return float.float_request(float_url)


