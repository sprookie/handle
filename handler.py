import PySimpleGUI as sg
import pandas as pd
import os
import time
import numpy as np
import threading

wd = sg.Window('cyber_head',
               [[sg.Text('')],
                [sg.Input()],
                [sg.Checkbox('豪放模式'),sg.Checkbox('人性模式')],
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
        print(count)
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


def countdown():
    while flag:
        global count
        time.sleep(1)
        count += 1
        print(count)

def listen_shutdown():
    while True:
        global count
        global flag
        global min_num
        print(count)
        time.sleep(1)
        if count >= min_num * 60:
            flag = 0
            sg.popup(values[0])
            wd.close()
            break
if __name__ == '__main__':            
    l.start()
    c.start()
    s.start()
    l = threading.Thread(target=listen)
    c = threading.Thread(target=countdown)
    s = threading.Thread(target=listen_shutdown)
