import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from steam_logger import *
from Inventory_calculator import *
from skins_db import *
from price_parser import *
from fv_compare import *

bot  = telebot.TeleBot("token")

data = []


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hi, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id,mess,parse_mode='html')
    remove = telebot.types.ReplyKeyboardRemove()
    mess = "/start - start_bot \n/steam_balance - calculate my steam balance \n/calculate_inventory_price - calculate my inventory price \n/add_item_to_parse - add new item to parse list \n/get_parsed_items - get all parsed items in message \n/parse_price - parse prices of all added items \n/send_parsed_items - to get parse prices in markups"
    bot.send_message(message.chat.id,mess,parse_mode='html', reply_markup = remove )
    
    
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
     if os.path.exists("skins.txt"):
         data = db.read_items()
         for i in range(0, len(data)):
             keyboard.add(InlineKeyboardButton(text = f'{data[i]}', callback_data = f'data {data[i]}'))
             #bot.send_message(message.chat.id,'Try :',reply_markup = keyboard)
     else :
         bot.send_message(message.chat.id,"No skins in database :(",parse_mode='html')
     
     bot.send_message(message.chat.id,'Your saved items :',reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: call.data.startswith('data'))
def answer(call):
   data = db.read_items()

   for i in range(0, len(data)):
       if call.data == f'data {data[i]}':
          print("da")
          skin_price = parser.get_markup_price(i)
          bot.send_message(call.message.chat.id,skin_price)
          
       else:
           print("nie")


@bot.message_handler(commands=['send_my_inventory'])
def send_markups(message):
     keyboard = InlineKeyboardMarkup()
     keyboard.row_width = 2
     if os.path.exists("inventory.txt"):
         data = db.read_inventory_item()
         for i in range(0, len(data)):
             if "https" in data[i]:
                continue
             data[i] = data[i].replace(" ", "")
             data[i] = data[i][0:20]   #max 20 elements in markup
             keyboard.add(InlineKeyboardButton(text = f'{data[i]}', callback_data = f'inventory_data {data[i]}'))
             
             #bot.send_message(message.chat.id,'Try :',reply_markup = keyboard)
     else :
         bot.send_message(message.chat.id,"No skins in database :(",parse_mode='html')
     #print(len('keyboard'.encode('utf-8')))
     bot.send_message(message.chat.id,'Your inventory items :',reply_markup = keyboard)

@bot.callback_query_handler(func = lambda call: call.data.startswith('inventory_data'))
def answer(call):
   data = db.read_inventory_item()

   for i in range(0, len(data)):
       if call.data == f'inventory_data {data[i]}':
          print("das")
          skin_price = parser.get_InvItem_price(data[i],data[i + 1])
          i = i + 1
          bot.send_message(call.message.chat.id,skin_price)
       else:
           print("nie")

           
@bot.message_handler(commands=['add_item_to_parse'])
def add_skin(message):
    request = bot.send_message(message.chat.id,'Send name :')
    bot.register_next_step_handler(request, user_answer)

def user_answer(message):
    bot.send_message(message.chat.id,f'Your input :{message.text}')
    #data.append(f'{message.text}')
    db.add_new_item(f'{message.text}')
 
    
@bot.message_handler(commands=['get_parsed_items'])
def send_array(message):
   if os.path.exists("skins.txt"):
         data = db.read_items()
   else:
       return bot.send_message(message.chat.id,"No skins in database :(",parse_mode='html')
   
   for i in data:
     bot.send_message(message.chat.id,i)


@bot.message_handler(commands=['parse_price'])
def get_price(message):
   if os.path.exists("skins.txt"):
         data = db.read_items()
   else:
       return bot.send_message(message.chat.id,"No skins in database :(",parse_mode='html')
   
   for i in range(0, len(data)):
     all_skins_price = parser.get_markup_price(i)
     bot.send_message(message.chat.id,all_skins_price)
 
     
@bot.message_handler(commands=['get_my_lisings_prices'])
def get_market_listings(message):
    user_listings = get_listings()
    bot.send_message(message.chat.id,f'Your steam community listings: {user_listings}')
fv_data = [] #hyita 
@bot.message_handler(commands=['float_parser'])
def parse_my_item(message):
    request = bot.send_message(message.chat.id,'Send item name :')
    bot.register_next_step_handler(request, fv_item_answer)
    
def fv_item_answer(message):
    fv_data.append(message.text)
    request = bot.send_message(message.chat.id,'Send item max fv :')
    bot.register_next_step_handler(request, fv_max_answer)
    
def fv_max_answer(message):
    fv_data.append(message.text)
    fv_result = compare_fv(fv_data[1],fv_data[0])
    bot.send_message(message.chat.id,f'Found {len(fv_result)} items {fv_data[0]} with floats :\n {fv_result}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn = types.KeyboardButton("/async_on")
    markup.add(btn)
    bot.send_message(message.chat.id, text="Click '/async_on' to turn on parsing for this item .".format(message.from_user), reply_markup=markup)
    #fv_data.clear() #chistka huity 
       

async def async_fv_parse(message):
    while True:
        fv_max_answer(message)
        await asyncio.sleep(10)
        


async def async_fv_main(message):
    if len(fv_data) > 1 :
        ask = asyncio.create_task(async_fv_parse(message))
        await ask
@bot.message_handler(commands=['async_on'])   
def funy(message):
    
    asyncio.run(async_fv_main(message))

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

