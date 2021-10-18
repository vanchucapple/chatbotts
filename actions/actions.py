from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import fuzz
from rasa_sdk.events import SlotSet, AllSlotsReset, SessionStarted, ActionExecuted, EventType
import pandas as pd
df = pd.read_excel("Tuyensinh.xlsx")

def get_matching_entites(entities,list_name,threshold):

    result_match = dict()
    print(entities)
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
        print("department: ",department)
        print("major: ",major)

        if department == None:
            dispatcher.utter_message(text=f"Dách sách các ngành mà trường đào tạo gồm: \n {df.ngành}")
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
        return []

class ActionSearchExits(Action):


    def name(self) -> Text:
        return "action_search_exits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name_department = tracker.get_slot("name_department")
        name_major = tracker.get_slot("name_major")
        print("name_department: ",name_department)
        print("name_major: ",name_major)

        if name_department == None:
            list_major = df['ngành']
            result_entites = get_matching_entites(name_major,list_major,70)
            if result_entites == []:
                dispatcher.utter_message(text=f" Trường không đào tạo ngành {name_major}")
                dispatcher.utter_message(text=f"Dách sách các ngành mà trường đào tạo gồm: \n {df.ngành}")
            else :
                dispatcher.utter_message(text=f" Trường có đào tạo ngành {name_major}. Thông tin đến bạn!")
                dispatcher.utter_message(text=f"Dách sách các ngành mà trường đào tạo gồm: \n {df.ngành}")
        return []