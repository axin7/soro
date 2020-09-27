"""
该模块定义初始化
"""

import ast
from random import randint
import subprocess

import emoji
from rich.console import Console

from .model import App, Db_sqlite, InFo
from .config import SPEECH


def save_user_app(user_applist, user_app_kw_dict):
    """保存用户应用信息
    
    :param user_applist：用户应用列表
    :param user_app_kw_dict：用户应用关键词词典
    """
    Db_sqlite.connect()
    Db_sqlite.create_tables([App,InFo])

    # 保存用户应用信息
    for i in user_applist:
        app = (App
        .replace(name=i['name'], path=i['path'], tag=i['tag'])
        .execute())

    # 合并、更新app关键词词典
    query = InFo.select().where(InFo.name=='sys_app_kw_dict')
    sys_app_kw_dict = ast.literal_eval(query[0].content)

    app_kw_dict =dict(sys_app_kw_dict,**user_app_kw_dict)
    kw = (InFo
        .replace(name="app_kw_dict", content=app_kw_dict)
        .execute())

    Db_sqlite.close


console = Console()

def status_record(value=0,rand_value=2):
    """录音状态可视化
    
    :param value：帧的最大采样值
    :param rand_value：随机值。用来控制进度条的刷新率
    """
    
    rand = randint(1,rand_value)
    if rand == 1:
        print(" "*80,end='\r')
        if value < 100:
            times = int((value/3) + 1)
            if times > 10:
                times = 10
            str1 = ':dash:' * times
            console.print("[bold gray]环境音:[/bold gray]",emoji.emojize(str1),end='\r')

        else:
            times = int((value/100) + 1)
            if times > 10:
                times = 10
            str2 = ':sound:' * times
            console.print("[bold red]录音中:[/bold red]",emoji.emojize(str2),end='\r')

def nlp_process(message,speech=SPEECH):
    if message:
        console.print(emoji.emojize(':ok_hand:'),f"[bold blue]{message}[/bold blue]",end='\n ')

        if speech:
            command = ['say','-v','Mei-Jia',message]
            subprocess.run(command)

# 初始化文字
initial_text = """    

_ _ _ _ _ _ _ _ _ _ _ _ _ _ _                                        
  ___    ___    _ __    ___  
 / __|  / _ \  | '__|  / _ \ 
 \__ \ | (_) | | |    | (_) |
 |___/  \___/  |_|     \___/ 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _                                                                                                                                                       
"""