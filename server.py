from main import telegram_chatbot
import pdb


main = telegram_chatbot("config.cfg")

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

            try:
                main.handler_message(from_, message)
            except KeyError:
                main.send_message(from_, main.comand_error)
                main.handler_message(from_, 'optiones')
