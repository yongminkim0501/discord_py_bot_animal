from openai import OpenAI
import json

def connect_chatGpt(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['chatGpt_token']
    return TOKEN

gpt_token = connect_chatGpt("ChatGpt_token.json")

client = OpenAI(
    api_key = gpt_token
)

completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages=[
        {
            "role":"user",
            "content":"강아지에 대해서 설명해줘"}
    ]
)

print(completion.choices[0].message)


