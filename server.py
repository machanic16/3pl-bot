from main import telegram_chatbot
import pdb
main = telegram_chatbot("config.cfg")


def make_reply(msg):
    reply = None
    if msg is not None:
        reply = 'okay'
    return reply

update_id = None
updates = main.get_updates(offset=update_id)
updates = updates["result"]
try:
    from_ = updates[0]["message"]["from"]["id"]
except:
    from_ = updates[0]["edited_message"]["from"]["id"]
main.say_hi(from_)
#pdb.set_trace()
while True:
    updates = main.get_updates(offset=update_id)
    updates = updates["result"]
    
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = 'no message'
            try:
                from_ = item["message"]["from"]["id"]
            except:
                from_ = item["edited_message"]["from"]["id"]
            if message == 'Precios 💰':
                main.precios_button_handler(from_)
                break
            elif message == 'menu principal':
                main.menu_button_handler(from_, 'En su teclado encontrara las opciones', 'options')
            elif message == '🚚Destinos servidos🚛':
                main.send_cities_to_serve(from_)
            elif message == '🏦Atlanta🏦':
                msg = main.prices['Atlanta prices']
                main.atlanta_handler( msg,from_)
                pass
            elif message == 'Contacto':
                main.send_contact_info(from_)
            if message.lower().capitalize() == 'Opciones':
                main.send_reply_keyboard_markup(from_, 'En su teclado encontrara las opciones', 'options')