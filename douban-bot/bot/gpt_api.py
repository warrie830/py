import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_reply(content):
    """ 使用 OpenAI GPT 生成回复 """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一个智能聊天机器人，负责回复豆瓣用户消息。"},
            {"role": "user", "content": content}
        ]
    )
    return response["choices"][0]["message"]["content"]
