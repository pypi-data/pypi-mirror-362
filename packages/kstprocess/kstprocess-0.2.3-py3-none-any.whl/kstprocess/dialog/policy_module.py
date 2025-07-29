"""
     对话机器人--一些默认的policy。不同科室根据不同的特性进行不同的配置。
"""


from typing import Optional, Dict, List
import json
from cachetools import LRUCache
import configparser
import re
from kstprocess.dialog.postprocess import ActionProcessor



class ContextClueModel():
    def __init__(self) -> None:
        self.session_id = None
        self.nlu_result = LRUCache(maxsize=10000)
        self.topic_dict = LRUCache(maxsize=10000)
        self.action_filter_flag_dict = LRUCache(maxsize=10000)
        self.male_gender_keyword = ["睾丸", "阴茎", "阴毛", "腋毛", "胡须", 
                            "喉结", "变声", "睾丸酮", "雄激素",  "男"
                            "男生", "男孩"]
        
        self.female_gender_keyword = ["姨妈", "月经", "例假", "乳房", "阴毛", 
                                "腋毛", "初潮", "骨盆", "卵巢", "女生胸部", "女",
                                "女生", "女孩"]
    
    def get_nlu_result_and_get_clue(self, 
                                    session_id: Optional[str],
                                    input_params: Optional[Dict],
                                    user_utterance: Optional[str],
                                    keyword: Optional[str]):
        self.session_id = session_id
        ### 获取对话的 self.topic 信息
        if session_id not in self.topic_dict:
           self.topic_dict[session_id] = input_params["topic"] 
        elif session_id in self.topic_dict and input_params["topic"] != "无主题":
            self.topic_dict[session_id] = input_params["topic"] 


        ### 获取搜索词中的性别信息
        if session_id not in self.action_filter_flag_dict:
            self.action_filter_flag_dict[session_id] = {}

        if session_id not in self.nlu_result:
            self.nlu_result[session_id] = {"age": None, "gender": None, "height": None, "weight": None, "identity": None}
        
        if "nluResult" not in input_params or not input_params["nluResult"]:
            self.nlu_result[session_id] = {"age": None, "gender": None, "height": None, "weight": None, "identity": None}
            self.action_filter_flag_dict[session_id] = {}
            return


        for item in json.loads(input_params["nluResult"])["data"][0]["entity"]:
            if item["key"] == "age":
                self.nlu_result[session_id]["age"] = item["value"][0]
            if item["key"] == "gender":
                self.nlu_result[session_id]["gender"] = item["value"][0]
            if item["key"] == "height":
                self.nlu_result[session_id]["height"] = item["value"][0] 
            if item["key"] == "weight":
                self.nlu_result[session_id]["weight"] = item["value"][0]
            if item["key"] == "identity" and item["name"] == "身份":
                self.nlu_result[session_id]["identity"] = item["value"][0]

        
        if not self.nlu_result[session_id]["gender"]:
            for key in self.female_gender_keyword:
                if key in user_utterance:
                    self.nlu_result[session_id]["gender"] = "女"
                if key in keyword:
                    self.nlu_result[session_id]["gender"] = "女"
            for key in self.male_gender_keyword:
                if key in user_utterance:
                    self.nlu_result[session_id]["gender"] = "男"
                if key in keyword:
                    self.nlu_result[session_id]["gender"] = "男"

        if "keyword_entity" in input_params and "data" in input_params["keyword_entity"] and input_params["keyword_entity"]["data"]:
            if input_params["keyword_entity"]["data"]["age"]:
                self.nlu_result[session_id]["age"] = input_params["keyword_entity"]["data"]["age"]
            if input_params["keyword_entity"]["data"]["gender"]:
                self.nlu_result[session_id]["gender"] = input_params["keyword_entity"]["data"]["gender"]



        if self.nlu_result[session_id]["gender"]:
            self.action_filter_flag_dict[session_id]["gender"] = True
        
        if self.nlu_result[session_id]["age"]:
            self.action_filter_flag_dict[session_id]["age"] = True



    def postprocess_by_age(self, response):
        try:
            if self.session_id in self.nlu_result and  "age" in self.nlu_result[self.session_id] and self.nlu_result[self.session_id]["age"] and int(self.nlu_result[self.session_id]["age"])>=18:
                response = [item.replace("孩子", "") for item in response]
                return response
            else:
                return response
        except:
            return response
        
    def postprocess_by_identity(self, response):
        try:
            if self.session_id in self.nlu_result and  "identity" in self.nlu_result[self.session_id] and self.nlu_result[self.session_id]["identity"] in ["自己", "我自己", "本人", "是本人"]:
                response = [item.replace("他", "").replace("她", "").replace("它", "") for item in response]
                return response
            else:
                return response
        except:
            return response





class ActionFilter():
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./config/sever.ini')
        with open(self.config["other"]["action_map_file_path"]) as f:
            self.action_map = json.load(f)
        self.actions_priority = {"答疑":2, "套电": 1, "问诊": 1, "None":0}
        with open(self.config["other"]["local_prompt_artificial_file"]) as f:
            self.local_prompt_artificial_file = json.load(f)
        self.topic_dict = LRUCache(maxsize=10000)
        self.session_id = None
        self.action_processor = ActionProcessor()

    def return_action_type(self, action:str):
        acquire_contact_type = self.action_map["套电"]
        Interrogation_type = self.action_map["问诊"]
        reply_type = self.action_map["答疑"]
        if action in acquire_contact_type:
            return "套电"
        elif action in Interrogation_type:
            return "问诊"
        elif action in reply_type:
            return "答疑"
        else:
            return "None"
        
    
    def add_prompt_priority(self, basic_action_label_list:Optional[List]=None, 
                                 mapping_prompt:Optional[List]=None,
                                 max_action_num:Optional[int]=4):
        """
             在basic_action_label_list加入 action，如果存在问诊，套电 动作则 不加入
        """
        actions_count = {"套电": 0, "答疑":0, "问诊": 0, "None": 0}
        save_actions = set()

        for basic_ac in basic_action_label_list:
            basic_t = self.return_action_type(basic_ac)
            actions_count[basic_t] += 1
            save_actions.add(basic_ac)

        for mapping_ac in mapping_prompt:
            mapping_t = self.return_action_type(mapping_ac)    
            if mapping_t != "None" and actions_count[mapping_t] > 2:
                continue
            if mapping_t == "套电" and actions_count["问诊"] > 0:
                continue
            if mapping_t == "问诊" and actions_count["套电"] > 0:
                continue
            if len(save_actions) <= max_action_num:
                save_actions.add(mapping_ac)
            else:
                break
        return list(save_actions)

    def count_action_type_num(self, actions:Optional[List]):
        """
            计算一个list 中的action 他的一级标签的分布
        """
        actions_count = {"套电": 0, "答疑":0, "问诊": 0, "None": 0}
        for ac in actions:
            actions_count[self.return_action_type(ac)] += 1
            if ac in self.action_map.keys():
                actions_count[ac] += 1
        return actions_count
    
    def get_order_value(self, actions:Optional[List]):
        """
             按照默认的一级标签的优先级，进行重排。
        """
        action_order_dict = {}
        for ac in actions:
            ac_priority = self.actions_priority[self.return_action_type(ac)]
            action_order_dict[ac] = ac_priority
        action_order_dict = sorted(action_order_dict.items(), key=lambda x: x[1], reverse=True)
        actions = [action for action, _ in action_order_dict]
        return actions


    def add_prompt_strict(self, basic_action_label_list:list, prompt_artificial:list):
        """
           basic_action_label_list 加入action --》全包容策略
        """
        basic_action_label_list.extend(prompt_artificial)
        basic_action_label_list = list(set(basic_action_label_list))
        return prompt_artificial
    

    def fill_action_by_default_config(self, prompt_artificial:Optional[List],
                                            server_round:Optional[str]):
        """
            查找本地配置的指令，例如(默认主题继承)
                    "抽动症": {
                        "1": ["问年龄"],
                        "2": ["问诊"],
                        "3": ["问诊"],
                        "4": ["问诊"],
                        "5": ["治疗套电话术"],
                        "7": ["答疑", "套电相关"],
                        "10": ["套电相关"],
                        "13": ["套电相关"]
                    },
        """

        new_prompt_artificial = []
        for p in prompt_artificial:
            if p in ["问诊", "答疑", "套电", "套电相关"] and self.topic_dict[self.session_id] in self.local_prompt_artificial_file.keys() and server_round in self.local_prompt_artificial_file[self.topic_dict[self.session_id]].keys() and p ==  self.return_action_type(self.local_prompt_artificial_file[self.topic_dict[self.session_id]][server_round]):
                new_prompt_artificial.extend(self.local_prompt_artificial_file[self.topic_dict[self.session_id]][server_round])
            else:
                new_prompt_artificial.append(p)
        return new_prompt_artificial
    
    
    def action_filter_policy_for_prospective_user(self,
                                                  dialogRecord:Optional[List[Dict]],
                                                  user_utterance:str,
                                                  server_round:int,
                                                  action_label_list: Optional[List]):
        """
            倾向套电的， 下一轮 action 更新为要联系方式。
        """
        # ROBOT_WARM ROBOT_GUIDE ROBOT_GREETING
        pattern = r'^(?:[嗯恩]?好的?|可以[的]?$?|方便$|行$|成$|[OoKk]$|谢谢$|[嗯恩]，好$|[嗯恩],好$|好好$|[嗯恩]$|发来看看$|用$)$'
        actions_order_list = [line["action"] for line in dialogRecord if line["subType"] not in ["ROBOT_GREETING", "ROBOT_GUIDE", "ROBOT_WARM"] and line["role"]=="SERVER"]
        last_action = actions_order_list[-1] 
        last_ac_map = self.action_processor.get_action_level_count(last_action)
        if last_ac_map["套电"] > 0 and server_round >3 and re.match(pattern, user_utterance):
            return ["要微信"]
        else:
            return action_label_list