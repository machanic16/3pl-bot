from main import Telegram_chatbot
import pdb


main = Telegram_chatbot("config.cfg")

update_id = None

while True:
    updates = main.get_updates(offset=update_id)
    updates = updates["result"]
    status = 'ok'
    
    
    '''len(updates) = 1, mean that the user did not write anything yet
    if it is greater than 1, the user already write a message and the bot
    can now respond '''
    if len(updates) == 1 :
        
        try:
            status = updates[0]["my_chat_member"]["old_chat_member"]["status"]
            print(f"""status: {status}""")
            status = 'bad'
        except KeyError as k: 
            print(f"""{type(k)}: {k} 
                    updates[0]["my_chat_member"]["old_chat_member"]["status"] """)
    else:
        print("It should work")
    
    
    if updates and status != 'bad':
        item = updates[-1]
        update_id = item["update_id"]
        try:
            message = str(item["message"]["text"])
        except:
            message = ''
        try:
            from_ = item["message"]["from"]["id"]
        except:
            '''Here is the alternative key to find the id in case that 
            the bot receive another json as response '''
            from_ = item["my_chat_member"]["from"]["id"]
        try:
            #pdb.set_trace()
            print(f"""message from {updates[-1]['message']['from']['username']}: {message}
                user id : {updates[-1]['message']['from']['id']}""")
            main.handler_message(from_, message)
        except :
            main.send_message(from_, main.comand_error)
            main.handler_message(from_, 'optiones')
            print('User entered an invalid command')
                
    else:
        print('infinity loop')
        pass
