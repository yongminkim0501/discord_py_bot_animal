from chatGptJsonMessage import *
from searching_data import *

chatGptObject = ChatGptMessage()

temp_sigun_nm = chatGptObject.get_sigun_nm()
temp_species_nm = chatGptObject.get_species_nm()
temp_color_nm = chatGptObject.get_color_nm()
temp_sex_nm = chatGptObject.get_sex_nm()

candidate_array = []
update_searching_data_object = update_searching_data(temp_sigun_nm, temp_species_nm, temp_color_nm, temp_sex_nm)
candidate_array = update_searching_data_object.all_work_run() # 실행

