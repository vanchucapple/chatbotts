
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import fuzz
from rasa_sdk.events import SlotSet, AllSlotsReset, SessionStarted, ActionExecuted, EventType
import pandas as pd

df = pd.read_excel("Tuyensinh.xlsx")


list_name_col = ["Cấp", "Khoa", "Mã ngành","Học phí", "Cách tính điểm", "Xét tuyển theo học bạ", "link", "Khối thi", "Điểm năm 2021" , "Hồ sơ xét tuyển"]

def get_matching_entites(entities,list_name,threshold):

    result_match = dict()
    for i in list_name:
        ratio = fuzz.ratio(entities, i)
        result_match[i] =ratio
    print(result_match)
    if max(result_match.values()) >= threshold:
        return max(result_match, key=result_match.get)
    else:
        return []


def get_key(my_dict,val):

    for key, value in my_dict.items():
        if val == value:
            return key


class ActionSearchListDepartmentMajor(Action):


    def name(self) -> Text:
        return "action_search_list_department_major"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        department = tracker.get_slot("department")
        major = tracker.get_slot("major")
        name_department = tracker.get_slot("name_department")
        print("department: ",department)
        print("major: ",major)
        if (department != None) & (name_department != None):
            list_name_department = df['Khoa']
            
            result_entites_column = get_matching_entites(department,list_name_col,50)
            
            result_entites_department = get_matching_entites(name_department,list_name_department,50)
            
            message = df.loc[df[result_entites_column] == result_entites_department]['Ngành'].unique()
            
            dispatcher.utter_message(text=f"Gửi bạn danh sách các ngành của khoa {result_entites_department} : {message} ")
        elif (department != None) & (name_department == None):
            dispatcher.utter_message(text=f"Gửi bạn danh sách các Khoa của trường : {df['Khoa'].unique()}")
        elif (department == None) & (name_department == None) & (major != None):
            dispatcher.utter_message(text=f"Dách sách các Ngành mà trường đào tạo gồm: \n {df.Ngành}")
        return []

class ActionGetInfo(Action):


    def name(self) -> Text:
        return "action_get_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        phone_info = tracker.get_slot("phone_info")
        name_info = tracker.get_slot("name_info")
        print("name_info: ",name_info)
        print("phone_info: ",phone_info)

        if phone_info == None:
            dispatcher.utter_message(text=f"Bạn vui lòng gửi chúng tôi SĐT để người tư vấn có thể chủ động gọi bạn!")
        elif (phone_info != None) & (name_info != None):
            dispatcher.utter_message(text=f"Oke bạn! Bạn vui lòng đợi sẽ có người chủ động gọi tư vấn cho bạn. Cảm ơn!")
        elif (phone_info != None) & (name_info == None):
            dispatcher.utter_message(text=f"Bạn vui lòng đợi sẽ có người chủ động gọi tư vấn cho bạn. Cảm ơn!")
        return [AllSlotsReset()]

class ActionSearchExits(Action):


    def name(self) -> Text:
        return "action_search_exits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name_department = tracker.get_slot("name_department")
        name_major = tracker.get_slot("name_major")
        name_column = tracker.get_slot("name_column")
        print("name_department: ",name_department)
        print("name_major: ",name_major)
        print("name_column: ",name_column)
        list_major = df['Ngành']
        result_entites = get_matching_entites(name_major,list_major,80)
        if name_column != None:
            if result_entites == []:
                dispatcher.utter_message(text=f" Trường không đào tạo Ngành {name_major}")
                dispatcher.utter_message(text=f"Dách sách các Ngành mà trường đào tạo gồm: \n {df.Ngành}")
            else :
                if df.loc[df['Ngành']== result_entites]['Xét tuyển theo học bạ'].values[0] != []:
                    result_query = str(df.loc[df['Ngành']== result_entites]['Xét tuyển theo học bạ'].values[0])
                    dispatcher.utter_message(text=f"Ngành {name_major} có xét" f"tuyển theo học bạ {result_query}"
                    f"Bạn muốn hỏi gì thêm về Ngành này không?")
                    
                else: 
                    dispatcher.utter_message(text=f"Ngành {name_major} không xét tuyển theo học bạn. Thông tin đến bạn!")
        elif (name_department == None) & (name_column == None) & (name_major != None):
            print("result_entites: ",result_entites)
            if result_entites == []:
                dispatcher.utter_message(text=f" Trường không đào tạo Ngành {name_major}")
                dispatcher.utter_message(text=f"Dách sách các Ngành mà trường đào tạo gồm: \n {df.Ngành}")
            else :
                message = "Mã ngành: " \
                + str(df.loc[df['Ngành']== result_entites]['Mã ngành'].values[0])
                print(message)
                dispatcher.utter_message(text=f" Trường có đào tạo Ngành {name_major}." \
                f"{message}" \
                f". Bạn có thể tham khảo chi tiết tại http://tuyensinh.vuted.edu.vn/. Bạn muốn hỏi gì thêm về Ngành này không?")
        return [AllSlotsReset()]
    


class ActionSearchInfoMajor(Action):


    def name(self) -> Text:
        return "action_search_info_major"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name_column = tracker.get_slot("name_column")
        name_major = tracker.get_slot("name_major")
        print("name_major: ",name_major)
        print("name_column: ",name_column)
        list_major = df['Ngành']
        result_entites_major = get_matching_entites(name_major,list_major,80)
        result_entites_column = get_matching_entites(name_column,list_name_col,50)
        print("result_entites_major", result_entites_major)
        print("result_entites_column", result_entites_column)
        if name_major == None:
            dispatcher.utter_message(text=f"Bạn vui lòng hỏi rõ hơn, bạn "
                                        f"đang tìm kiếm thông tin gì cho chuyên Ngành nào?")
        else:
            message = str(df.loc[df['Ngành'] == result_entites_major][result_entites_column].values[0])
            dispatcher.utter_message(text=f"Gửi bạn thông tin {result_entites_column} của {result_entites_major}: {message} . Thông tin đến bạn!")
        return []

class ActionSearchFile(Action):


    def name(self) -> Text:
        return "action_search_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name_column = tracker.get_slot("name_column")
        result_entites_column = get_matching_entites(name_column,list_name_col,30)
        print("result_entites_column", result_entites_column)
        message = str(df[result_entites_column][0])
        dispatcher.utter_message(text=f"Gửi bạn thông tin {result_entites_column} : {message}")
        return []