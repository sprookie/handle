import PySimpleGUI as sg
import pandas as pd
import os
import time
import numpy as np
import threading
import PIL
import io
from PIL import Image


def convert_to_bytes(file_or_bytes, resize=None, fill=False):
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    if fill:
        if resize is not None:
            img = make_square(img, resize[0])
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
      

sg.theme('DarkBlack')
img = convert_to_bytes('handler.png', (100,100))

wd = sg.Window('handler',
               [[sg.Image(data=img), sg.Text('输入提醒事项',key='txt')],
                [sg.Input()],
                [sg.Checkbox('豪放模式'), sg.Checkbox('人性模式')],
                [sg.Btn('确认')],
                [sg.Cancel()]]
               )
count = 0
flag = 1


def listen():
    while True:
        global flag
        global values
        global min_num
        event, values = wd.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            flag = 0
            sg.popup(values[0])
            wd.close()
            break
        else:
            if values[1]:
                min_num = np.random.randint(0,1440)
            else:
                min_num = np.random.rayleigh(scale=30)
            wd['txt'].update('设定完毕')


def countdown():
    while flag:
        global count
        time.sleep(1)
        count += 1

        
def listen_shutdown():
    while True:
        global count
        global flag
        global min_num
        time.sleep(1)
        if count >= min_num * 60:
            flag = 0
            sg.popup(values[0])
            wd.close()
            break

l = threading.Thread(target=listen)
c = threading.Thread(target=countdown)
s = threading.Thread(target=listen_shutdown)
l.start()
c.start()
s.start()

