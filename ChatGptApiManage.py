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
        self.instruction = "-> 여기 부터 지시 사항이야 이 문장에서 내가 필요한 정보는 강아지 이름, 색상, 사는 곳, 나이, 품종 등이야 내가 활용할 수 있게 끔 출력을 줘, 그리고 난 이정보를 코딩하는데 사용할거니까 json 타입으로 활용할 수 있게끔 줘"

    def send_chatGpt_server(self, message):
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {
                    "role":"user",
                    "content": message + self.instruction}
            ]
        )
        return completion.choices[0].message


