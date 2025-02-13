'''
params => api_key, response_type, page_index, page_size
기본 값 : response_type = json, page_index = 1, page_size = 100
'''
import requests
import pandas as pd
class animalcheck:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.data = None 
        self.rows = None

    def get_animals(self, response_type = 'json', page_index=1, page_size=100, **kwargs):
        params = {
            'KEY': self.api_key,
            'Type': response_type,
            'pIndex': page_index,
            'pSize': page_size
        }
        #params.update({k: v for k, v in kwargs.items() if v is not None})

        try:
            response = requests.get(self.api_url, params = params)
            response.raise_for_status()

            if response_type.lower() == 'json':
                self.data = response.json()
                if 'AbdmAnimalProtect' in self.data:
                     self.rows = self.data['AbdmAnimalProtect'][1]['row']
            else:
                raise ValueError("1")
        
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")
            return None
        
        except Exception as e:
            print(f"데이터 처리 중 오류 발생: {e}")
            return None
        
    def get_rows(self):
        return self.rows
    
    def search_SIGUN_NM(self, name):
        rows = self.get_rows()

        temp = []
        for individual in rows:
            if individual['SIGUN_NM'] == name:
                temp.append(individual)
        
        return pd.DataFrame(temp)
    
    def get_pandas_frame_data(self):
        return_data = self.get_rows()
        return pd.DataFrame(return_data)

    def get_tolist(self):
        dataset = self.get_pandas_frame_data()
        return dataset.columns.tolist()
    
    def get_count_species(self):
        dataset = self.get_pandas_frame_data()
        return dataset['SPECIES_NM'].value_counts().head()

    def get_count_age(self):    
        dataset = self.get_pandas_frame_data()
        return dataset['AGE_INFO'].value_counts().head()
    
    def get_count_sex(self):
        dataset = self.get_pandas_frame_data()
        return dataset['SEX_NM'].value_counts().head()
    
    def get_count_CHRGPSN_CONTCT_NO(self):
        dataset = self.get_pandas_frame_data()
        return dataset['CHRGPSN_CONTCT_NO'].value_counts().head()

    def _check_data_type_in_function(self):
        print(type(self.rows))
        print(type(self.data))
        print(type(self.get_pandas_frame_data()))

    def run(self):
        self.get_animals()

    def search(self, dog_breed, color, sex, neutering):
        dataset = self.get_pandas_frame_data() # pd.DataFrame 형식
        
def main():
    api_key = "8c605c4107134176a66bcea32876cfba"
    api_url = "https://openapi.gg.go.kr/AbdmAnimalProtect"
    api = animalcheck(api_key, api_url)
    api.run() # 이 부분을 실행해야만 함
'''
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
