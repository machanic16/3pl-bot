from main import telegram_chatbot

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
                main.send_prices(from_)
                break
            else if message == '🚚Destinos servidos🚛':
                main.send_cities_to_serve(from_)
            else if message == 'Contacto':
                main.send_contact_info(from_)
            main.send_reply_keyboard_markup(from_)