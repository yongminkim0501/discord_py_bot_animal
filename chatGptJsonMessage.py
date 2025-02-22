from ChatGptApiManage import *
import json

class ChatGptMessage:
    def __init__(self):
        self.sigun_nm = None
        self.species_nm = None
        self.color_nm = None
        self.sex_nm = None

    def get_message(self, message):
        json_dict = json.loads(message.content)

        self.sigun_nm = json_dict["sigun_nm"]
        self.species_nm = json_dict["species_nm"]
        self.color_nm = json_dict["color_nm"]
        self.sex_nm = json_dict["sex_nm"]
        '''
        print(self.sigun_nm)    #강남구
        print(self.species_nm)  #포메라니안
        print(self.color_nm)    #갈색과 흰색
        print(self.sex_nm)      #수컷 등
        '''
    def get_sigun_nm(self):
        return self.sigun_nm

    def get_species_nm(self):
        return self.species_nm
    
    def get_color_nm(self):
        return self.color_nm
    
    def get_sex_nm(self):
        return self.sex_nm