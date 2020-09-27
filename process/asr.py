"""
该模块调用百度进行语音识别
"""

import base64
import json
import sys
import time
from pprint import pprint
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .initial import console, emoji
from .config import ASR_API_KEY, ASR_SECRET_KEY

timer = time.perf_counter

API_KEY = ASR_API_KEY
SECRET_KEY = ASR_SECRET_KEY

# 需要识别的文件
AUDIO_FILE = 'cache1.wav'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = 'wav'  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值


#测试自训练平台需要打开以下信息， 自训练平台模型上线后，您会看见 第二步：“”获取专属模型参数pid:8001，modelid:1234”，按照这个信息获取 dev_pid=8001，lm_id=1234
# DEV_PID = 8001 ;   
# LM_ID = 1234 ;

# 极速版 打开注释的话请填写自己申请的appkey appSecret ，并在网页中开通极速版（开通后可能会收费）

DEV_PID = 80001
ASR_URL = 'http://vop.baidu.com/pro_api'
SCOPE = 'brain_enhanced_asr'  # 有此scope表示有极速版能力，没有请在网页里开通极速版

# 忽略scope检查，非常旧的应用可能没有
# SCOPE = False

class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    f = urlopen(req)
    result_str = f.read()   
    result_str = result_str.decode()
    result = json.loads(result_str)

    return result['access_token']

"""  TOKEN end """

def asr(speech_data):
    token = fetch_token()
    length = len(speech_data)
    speech = base64.b64encode(speech_data)
    speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
             #"lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': '123456PYTHON',
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        # print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = str(result_str, 'utf-8')
    value = json.loads(result_str).get('result',"null")[0]
    # result = re.sub('\W+', '', value).replace("_", '')
    result = value.strip('。')
    # console.print(emoji.emojize(':point_right:'),f"[bold gray]{result}[/bold gray]")
    return result
