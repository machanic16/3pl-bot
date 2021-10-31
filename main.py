# -*- coding: UTF8 -*-
import requests
import json
import configparser as cfg
# $ pip install pyTelegramBotAPI
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


class Telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        self.tb = telebot.TeleBot(self.token)
    # Comand error message:
        self.comand_error = 'Por favor utilice solo el teclado sugerido para indicar su mensaje'

    #bot keyboards
        self.keyboards = {
            'options': types.ReplyKeyboardMarkup(),
            'info' : types.ReplyKeyboardMarkup(),
            'cities': types.ReplyKeyboardMarkup()
        }
        # Add buttons to the keyboard 'options'
        self.keyboards['options'].row('Precios 💰')
        self.keyboards['options'].row('🚚Destinos servidos🚛')
        self.keyboards['options'].row('Informacion')

        # Add buttons to the keyboard 'info'
        self.keyboards['info'].row('Direcciones')
        self.keyboards['info'].row('¿Donde esta mi envio?')
        self.keyboards['info'].row('Contacto')
        self.keyboards['info'].row('menu principal')


        # Add buttons to the keyboard 'cities'
        self.keyboards['cities'].row('🏦Atlanta🏦')
        self.keyboards['cities'].row('🐊Orlando🐊')
        self.keyboards['cities'].row('🌴Miami🌴')
        self.keyboards['cities'].row('menu principal')

        # Commads dictionary
        self.commands ={
            'optiones': self.menu_button_handler,
            'Precios 💰': self.precios_button_handler,
            '🚚Destinos servidos🚛':self.send_cities_to_serve,
            'Informacion': self.show_info,
            'Contacto': self.send_contact_info,
            'menu principal': self.menu_button_handler,     
            '🏦Atlanta🏦':self.atlanta_handler,
            '🐊Orlando🐊':self.orlando_handler,
            '🌴Miami🌴':self.miami_handler,
            'Direcciones': self.send_addresses,
            '¿Donde esta mi envio?': self.show_traking_help          
        }

        # Prices in txt files to keep everything clean
        self.atlanta_prices = open("atlanta_prices.txt", "r")
        self.orlando_prices = open("orlando_prices.txt", "r")
        self.miami_prices = open("miami_prices.txt", "r")
        self.prices = {
            'Atlanta prices': self.atlanta_prices.read(),
            'Orlando prices' : self.orlando_prices.read(),
            'Miami prices': self.miami_prices.read()
        }
        
        
        

    greet = '''Hola! soy el bot de 3PL Express, espero poder ayudarle, \n vera en su teclado la informacion que le puedo facilitar'''

    places = 'Todo el territorio, excepto: Nueva Esparta, Amazonas y Delta Amacuro '

    contact_info = '''puede visitar nuestra pag web http://3pl-express.com/ \n o seguirnos en Instagram https://www.instagram.com/3pl_express/
                '''
    
    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        respuesta = json.loads(r.content)
        if respuesta["ok"] != True:
            print( f"{respuesta} Telegram se jodio")
        else:
            print(f'La respuesta es: {respuesta}')
            return respuesta

    def handler_message(self, chat_id, command):
        self.commands[command](chat_id)

    def send_reply_keyboard_markup(self, chat_id, msg, keyboard ):
        self.tb.send_message(chat_id, msg, reply_markup= self.keyboards[keyboard])

    def send_message(self, chat_id, msg):
        self.tb.send_message(chat_id, msg)
    

    def send_prices(self, chat_id, prices):
        self.tb.send_message(chat_id, prices )
    
    def say_hi(self, chat_id, greeting=greet):
        self.tb.send_message(chat_id,greeting)
    
    def send_cities_to_serve(self,chat_id, places= places):
        self.tb.send_message(chat_id, places)
    
    def show_info(self, chat_id):
        self.send_reply_keyboard_markup(chat_id,'Elija la informacion que desea', 'info')

    def send_contact_info(self,chat_id, contact_info=contact_info):
        self.tb.send_message(chat_id, contact_info)

    def precios_button_handler(self,chat_id):
        self.send_reply_keyboard_markup(chat_id,'Elija la ciudad de partida', 'cities')
    
    def menu_button_handler(self,chat_id,msg='En su teclado encontrara las opciones', keyboard='options'):
        self.send_reply_keyboard_markup(chat_id, msg, keyboard)
    
    def send_addresses(self, chat_id):
        msg = open('address.txt', 'r')
        self.send_message(chat_id,msg = msg.read())
    
    def show_traking_help(self, chat_id):
        msg = 'Dirijase a nuestra pagina web http://3pl-express.com e ingrese su numero de traking'
        self.send_message(chat_id, msg )

    # Cities buttons
    def atlanta_handler(self, chat_id):
        self.send_message(chat_id,msg= self.prices['Atlanta prices'])

    def orlando_handler(self, chat_id):
        self.send_message(chat_id,msg= self.prices['Orlando prices'])
    
    def miami_handler(self, chat_id):
        self.send_message(chat_id, msg= self.prices['Miami prices'])
