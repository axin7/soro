"""
该模块对query进行纠错
"""
from .initial import console, emoji
from pycorrector import Corrector #kenlm安装失败使用：pip install https://github.com/kpu/kenlm/archive/master.zip

path = ('./data/people_chars_lm.klm')
model = Corrector(language_model_path=path)

def correct(sentence):
    """句子纠错
    
    :param sentence：待纠错原句
    :return result: 纠错完成后的句子
    """
    result, detail = model.correct(sentence)
    # print(result, detail)
    if sentence:
        console.print(emoji.emojize(':point_right:'),f"[bold gray]{result}[/bold gray]")
    return result