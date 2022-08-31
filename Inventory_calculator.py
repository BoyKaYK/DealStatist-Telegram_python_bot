from steam_logger import *
from skins_db import *
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
        print(number_of_items)
        return int(number_of_items)

    def select_item(user, number_of_items: int):
        item_list=user.driver.find_elements(By.CLASS_NAME, "inventory_item_link")
        item_list[number_of_items].click()
        sleep(5)

    def open_all_items(user, game) -> float:
        counter = 0
        number_of_items = user.get_number_of_items(game)
        total_price = 0
        for item in range(number_of_items):
           try:
              user.select_item(item)
              counter+=1

              name = user.get_item_name()
              print(name)
              link = user.get_market_link()
              print(link)
              db.add_inventory_item(name,link)
              price = user.get_item_price()
              total_price += price
              print(total_price)
              if(counter + 1 % 25 == 0) and (counter != 0):
                  user.driver.find_element(By.ID, 'pagebtn_next').click()
                  sleep(2)
              

           except ElementNotInteractableException:
               continue
        return float(total_price)

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
   
    def get_sell_listing(user) -> str:

        user.driver.get(market_link)
        sell_listing = user.driver.find_elements(By.CLASS_NAME,"market_listing_price")
        size_of_list = len(sell_listing)
        item_on_sale = sell_listing
        for i in range(size_of_list):
            item_on_sale[i] = sell_listing[i].text
            print(item_on_sale[i])
            item_on_sale[i] = str(item_on_sale[i]).replace('\n', ' ')
        
        return str(item_on_sale)


    def get_my_inventory(user):
        inventory_list = db.read_inventory_item()
        return inventory_list
    
    def get_market_link(user):
        
        link = user.driver.find_element(By.XPATH, "//div[@style='height: 24px;']/a").get_attribute('href')
        #link = user.driver.find_element(By.PARTIAL_LINK_TEXT, "https://steamcommunity.com/market/listings").text.strip('()')
        return link



       
inventory = Inv_calculator()

    
def calculate_my_inventory(game) -> float:
    inventory.steam_login()
    inventory.go_to_inventory()
    inventory.set_game(game)    
    inventory.set_marketable_items()
    total_price = inventory.open_all_items(game)
    #inventory.close_browser()
    return total_price


def get_steam_balance() -> str:
    inventory.steam_login()
    steam_balance = inventory.get_balance()
    #inventory.close_browser()
    return steam_balance


def get_listings():
    inventory.steam_login()
    lists = inventory.get_sell_listing()
    #lists = lists.replace('\n', '')
   
    return lists



#inventory.steam_login()
#inventory.go_to_inventory()
#inventory.get_balance()
#print(get_listings())
#sleep(20)
#inventory.get_sell_listing()
#inventory.set_game("Dota 2")
#inventory.set_marketable_items()
#inventory.open_all_items()            
#inventory.save_cookie()
#inventory.close_browser()
          




        


