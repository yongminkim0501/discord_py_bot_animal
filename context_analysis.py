'''import urllib3
import json

def connect_etri(path):
    with open(path) as f:
        config = json.load(f)
        TOKEN = config['etri_api_key']
    return TOKEN

etri_token = connect_etri("etri_token.json")

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"

accessKey = etri_token
analysisCode = "wsd"

morp : 형태소 분석
ner : 개체명 인식
dparse : 의존 구문 분석
wsd : 어휘 의미 분석

text = "윤동주(尹東柱, 1917년 12월 30일 ~ 1945년 2월 16일)는 한국의 독립운동가, 시인, 작가이다."+"중국 만저우 지방 지린 성 연변 용정에서 출생하여 명동학교에서 수학하였고, 숭실중학교와 연희전문학교를 졸업하였다. 숭실중학교 때 처음 시를 발표하였고, 1939년 연희전문 2학년 재학 중 소년(少年) 지에 시를 발표하며 정식으로 문단에 데뷔했다."+"일본 유학 후 도시샤 대학 재학 중 , 1943년 항일운동을 했다는 혐의로 일본 경찰에 체포되어 후쿠오카 형무소(福岡刑務所)에 투옥, 100여 편의 시를 남기고 27세의 나이에 옥중에서 요절하였다. 사인이 일본의 생체실험이라는 견해가 있고 그의 사후 일본군에 의한 마루타, 생체실험설이 제기되었으나 불확실하다. 사후에 그의 시집 《하늘과 바람과 별과 시》가 출간되었다."+"일제 강점기 후반의 양심적 지식인으로 인정받았으며, 그의 시는 일제와 조선총독부에 대한 비판과 자아성찰 등을 소재로 하였다. 그의 친구이자 사촌인 송몽규 역시 독립운동에 가담하려다가 체포되어 일제의 생체 실험으로 의문의 죽음을 맞는다. 1990년대 후반 이후 그의 창씨개명 '히라누마'가 알려져 논란이 일기도 했다. 본명 외에 윤동주(尹童柱), 윤주(尹柱)라는 필명도 사용하였다.";

requestJson = {
    "argument": {
            "text": text,
            "analysis_code": analysisCode
    }
}

http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={
        "Content-Type":"application/json; charset=UTF-8","Authorization":accessKey},
    body = json.dumps(requestJson)
)

print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))
'''
import requests
import json
from collections import defaultdict
import json

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
    noun_count = 0
    for morpheme in morphemes:
        if morpheme.type in ["NNG", "NNP", "NNB"]:
            print(f"[명사] {morpheme.text} ({morpheme.count})")
            noun_count += 1
            if noun_count >= 5:
                break
    
    print("")
    
    # 형태소들 중 동사들에 대해서 많이 노출된 순으로 출력 (최대 5개)
    verb_count = 0
    for morpheme in morphemes:
        if morpheme.type == "VV":
            print(f"[동사] {morpheme.text} ({morpheme.count})")
            verb_count += 1
            if verb_count >= 5:
                break
    
    print("")
    
    # 인식된 개체명들 많이 노출된 순으로 출력 (최대 5개)
    for i, name_entity in enumerate(name_entities):
        if i >= 10:
            break
        print(f"[개체명] {name_entity.text} ({name_entity.count})")

except Exception as e:
    print(f"예외가 발생했습니다: {str(e)}")