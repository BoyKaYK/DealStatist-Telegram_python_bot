from steam_logger import *
market_link = 'https://steamcommunity.com/market/'
class Inv_calculator(Steam_logger): 
    def go_to_inventory(user):
        driver = user.driver
        driver.find_elements(By.XPATH, "//a[@data-tooltip-content='.submenu_username']")[1].click()
        sleep(3)
        driver.find_element(By.XPATH, "//img[@src='https://community.cloudflare.steamstatic.com/public/images/skin_1/iconInventory.png']").click()
        #user.save_cookie()

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

        return int(number_of_items)

    def select_item(user, number_of_items: int):
        item_list=user.driver.find_elements(By.CLASS_NAME, "inventory_item_link")
        item_list[number_of_items].click()
        sleep(5)

    def open_all_items(user) -> float:
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
              print(total_price)
              if(counter + 1 % 25 == 0) and (counter != 0):
                  user.driver.find_element(By.ID, 'pagebtn_next').click()
                  sleep(2)
              return float(total_price)

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
        prices = user.driver.find_elements(By.XPATH, "//div[@style='min-height: 3em; margin-left: 1em;']")

        if prices[0].is_displayed():
            price = prices[0].text.replace(',','.').split()[1]
            float_price = price.replace('₴','')
        else:
            price = prices[1].text.replace(',','.').split()[1]
            float_price = price.replace('₴','')
        sleep(5)

        return float(float_price)

    def get_balance(user) -> str:
        str_balance = user.driver.find_element(By.XPATH, "//*[@id='header_wallet_balance']").text
        
        #print(str(str_balance))
        return str(str_balance)
   
    def get_sell_listing(user):

        user.driver.get(market_link)
        sell_listing = user.driver.find_elements(By.CLASS_NAME,"market_listing_price")
        size_of_list = len(sell_listing)
        item_on_sale = sell_listing
        for i in range(size_of_list):
            item_on_sale[i] = sell_listing[i].text
            print(item_on_sale[i])
        return item_on_sale
       
inventory = Inv_calculator()

    
def calculate_my_inventory(game) -> float:
    inventory.steam_login()
    inventory.go_to_inventory()
    inventory.set_game(game)    
    inventory.set_marketable_items()
    total_price = inventory.open_all_items()
    return total_price


def get_steam_balance() -> str:
    inventory.steam_login()
    steam_balance = inventory.get_balance()
    return steam_balance


def get_listings():
    lists = inventory.get_sell_listing()
    return lists

#not connented with tg_bot
