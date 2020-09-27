"""
该模块定义了实时录音及录音处理
"""

import pyaudio
import numpy as np
import time
from .initial import status_record,console,emoji
 
def record():
    """录音模块
    
    :return speech_data: 录音的数据流
    """
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    console.print(emoji.emojize(':clapper:'),"[bold red]正在录音[/bold red]")
    # print("开始缓存录音")
    record_start_time = time.time()
    frames = []
    frames_save = []
    start_record_time = 0
    last_record_time = 0
    times = 0
    temp = 0
    data = ''
    speech_data = b''
    while (True):
        # print(f"开始循环： {start_time}")
        for i in range(0, 5):
            data = stream.read(CHUNK)
            frames.append(data)

            if start_record_time>0 and temp > 30:
                if len(frames_save)>0:
                    frames_save.append(data)
                else:
                    frames_save.extend(frames[-40:])
            

        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        status_record(temp)
        # print (f'当前阈值为：{temp}') 
        # print("> 判断音量是否大于阈值")


        if temp > 100 :
            # print (">> 音量大于阈值")
            # print(f">>> 判断是否存在开始时间")
            if start_record_time:
                # print(f">>>> 存在开始时间")
                last_record_time = time.time()
                # print(f">>>>> 赋值最新有声时间为: {last_record_time}")
            
            elif not start_record_time :
                start_record_time = time.time()
                last_record_time = time.time()
                # print(f">>>> 不存在开始时间")
                # print(f">>>>> 赋值开始有声时间为: {start_record_time}")
                # print(f">>>>> 赋值最新有声时间为: {start_record_time}")
            

        else:
            # print(">> 音量小于阈值")
            # print(">>> 判断是否存在开始时间")
            if start_record_time:
                # print(">>>> 存在开始时间")
                # print(f">>>> 判断录音时长是否大于一秒")
                total_record_time = last_record_time - start_record_time
                if total_record_time > 0.5 :
                    # print(f">>>>> 录音时长为{total_record_time}")
                    # print(f">>>>> 判断录音时长大于一秒")
                    silent_time = time.time() - last_record_time
                    # print(f">>>>>> 判断静音时长是否大于一秒")
                    if silent_time < 0.3 :
                        # print(f">>>>>>> 静音时长为{silent_time}")
                        # print(f">>>>>>> 静音时长小于0.3秒")
                        # continue
                        print("",end='')

                    else:
                        # print(f">>>>>>> 静音时长为{silent_time}")
                        # print(f">>>>>>> 静音时长大于0.3秒")
                        record_stop_time = time.time()
                        # print(f"""

                        # 开始录音时间为： {record_start_time}
                        # 结束录音时间为： {record_stop_time}
                        # 总录音时长为： {record_stop_time-record_start_time}
                        # 开始有声时间为： {start_record_time}
                        # 最新有声时间为： {last_record_time}
                        # 静音时长为： {silent_time}
                        # """)
                        break

                else:
                    # print(f">>>>> 录音时长为{total_record_time}")
                    # print(f">>>>> 判断录音时长小于一秒")
                    frames_save = []
                    start_record_time = time.time()
                    last_record_time = time.time()
                    # print(f">>>>>> 更新开始有声时间为: {last_record_time}")
            else:
                # print(">>>> 不存在开始时间")
                print("",end='')

        end_time = time.time()
        # print(f"结束循环： {start_time}")
        # print(f"时间间隔为: {end_time > start_time}")
    stream.stop_stream()
    stream.close()
    p.terminate()
    speech_data = b''.join(frames_save)
    print(" "*80,end='\r')
    console.print(emoji.emojize(':ok:'),"完成录音")
    return speech_data


if __name__ == '__main__':
    while True :
        start = time.time()
        record()
        end = time.time()
        print(f"一共耗时为：{end-start}")
