from steam_logger import *

class Inv_calculator(Steam_logger): 
    def go_to_inventory(user):
        driver = user.driver
        driver.find_elements(By.XPATH, "//a[@data-tooltip-content='.submenu_username']")[1].click()
        sleep(3)
        driver.find_element(By.XPATH, "//img[@src='https://community.cloudflare.steamstatic.com/public/images/skin_1/iconInventory.png']").click()

    def set_game(user, game):
        driver = user.driver
        driver.find_element(By.XPATH, f'//*[text()="{game}"]').click()

    def set_marketable_items(user):
        driver = user.driver
        driver.find_element(By.ID, "filter_tag_show").click()
        sleep(5)
        driver.find_element(By.CSS_SELECTOR, "input[tag_name=marketable]").click()
        sleep(3)

    def get_number_of_items(user, game) -> int:
        number_of_items = user.driver.find_element(By.XPATH, f"//span[text()='{game}']/following-sibling::span").text.strip('()')

        return number_of_items

    def select_item(user, number_of_items: int):
        item_list=user.driver.find_elements(By.CLASS_NAME, "inventory_item_link")
        item_list[number_of_items].click()
        sleep(5)

    def open_all_items(user):
        counter = 0
        number_of_items = user.get_number_of_items("Dota 2")
        total_price = 0
        for item in range(number_of_items):
           try:
              user.select_item(item)
              counter+=1

              name = user.get_item_name()
              price = user.get_item_price()
              total_price += price

              if(count + 1 % 25 == 0) and (count != 0):
                  user.driver.find_element(By.ID, 'pagebtn_next').click()
                  sleep(2)

           except ElementNotInteractableException:
               continue

    def get_item_name(user) -> str:
          names = user.driver.find_elements(By.CLASS_NAME, "hover_item_name")

          if names[0].is_displayed():
              name = names[0].text
          else:
              name = names[1].text

          return name

    def get_item_price(user) -> float:
        prices = user.driver.find_elements(By.XPATH, "//div[@style='min-height: 3em; margin-left:1em;']")

        if prices[0].is_displayed():
            price = prices[0].text.replace(',','.').split()[1]
        else:
            price = prices[1].text.replace(',','.').split()[1]

        sleep(5)

        return float(price)

inventory = Inv_calculator()
inventory.steam_login()
inventory.go_to_inventory()
inventory.set_game("Dota 2")
inventory.set_marketable_items()
inventory.open_all_items()
          




        


