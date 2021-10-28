import PySimpleGUI as sg
import os
import time
import numpy as np
import threading
import PIL
import io
from PIL import Image
import winsound
import time


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


img = convert_to_bytes('handle.png', (100,100), )

wd = sg.Window('handle',
               [[sg.Image(data=img), sg.Text('输入提醒事项', key='txt',
                                             text_color='#7878AB',
                                             font='Abel',
                                             auto_size_text=True,
                                             background_color='#F5F5FA')],

                [sg.Input()],

                [sg.Checkbox('豪放模式', font='Abel',
                             text_color='#7878AB', background_color='#F5F5FA'),
                 sg.Checkbox('人性模式', font='Abel', 
                             text_color='#7878AB', background_color='#F5F5FA')],

                [sg.Btn('', image_filename='./assets/image_3.png',
                        button_color='#F5F5FA', image_subsample=3, border_width=0),
                 sg.Btn('', image_filename='./assets/image_2.png',
                        button_color='#F5F5FA', image_subsample=3, border_width=0)],
                ],
                background_color='#F5F5FA',
               )
count = 0
flag = 1


def listen():
    while True:
        global flag
        global values
        global min_num
        event, values = wd.read()
        print(event)
        if event == sg.WIN_CLOSED or event == '0':
            flag = 0
            sg.popup(values[1])
            wd.close()
            break
        else:
            flag = 2
            if values[2]:
                min_num = np.random.randint(0,1440)
            else:
                min_num = np.random.rayleigh(scale=30)
            wd['txt'].update('设定完毕')


def countdown():
    while flag:
        global count
        time.sleep(1)
        count += 1


# def beep():
#     for i in range(3):
#         winsound.Beep(600, 800)
#         time.sleep(0.6)


def popup(value):
    sg.popup(value)


def listen_shutdown():
    while True:
        global count
        global min_num
        global flag
        time.sleep(1)
        if count >= 5 and flag == 2:
            sg.popup(values[1])
#             b = threading.Thread(target=beep)
#             p = threading.Thread(target=popup, args=[values[1]])
#             b.start()
#             p.start()
            flag = 0
            break



l = threading.Thread(target=listen)
c = threading.Thread(target=countdown)
s = threading.Thread(target=listen_shutdown)
l.start()
c.start()
s.start()
