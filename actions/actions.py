
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from fuzzywuzzy import fuzz
from rasa_sdk.events import SlotSet, AllSlotsReset, SessionStarted, ActionExecuted, EventType
import pandas as pd

df = pd.read_excel("Tuyensinh.xlsx")
list_name_col = list(df.columns)
list_major = df['Ngành']
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


class ActionContacts(Action):

    def name(self) -> Text:
        return "action_contacts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        button = {
            "type": "postback",
            "title": "Tư vấn nhanh ở đây",
            "payload": "/quick_consultation"
        }
        button1 = {
            "type": "postback",
            "title": "Gọi điện tư vấn trực tiếp",
            "payload": "/hotline"
        }

        button2 = {
            "type": "web_url",
            "url": "http://tuyensinh.vuted.edu.vn/",
            "title": "Truy cập vào website"
        }

        ret_text = "Bạn vui lòng chọn một trong các phương thức tư vấn sau: "
        dispatcher.utter_message(text=ret_text, buttons=[button, button1, button2])

        return []
    
class ActionSearchListDepartmentMajor(Action):


    def name(self) -> Text:
        return "action_search_list_department_major"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("__________________________action_search_list_department_major_______________________")
        department = tracker.get_slot("department")
        major = tracker.get_slot("major")
        name_department = tracker.get_slot("name_department")
        print("department: ",department)
        print("major: ",major)
        if (department != None) & (name_department != None):
            list_name_department = df['Khoa']
            
            result_entites_column = get_matching_entites(department,list_name_col,50)
            
            result_entites_department = get_matching_entites(name_department,list_name_department,50)
            
            dispatcher.utter_message(text=f"Gửi bạn danh sách các ngành của khoa {result_entites_department} : ")
            
            for i in df.loc[df[result_entites_column] == result_entites_department]['Ngành'].unique():
                dispatcher.utter_message(i)
            
            
        elif (department != None) & (name_department == None):
            dispatcher.utter_message(text=f"Gửi bạn danh sách các Khoa của trường : ")
            for i in df['Khoa'].unique():
                dispatcher.utter_message(i)
        elif (department == None) & (name_department == None) & (major != None):
            dispatcher.utter_message(text=f"Trường đang đào tạo {len(df['Ngành'].unique())} ngành. Danh sách các Ngành mà trường đào tạo gồm: ")
            for i in df['Ngành'].unique():
                dispatcher.utter_message(i)
        return [AllSlotsReset()]

class ActionGetInfo(Action):


    def name(self) -> Text:
        return "action_get_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("__________________________action_get_info_______________________")
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

class ActionSearchMajorExits(Action):
    
    def name(self) -> Text:
        return "action_search_major_exits"
    def  run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("_______________________action_search_major_exits___________________")
        name_major = tracker.get_slot("name_major")
        result_name_major = get_matching_entites(name_major,list_major,60)
        if result_name_major != []:
            message = " Mã ngành: " \
                    + str(int(df.loc[df['Ngành']== result_name_major]['Mã ngành'].values[0]))
            print(message)
            dispatcher.utter_message(text=f"Trường có đào tạo Ngành {name_major}." \
            f"{message}" \
            f". Bạn có thể tham khảo chi tiết tại http://tuyensinh.vuted.edu.vn/. Bạn muốn hỏi gì thêm về Ngành này không?")
        else:
            dispatcher.utter_message(text=f" Trường không đào tạo Ngành {name_major}")
            dispatcher.utter_message(text=f"Dách sách các Ngành mà trường đào tạo gồm: \n {df.Ngành}")
        
class ActionSearchColumnsExits(Action):


    def name(self) -> Text:
        return "action_search_column_exits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("_______________________action_search_column_exits___________________")
        
    
        name_major = tracker.get_slot("name_major")
        name_column_exits = tracker.get_slot("name_column_exits")
        print("name_major: ",name_major)
        print("name_column_exits: ",name_column_exits)
        
        result_name_major = get_matching_entites(name_major,list_major,60)
        result_name_column_exits = get_matching_entites(name_column_exits,list_name_col,30)
        
        if name_column_exits != None:
            
            if name_major == None:
            
                dispatcher.utter_message(text=f"Bạn vui lòng nói rõ bạn đang tìm thông tin gì và của ngành nào giúp mình!")
            else :
                
                if result_name_major == []:
                    dispatcher.utter_message(text=f"Ngành {result_name_major}  trường không đào tạo. Thông tin đến bạn!")
                else:
                    
                    if df.loc[df['Ngành']== result_name_major][result_name_column_exits].values[0] != []:
                        dispatcher.utter_message(text=f"Ngành {name_major} " f"trường có đào tạo và còn có thể {result_name_column_exits}" 
                        f". Bạn muốn hỏi thêm thông tin gì về ngành này không?")
                        
                    else: 
                        dispatcher.utter_message(text=f"Ngành {name_major} " f"trường có đào tạo và không {result_name_column_exits}" 
                        f". Thông tin đến bạn")
                        
        elif (name_column_exits == None) & (name_major != None):
            print("result_name_major: ",result_name_major)
            if result_name_major == []:
                dispatcher.utter_message(text=f" Trường không đào tạo Ngành {name_major}")
                dispatcher.utter_message(text=f"Dách sách các Ngành mà trường đào tạo gồm: \n {df.Ngành}")
            # else :
            #     message = " Mã ngành: " \
            #     + str(int(df.loc[df['Ngành']== result_name_major]['Mã ngành'].values[0]))
            #     print(message)
            #     dispatcher.utter_message(text=f" Trường có đào tạo Ngành {name_major}." \
            #     f"{message}" \
            #     f". Bạn có thể tham khảo chi tiết tại http://tuyensinh.vuted.edu.vn/. Bạn muốn hỏi gì thêm về Ngành này không?")
        return []
    


class ActionSearchInfoMajor(Action):


    def name(self) -> Text:
        return "action_search_info_major"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("__________________________action_search_info_major_______________________")
        
        name_column = tracker.get_slot("name_column")
        name_major = tracker.get_slot("name_major")
        print("name_major: ",name_major)
        print("name_column: ",name_column)
        result_entites_major = get_matching_entites(name_major,list_major,50)
        result_entites_column = get_matching_entites(name_column,list_name_col,35)
        print("result_entites_major", result_entites_major)
        print("result_entites_column", result_entites_column)
        
        if name_major == None:
            
            dispatcher.utter_message(text=f"Bạn vui lòng hỏi rõ hơn, bạn "
                                        f"đang tìm kiếm thông tin gì cho chuyên ngành nào?")
        elif (name_column == None) & (name_major != None):
            if result_entites_major != []:
                message = " Mã ngành: " \
                        + str(int(df.loc[df['Ngành']== result_entites_major]['Mã ngành'].values[0]))
                print(message)
                dispatcher.utter_message(text=f"Trường có đào tạo Ngành {name_major}." \
                f"{message}" \
                f". Bạn có thể tham khảo chi tiết tại http://tuyensinh.vuted.edu.vn/. Bạn muốn hỏi gì thêm về Ngành này không?")
            else:
                dispatcher.utter_message(text=f" Trường không đào tạo Ngành {name_major}")
                dispatcher.utter_message(text=f"Dách sách các Ngành mà trường đào tạo gồm: \n {df.Ngành}")
                
        
        elif (name_column != None) & (name_major != None):
            if result_entites_major == []:
                dispatcher.utter_message(text=f" Trường không đào tạo Ngành {name_major}. Thông tin đến bạn!")
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
        print("__________________________action_search_file_______________________")
        file = tracker.get_slot("file")
        level = tracker.get_slot("level")
        if level != None:
            dispatcher.utter_message(text=f"Bạn vui lòng nói rõ bạn muốn thông tin hồ sơ của cấp nào? Đại học, cao đẳng hay thạc sĩ??")
        else:
            message = df.loc[df['Cấp']== level]['Hồ sơ'][0]
            dispatcher.utter_message(text=f"Gửi bạn thông tin về hồ sơ của cấp {level} : message")
            
        return []

class ActionSearchFile(Action):

    def name(self) -> Text:
        return "action_search_file"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        button = {
            "type": "postback",
            "title": "Thông tin hồ sơ cấp đại học",
            "payload": "/daihoc"
        }
        button1 = {
            "type": "postback",
            "title": "Thông tin hồ sơ cấp cao đẳng",
            "payload": "/caodang"
        }

        button2 = {
            "type": "postback",
            "title": "Thông tin hồ sơ cấp thạc sĩ",
            "payload": "thacsi"
        }

        ret_text = "Bạn vui lòng chọn một trong các phương thức tư vấn sau: "
        dispatcher.utter_message(text=ret_text, buttons=[button, button1, button2])

        return []
    
class ActionSaveConversation(Action):


    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        conversation = tracker.events #get all info of conversation
        # # print(conversation)

        # save to csv
        import os
        if not os.path.isfile('chats.csv'):
            with open('chats.csv', 'w') as file:
                file.write(
                    "user_input,intent,entity_name,entity_value,"
                    "bot_reply\n")

        chat_data = ''

        for i in range(len(conversation)):

            if conversation[i]['event'] == 'user':

                chat_data += conversation[i]['text'] \
                             + ',' \
                             + conversation[i]['parse_data']['intent']['name'] \
                             + ','
                # # print('user: {}'.format(i['text']))

                if len(conversation[i]['parse_data']['entities']) > 0:
                    chat_data += str([conversation[i]['parse_data']['entities'][j]['entity']
                                  for j in range(len(conversation[i]['parse_data'][
                                                         'entities']))]) \
                                 + ',' \
                                 + str([conversation[i]['parse_data']['entities'][j][
                                            'value']
                                    for j in range(len(conversation[i]['parse_data'][
                                                           'entities']))]) \
                                 + ','
                    # # print('extra data:',
                    #       i['parse_data']['entities'][0]['entity'], '=',
                    #       i['parse_data']['entities'][0]['value'])

                else:
                    chat_data += ",,"


            elif conversation[i]['event'] == 'bot':
                # # print('Bot: {}'.format(i['text']))
                if conversation[i-1]['event'] != 'bot':
                    chat_data += conversation[i]['text'] \
                                 + '\n'
                else:
                    chat_data += ',,,,' \
                                + conversation[i]['text'] + '\n'
        else:
            # print("_________________________________________")

            with open('chats.csv', 'a') as file:
                file.write(chat_data)
            chat_data = ''
        chat_data = []
        # print(chat_data)
        return []
