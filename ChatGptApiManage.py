from openai import OpenAI
import json

def connect_chatGpt(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['chatGpt_token']
    return TOKEN

class gpt_object:
    def __init__(self,):
        self.token = connect_chatGpt("ChatGpt_token.json")
        self.client = OpenAI(
            api_key = self.token
        )

    def send_chatGpt_server(self, message):
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {
                    "role":"user",
                    "content": message}
            ]
        )
        return completion.choices[0].message


