import requests
from config.settings import DOUBAN_COOKIE

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": DOUBAN_COOKIE
}

def get_douban_messages():
    """ 获取最新的豆瓣私信 """
    url = "https://www.douban.com/j/msg/inbox"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else None

def send_douban_reply(user_id, message):
    """ 发送豆瓣私信 """
    url = "https://www.douban.com/j/msg/send"
    data = {"to": user_id, "text": message}
    response = requests.post(url, headers=HEADERS, data=data)
    return response.status_code == 200
