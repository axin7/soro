from pprint import pprint
import time

from process.application import user_app_list,sys_app_list
from process.initial import save_user_app,initial_text,status_record,nlp_process,console,emoji
from process.asr import asr
from process.record import record
from process.correct import correct
from process.nlp import nlp


if __name__ == "__main__":
    console.print(f"[bold]{initial_text}[/bold]")

    console.print(emoji.emojize(':hammer:'),f"[bold gray]正在初始化[/bold gray]")
    st = time.time()
    user_applist, user_app_kw_dict = user_app_list()
    save_user_app(user_applist, user_app_kw_dict)
    correct('')
    console.print(emoji.emojize(':ok_hand:'),f"[bold gray]完成初始化[/bold gray]")
    print(" "*80)
    
    console.print(emoji.emojize(':sparkles:'),f"[bold red]跟我说点什么吧[/bold red]")
    print(" "*80)

    while True:
        speech_data = record()
        asr_result = asr(speech_data)
        correct_result= correct(asr_result)
        nlp_result = nlp(correct_result)
        nlp_process(nlp_result)
        print(" "*80)
