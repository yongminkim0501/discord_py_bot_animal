from ChatGptApiManage import *

class ChatGptMessage:
    def __init__(self):
        self.sigun_nm = None
        self.species_nm = None
        self.color_nm = None
        self.sex_nm = None

    def get_message(self, message):
        self.sigun_nm = message[0][1]
        self.species_nm = message[1][1]
        self.color_nm = message[2][1]
        self.sex_nm = message[3][1]

    def get_sigun_nm(self):
        return self.sigun_nm

    def get_species_nm(self):
        return self.species_nm
    
    def get_color_nm(self):
        return self.color_nm
    
    def get_sex_nm(self):
        return self.sex_nm