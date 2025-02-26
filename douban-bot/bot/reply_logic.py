from bot.douban_api import get_douban_messages, send_douban_reply
from bot.gpt_api import generate_reply

def process_messages():
    """ 处理所有未读消息并回复 """
    messages = get_douban_messages()
    if messages:
        for msg in messages['messages']:
            user_id = msg['sender']['id']
            content = msg['text']
            reply = generate_reply(content)
            send_douban_reply(user_id, reply)
