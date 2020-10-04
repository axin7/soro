"""
该模块定义了调用Rasa服务
"""

import time
from http.client import responses
from pprint import pprint

import requests

from .config import MESSAGE_NLP_FAIL, MESSAGE_UNKNOW, VALUE_QA_UNKNOW


def nlp(query,message_id='123',sender='user'):
    """调用Rasa服务
    
    :param query：用户输入信息
    :param message_id：对话ID
    :param sender：发送者
    :return message_res: Rasa服务的返回信息
    """

    # Rasa服务调用接口地址。 接口文档地址：1、https://rasa.com/docs/rasa/api/http-api/   2、https://rasa.com/docs/rasa/api/action-server/
    _url_core_message = f'http://localhost:5005/conversations/{message_id}/messages'    #rasa-core query加入tracker地址
    _url_core_predict = f'http://localhost:5005/conversations/{message_id}/predict'     #rasa-core 预测下一步动作
    _url_core_action  = 'http://localhost:5055/webhook/'

    nlu_req_data = {"text":query,"message_id":message_id}
    core_message_req_data = {"text":query,"sender":sender}
    # core_action_req_data = {"next_action":action,"sender_id":message_id,"tracker":tracker}



    core_message_req = requests.post(_url_core_message,json=core_message_req_data)
    core_message_res = dict(core_message_req.json())
    intent_name = core_message_res["latest_message"]["intent"]["name"]
    intent_confidence = core_message_res["latest_message"]["intent"]["confidence"]

    # 当意图为QA类时
    if intent_name in ['chitchat']:
        if intent_confidence  > VALUE_QA_UNKNOW :
            response = core_message_res["latest_message"]["response_selector"]["default"]["response"]["name"]
            return response

        else:
            return MESSAGE_UNKNOW

    # 当意图为空时
    elif not intent_name:
        return MESSAGE_UNKNOW

    else:

        try:
            core_predict_req = requests.post(_url_core_predict)
            core_predict_res = dict(core_predict_req.json())
            action = core_predict_res['tracker']['latest_message']['intent']['name']
            tracker = core_predict_res['tracker']
            core_action_req_data = {"next_action":f"action_{action}","sender_id":message_id,"tracker":tracker}
            core_action_req = requests.post(_url_core_action,json=core_action_req_data)
            core_action_res = dict(core_action_req.json())
            message_res = core_action_res['responses'][0]['text']
            # pprint(message_res)
            return message_res

        except Exception as ex:
            # print(ex)
            return MESSAGE_NLP_FAIL

