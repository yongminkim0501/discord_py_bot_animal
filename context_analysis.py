import requests
import json
from collections import defaultdict
import json
import urllib3
'''
나중에 개발을 위해 아껴두기, 사전 기반 형태소 처리 알고리즘 사용하려 했으나 갖고 있지 않은 견종
데이터가 생각보다 많아서 한계가 있다고 판단하여 chatgpt prompt를 이용한 처리를 하는 것으로
방향을 바꿈
'''
def connect_etri(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['etri_api_key']
    return TOKEN

etri_token = connect_etri("etri_token.json")

class Morpheme:
    def __init__(self, text, type_, count):
        self.text = text
        self.type = type_
        self.count = count

class NameEntity:
    def __init__(self, text, type_, count):
        self.text = text
        self.type = type_
        self.count = count

# 언어 분석 기술 문어/구어 중 한가지만 선택해 사용
# 언어 분석 기술(문어)
#open_api_url = "http://aiopen.etri.re.kr:8000/WiseNLU"
# 언어 분석 기술(구어)
open_api_url = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken"

access_key = etri_token  # 발급받은 API Key
analysis_code = "ner"  # 언어 분석 코드

# 분석할 텍스트 데이터
text = "전 우리 뽀삐를 찾고 싶어요 뽀삐는 저랑 15년을 살았구요." + \
    "뽀삐는 경기도 수원시 영통구 하동에서 살았어요." + \
    "뽀삐는 흰색이고 견종은 포메라니안이에요. 뒤쪽에 살짝 검정색의 긴 털이 나 있어요."
# 언어 분석 기술(구어) 텍스트
# text += "네 안녕하세요 홍길동 교숩니다"

request = {
    'argument': {
        'analysis_code': analysis_code,
        'text': text
    }
}

try:
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': access_key
    }
    
    # API 호출
    response = requests.post(open_api_url, headers=headers, data=json.dumps(request))
    
    # 응답 확인
    if response.status_code != 200:
        print(f"[error] {response.text}")
        exit()
    
    response_body = response.json()
    result = response_body.get('result')
    
    # 분석 요청 오류 시 처리
    if result != 0:
        print(f"[error] {result}")
        exit()
    
    # 분석 결과 활용
    return_object = response_body.get('return_object')
    sentences = return_object.get('sentence')
    
    morphemes_map = defaultdict(lambda: None)
    name_entities_map = defaultdict(lambda: None)
    
    for sentence in sentences:
        # 형태소 분석기 결과 수집 및 정렬
        morphological_analysis_result = sentence.get('morp', [])
        for morpheme_info in morphological_analysis_result:
            lemma = morpheme_info.get('lemma')
            morpheme = morphemes_map[lemma]
            if morpheme is None:
                morpheme = Morpheme(lemma, morpheme_info.get('type'), 1)
                morphemes_map[lemma] = morpheme
            else:
                morpheme.count += 1
        
        # 개체명 분석 결과 수집 및 정렬
        name_entity_recognition_result = sentence.get('NE', [])
        for name_entity_info in name_entity_recognition_result:
            name = name_entity_info.get('text')
            name_entity = name_entities_map[name]
            if name_entity is None:
                name_entity = NameEntity(name, name_entity_info.get('type'), 1)
                name_entities_map[name] = name_entity
            else:
                name_entity.count += 1
    
    morphemes = []
    if len(morphemes_map) > 0:
        morphemes = list(morphemes_map.values())
        morphemes.sort(key=lambda morpheme: morpheme.count, reverse=True)
    
    name_entities = []
    if len(name_entities_map) > 0:
        name_entities = list(name_entities_map.values())
        name_entities.sort(key=lambda name_entity: name_entity.count, reverse=True)
    
    # 형태소들 중 명사들에 대해서 많이 노출된 순으로 출력 (최대 5개)
    '''
    noun_count = 0
    for morpheme in morphemes:
        if morpheme.type in ["NNG", "NNP", "NNB"]:
            print(f"[명사] {morpheme.text} ({morpheme.count})")
            noun_count += 1
            if noun_count >= 5:
                break
    
    print("")'''
    
    # 형태소들 중 동사들에 대해서 많이 노출된 순으로 출력 (최대 5개)
    
    '''
    verb_count = 0
    for morpheme in morphemes:
        if morpheme.type == "VV":
            print(f"[동사] {morpheme.text} ({morpheme.count})")
            verb_count += 1
            if verb_count >= 5:
                break
    
    print("")
    '''
    # 인식된 개체명들 많이 노출된 순으로 출력 (최대 5개)
    for i, name_entity in enumerate(name_entities):
        if i >= 10:
            break
        print(f"[개체명] {name_entity.text} ({name_entity.count})")

except Exception as e:
    print(f"예외가 발생했습니다: {str(e)}")

name_characteristic = ["나이","견종","지역","색상"]
#print(name_entities[3].text, name_entities[3].count)
#수원시 1 출력

openApiURL_similarity = "http://aiopen.etri.re.kr:8000/WiseWWN/WordRel"

firstWord = "강아지"
firstSenseId = "00"
secondWord = "포메라니안"
secondSenseId = "00"

requestJson = {
    "argument": {
        'first_word': "강아지",
        'first_sense_id': firstSenseId,
        'second_word': "포메라니안",
        'second_sense_id': secondSenseId
    }
}

http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL_similarity,
    headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": etri_token},
    body=json.dumps(requestJson)
)

print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))

## 이 방법으로 사용 시, 언어 간 유사도 측정 시에 없는 강아지 종류에 대한 전처리 필요
# 일이 2배 3배로 들기 때문에 해당 문제에 대한 접근 새로 정리 필요