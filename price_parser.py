import requests
import bs4
from bs4 import BeautifulSoup ,SoupStrainer
from skins_db import *
from Inventory_calculator import *


class Price_parcer():
    def get_markup_price(user,skin):
        if os.path.exists("skins.txt"):
            data = db.read_items()
        else:
            return "No skins in database :("
        url = f'https://steamcommunity.com/market/listings/730/{data[skin]}'
        parse_session = requests.Session()
        if os.path.exists("cookie.pieckle"):
            for j in inventory.get_selenium_cookie():
                requests.utils.add_dict_to_cookiejar(parse_session.cookies, {j['name']: j['value']})
        else: print("no cookie file")

        get_page = parse_session.get(url)
        parser = BeautifulSoup(get_page.text,'html.parser')
        price = parser.find_all('span' ,class_='market_listing_price market_listing_price_with_fee' )
        parse_price = [c.text for c in price]
        clear_price = str(parse_price)
        clear_price = clear_price.replace('\\n', '')
        clear_price = clear_price.replace('\\t', '')
        clear_price = clear_price.replace('\\r', '')
        final_price_msg = f'{data[skin]} first 10 prices :\n{clear_price}'

        return final_price_msg
    
    def get_InvItem_price(user,skin,link):
        if os.path.exists("inventory.txt"):
            data = db.read_inventory_item()
        else:
            return "No skins in inventory database :("
        print(link)
        url = f'{link}'
        parse_session = requests.Session()
        if os.path.exists("cookie.pieckle"):
            for j in inventory.get_selenium_cookie():
                requests.utils.add_dict_to_cookiejar(parse_session.cookies, {j['name']: j['value']})
        else: print("no cookie file")
        get_page = parse_session.get(url)
        parser = BeautifulSoup(get_page.text,'html.parser')
        price = parser.find_all('span' ,class_='market_listing_price market_listing_price_with_fee' )
        parse_price = [c.text for c in price]
        clear_price = str(parse_price)
        clear_price = clear_price.replace('\\n', '')
        clear_price = clear_price.replace('\\t', '')
        clear_price = clear_price.replace('\\r', '')
        final_price_msg = f'{skin} first 10 prices :\n{clear_price}'
        return final_price_msg

parser = Price_parcer()
