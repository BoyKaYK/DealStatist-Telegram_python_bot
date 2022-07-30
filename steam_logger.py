from time import sleep
import pickle
import os 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from data import *
Link = 'https://store.steampowered.com/login'

class Steam_logger:
    def __init__(user):
        user.username = USERNAME
        user.password = PASSWORD
        user.driver = webdriver.Chrome()

    def close_browser(user) -> None:
        user.driver.close()
        user.driver.quit()

    def xpath_exists(user,xpath) ->bool:
        try:
            user.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def steam_login(user) -> None:
        driver = user.driver
        driver.get(Link)
        driver.maximize_window()
        driver.implicitly_wait(5)

        if os.path.exists("cookie.pieckle"):
            user.load_cookie()
            user.driver.refresh()
            sleep(2)

        else:
            driver.find_element(By.NAME, "username").send_keys(USERNAME)
            sleep(2)

            driver.find_element(By.NAME, "password").send_keys(PASSWORD)
            sleep(2)

            driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
            sleep(3)
            user.type_sg_code()
            sleep(5)
            user.save_cookie()
  
    def save_cookie(user):
        with open("cookie.pieckle",'wb') as file:
            pickle.dump(user.driver.get_cookies(),file)

    def load_cookie(user):
        with open("cookie.pieckle", 'rb') as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            user.driver.add_cookie(cookie)

    def type_sg_code(user) -> None:
       
            code = input("CODE: ")
            user.driver.find_element(By.XPATH, "//input[@id='twofactorcode_entry']").send_keys(code)
            sleep(2)
            user.driver.find_element(By.CSS_SELECTOR, "div[type=submit]").click()
            sleep(2)
        


#bot_Steam = Steam_logger()
#bot_Steam.steam_login()


       

       



