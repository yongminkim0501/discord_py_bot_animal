from openai import OpenAI
import json
from chatGptJsonMessage import *

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
        self.instruction = "-> 여기 부터 지시 사항, 다른 말 없이 json 타입과 동일하게 메시지를 나한테 보내줘, json type 속의 속성 순서는 1. sigun_nm, 2.species_nm, 3.color_nm, 4.sex_nm 이고 각각 의미하는 것은 sigun_nm은 살고있는 시군의 이름, species_nm은 견종 이름, color_nm은 강아지 색상, sex_nm은 성별 이름이야 수컷 또는 암컷으로 표시해줘, 이를 제외한 모든 부가적인 말 없이 json 형태로만 보내줘"

    def send_chatGpt_server(self, message):
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {
                    "role":"user",
                    "content": message + self.instruction}
            ]
        )
        chatGptobject = ChatGptMessage()
        chatGptobject.get_message(completion.choices[0].message)

        '''
        예시 데이터 :
        ChatCompletionMessage(content='{\n  "sigun_nm": "강남구",\n  "species_nm": "포메라니안",\n  "color_nm": "갈색과 흰색",\n  "sex_nm": "수컷"\n}', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None)
        이렇게 전달됨
        '''
        '''
        print(f"completion data : {completion}")
        print(f"completion message data : {completion.choices[0].message}")
        '''
        return completion.choices[0].message


