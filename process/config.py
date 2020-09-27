"""
该模块为配置参数
"""
# 百度ASR配置参数
ASR_API_KEY = ""
ASR_SECRET_KEY = ""

# 返回消息是否开启语音合成
SPEECH = True

# nlp模块错误时返回的话术
MESSAGE_NLP_FAIL = "抱歉系统错误"

#QA类意图无法识别的置信度阈值
VALUE_QA_UNKNOW = 0.7

# 意图为未知问题时返回的话术
MESSAGE_UNKNOW = "抱歉，不太明白您的意思"