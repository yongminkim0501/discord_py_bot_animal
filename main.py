from run_discord import *
from discord_main import *
from searching_data import *

import json
def connect_dog(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['api_token']
    return TOKEN

def main():    
    api_key = connect_dog("dog_token.json")
    api_url = "https://openapi.gg.go.kr/AbdmAnimalProtect"
    api = animalcheck(api_key, api_url)
    api.run() # 이 부분을 실행해야만 함

    searching_data_object = searching_data()
    searching_data_object.set_api(api)     # request 사용안하고 set을 통하여 연결

    discord_TOKEN = connect_discord("discord_token.json")
    discord_object = set_discord()
    discord_object.set_discord_bot()
    discord_object.start_client(discord_TOKEN)
#    check = api.search_SIGUN_NM("수원시")
#    get_to_frame_data = api.get_pandas_frame_data()
#    print(get_to_frame_data)
#    print(check)
'''
    test code
    check = api.search_SIGUN_NM("수원시")
    print(check)
    check_count_age = api.get_count_age()
    check_count_sex = api.get_count_sex()
    check_count_phone = api.get_count_CHRGPSN_CONTCT_NO()
    check_count_species = api.get_count_species()
    print(f"나이별 체크 : {check_count_age}")
    print(f"담당자 폰 번호 별 마리 수 : {check_count_phone}")
    print(f"성별 별 유기견 마리 수 : {check_count_sex}")
    print(f"종 별 유기견 마리 수 : {check_count_species}")
'''

if __name__ == '__main__':

    main() # 현재 100개씩 출력되므로 계속해서 출력하는 코드로 변경해야함.
