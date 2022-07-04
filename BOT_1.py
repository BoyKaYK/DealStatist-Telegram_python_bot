import telebot
from telebot import types

import requests
import bs4
from bs4 import BeautifulSoup ,SoupStrainer


bot  = telebot.TeleBot("790266949:AAH5nSgi6Z-CymmNDQY0LRcQPB6mS48nadU")

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
    
    

@bot.message_handler(commands=['send'])
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
            

@bot.message_handler(commands=['add'])
def add_markups(message):
    request = bot.send_message(message.chat.id,'Send name :')
    bot.register_next_step_handler(request, user_answer)

def user_answer(message):
    bot.send_message(message.chat.id,f'Your input :{message.text}')
    data.append(f'{message.text}')
    
@bot.message_handler(commands=['get'])
def send_array(message):
    for i in data:
     bot.send_message(message.chat.id,i)

@bot.message_handler(commands=['price'])
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
        
bot.polling(none_stop=True)

