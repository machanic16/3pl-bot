# -*- coding: UTF8 -*-
import requests
import json
import configparser as cfg
import telebot
from telebot import types

""" markup = types.ReplyKeyboardMarkup()
markup.add('a', 'v', 'd')
tb.send_message(chat_id, message, reply_markup=markup)

# or add strings one row at a time:
markup = types.ReplyKeyboardMarkup()
markup.row('a', 'v')
markup.row('c', 'd', 'e')
tb.send_message(chat_id, message, reply_markup=markup) """


class telegram_chatbot():
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        self.tb = telebot.TeleBot(self.token)
    #bot keyboards
        self.keyboards = {
            'options': types.ReplyKeyboardMarkup(),
            'cities': types.ReplyKeyboardMarkup()
        }
        # Add buttons to the keyboard 'options'
        self.keyboards['options'].row('Precios 💰')
        self.keyboards['options'].row('🚚Destinos servidos🚛')
        self.keyboards['options'].row('Contacto')

        # Add buttons to the keyboar 'cities'
        self.keyboards['cities'].row('🏦Atlanta🏦')
        self.keyboards['cities'].row('🐊Orlando🐊')
        self.keyboards['cities'].row('🌴Miami🌴')
        self.keyboards['cities'].row('menu principal')

        self.options = types.ReplyKeyboardMarkup() 
        self.options.row('Precios 💰')
        self.options.row('🚚Destinos servidos🚛')
        self.options.row('Contacto')


        self.prices = {
            'Atlanta prices': '''*precios para Caracas, Valencia y Maracay*
                Caja extrasmall
                 10x12x15 : $24.5
                Caja small
                 12x12x16: $32.5
                Caja medium
                 16x18x18: $72.5
                Caja medium
                 15x16x22: $73.5
                Caja large
                 18x18x24: $108.5
                Caja extra
                 large 22x22x22: $146.5

                *precios para interior del pais*
                extra small
                 10x12x15: 26.50$
                small
                 12x12x16:34.50$
                medium
                 (16x18x18) :75.50$
                medium
                 Nueva  (15x16x22): 82.50$
                large
                 (18x18x24): 113.50$
                extra
                 large (22x22x22): 148.50$''',
            'Orlando prices' : 'tatatattat',
            'Miami prices': 'rarara'
        }
        
        

    greet = '''Hola! soy el bot de 3PL Express, espero poder ayudarle,
                vera en su teclado la informacion que le puedo facilitar'''

    places = 'Todo el territorio, excepto: Nueva Esparta, Amazonas y Bolivar '

    contact_info = '''https://www.instagram.com/3pl_express/
                3pl-express.com'''
    

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    
    def send_reply_keyboard_markup(self, chat_id, msg, keyboard ):
        self.tb.send_message(chat_id, msg, reply_markup= self.keyboards[keyboard])

    def send_message(self, msg, chat_id):
        self.tb.send_message(chat_id, msg)
    
    def send_prices(self, chat_id, prices):
        self.tb.send_message(chat_id, prices )
    
    def say_hi(self, chat_id, greeting=greet):
        self.tb.send_message(chat_id,greeting)

    def send_cities_to_serve(self,chat_id, places= places):
        self.tb.send_message(chat_id, places)

    def send_contact_info(self,chat_id, contact_info=contact_info):
        self.tb.send_message(chat_id, contact_info)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

    def precios_button_handler(self,chat_id):
        self.send_reply_keyboard_markup(chat_id,'Elija la ciudad de partida', 'cities')

    def menu_button_handler(self, chat_id, msg, keyboard):
        self.send_reply_keyboard_markup(chat_id, msg, keyboard)
    
    def atlanta_handler(self, msg, chat_id):
        self.send_message(msg,chat_id)

        
