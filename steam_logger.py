from time import sleep

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
            user.driver(xpath)
            return True
        except NoSuchElementException:
            return False

    def steam_login(user) -> None:
        driver = user.driver
        driver.get(Link)
        driver.maximize_window()
        driver.implicitly_wait(5)


        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        sleep(2)


        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        sleep(2)

        driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        sleep(3)

        user.type_sg_code()

        

    def type_sg_code(user) -> None:
        if user.xpath_exists("//input[@id='twofactorcode_entry']"):
            code = input("CODE: ")
            user.driver.find_element(By.XPATH, "//input[@id='twofactorcode_entry']").send_keys(code)
            sleep(2)
            user.driver.find_element(By.CSS_SELECTOR, "div[type=submit]").click()
            sleep(2)
        else :
            sleep(5)


bot_Steam = Steam_logger()
bot_Steam.steam_login()



       

       



