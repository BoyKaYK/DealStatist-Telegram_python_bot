import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import requests
import bs4
from bs4 import BeautifulSoup ,SoupStrainer

from steam_logger import *
from Inventory_calculator import *
 
bot  = telebot.TeleBot("token")

data = []


def get_markup_price(skin):
    url = f'https://steamcommunity.com/market/listings/730/{data[skin]}'
    get_page = requests.get(url)
    parser = BeautifulSoup(get_page.text,'html.parser')
    price = parser.find_all('span' ,class_='market_listing_price market_listing_price_with_fee' )
    parse_price = [c.text for c in price]
    clear_price = str(parse_price)
    clear_price = clear_price.replace('\\n', '')
    clear_price = clear_price.replace('\\t', '')
    clear_price = clear_price.replace('\\r', '')
    final_price_msg = f'{data[skin]} first 10 prices :\n{clear_price}'
    return final_price_msg



@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hi, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id,mess,parse_mode='html')
    mess = "/start - start_bot \n/steam_balance - calculate my steam balance \n/calculate_inventory_price - calculate my inventory price \n/add_item_to_parse - add new item to parse list \n/get_parsed_items - get all parsed items in message \n/parse_price - parse prices of all added items \n/send_parsed_items - to get parse prices in markups"
    bot.send_message(message.chat.id,mess,parse_mode='html')
    
@bot.message_handler(commands=['steam_balance'])
def get_balance(message):
    st_balance = get_steam_balance()
    mess = f'Your steam balance is : <b>{st_balance}</b>'
    bot.send_message(message.chat.id,mess,parse_mode='html')

@bot.message_handler(commands=['calculate_inventory_price'])
def inventory_price(message):
    request = bot.send_message(message.chat.id,'Send name of game :')
    bot.register_next_step_handler(request, user_game)
   

def user_game(message) -> str:
    bot.send_message(message.chat.id,f'Your game is: {message.text}')
    inventory_price=calculate_my_inventory(f'{message.text}')
    bot.send_message(message.chat.id,f'Your {message.text} inventory is : {inventory_price}')

@bot.message_handler(commands=['send_parsed_items'])
def send_markups(message):
     keyboard = InlineKeyboardMarkup()
     keyboard.row_width = 2
     for i in range(0, len(data)):
        
        keyboard.add(InlineKeyboardButton(text = f'{data[i]}', callback_data = f'data {data[i]}'))

     bot.send_message(message.chat.id,'Try :',reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
   for i in range(0, len(data)):
       if call.data == f'data {data[i]}':
          skin_price = get_markup_price(i)
          bot.send_message(call.message.chat.id,skin_price)
       
@bot.message_handler(commands=['add_item_to_parse'])
def add_skin(message):
    request = bot.send_message(message.chat.id,'Send name :')
    bot.register_next_step_handler(request, user_answer)

def user_answer(message):
    bot.send_message(message.chat.id,f'Your input :{message.text}')
    data.append(f'{message.text}')
    
@bot.message_handler(commands=['get_parsed_items'])
def send_array(message):
    for i in data:
     bot.send_message(message.chat.id,i)

@bot.message_handler(commands=['parse_price'])
def get_price(message):
   for i in data:
    url = f'https://steamcommunity.com/market/listings/730/{i}'
    get_page = requests.get(url)
    parser = BeautifulSoup(get_page.text,'html.parser')
    price = parser.find_all('span' ,class_='market_listing_price market_listing_price_with_fee' )
    parse_price = [c.text for c in price]
    clear_price = str(parse_price)
    clear_price = clear_price.replace('\\n', '')
    clear_price = clear_price.replace('\\t', '')
    clear_price = clear_price.replace('\\r', '')
    final_price_msg = f'{i} first 10 prices :\n{clear_price}'
    bot.send_message(message.chat.id,final_price_msg)
    


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "photo":
        mess = "Generating photo..."
        bot.send_message(message.chat.id,mess,parse_mode='html')
        photo = open('image.png', 'rb')
        bot.send_photo(message.chat.id ,photo)

    if message.text == "id":
        mess = f'Your ID: <b>{message.from_user.id}</b>'
        bot.send_message(message.chat.id,mess,parse_mode='html')
     
    else :
        mess = 'I dont understand you ! Use commands to use me :)'
        bot.send_message(message.chat.id,mess,parse_mode='html')

bot.polling(none_stop=True)

