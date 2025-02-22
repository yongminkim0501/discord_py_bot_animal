import pandas
from discord_main import *

class update_searching_data:
    def __init__(self, sigun_nm, species_nm, color_nm, sex_nm):
        self.api = None
        self.dataset = None
        self.message = None
        self.sigun_nm = sigun_nm
        self.color_nm = color_nm
        self.sex_nm = sex_nm
        self.speices_nm = species_nm

    def set_api(self, api_name):
        self.api = api_name

    def searching_by_SIGUN(self,SIGUN_name):
        self.dataset = self.api.search_SIGUN_NM(SIGUN_name)
    
    def searching_by_Species_NM(self, Species_NM):
        temp_dataFrame = []
        for individual in self.dataset:
            if individual[6] == Species_NM :
                temp_dataFrame.append(individual)
        self.dataset = temp_dataFrame

    def searching_by_color_nm(self, color_NM):
        temp_dataFrame = []
        for individual in self.dataset:
            if individual[8] == color_NM :
                temp_dataFrame.append(individual)
        self.dataset = temp_dataFrame

    def searching_by_sex_nm(self, sex_NM):
        temp_dataFrame = []
        for individual in self.dataset:
            if individual[16] == sex_NM:
                temp_dataFrame.append(individual)
        self.dataset = temp_dataFrame

    def set_chatGPT_message(self, message):
        self.message = message

    def all_work_run(self):
        # 처리 데이터는 나중에 정의
        # 필요한 데이터 형식은 sigun_name, species_nm, color_nm, sex_nm

        self.searching_by_SIGUN(self.sigun_nm)
        self.searching_by_Species_NM(self.species_nm)
        self.searching_by_color_nm(self.color_nm)
        self.searching_by_sex_nm(self.sex_nm)

        return self.dataset
