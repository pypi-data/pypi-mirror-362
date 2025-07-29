import multiprocessing
import pygame
from shared_memory_dict import SharedMemoryDict

import pickle
import os

smd = SharedMemoryDict(name='data', size=1024)
smd["Active"] = False
smd["Hit"]= False
smd["Pos"] = False
smd["Players"] = False
smd["Screen"] = False
smd["RGB"] = False
smd["Temp"] = False
smd["Action"] = False
smd["Buttons"] = False


path = os.path.realpath(__file__)
path = path.replace('functions.py', '')


def get_path():
    return path


def screenshot_refresh():
    try:
        q = smd["Screen"]
        if q != False:
            smd["Screen"] = False
            return True
        else:
            return False
    except:
        return False


def take_screenshot(screen):
    try:
        os.remove(os.path.join(path, "screencapture.jpg"))
    except:
        pass
    pygame.image.save(screen, os.path.join(path, "screencapture.jpg"))
    smd["Screen"] = True


def game_isactive():
    smd = SharedMemoryDict(name='data', size=1024)
    try:
        return smd["Active"]
    except:
        return True

def close_game():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Active"]=False

def open_game():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Active"] = True


def clear_pickle(filename, val):
    file = open((os.path.join(path, filename)), 'wb')
    pickle.dump(val, file)
    file.close()


def put_pos(pos):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Pos"]=pos


def get_size():
    return (1360, 768)


def get_pos():
    smd = SharedMemoryDict(name='data', size=1024)
    return smd["Pos"]


def put_temp(temp):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Temp"]=temp


def get_temp():
    smd = SharedMemoryDict(name='data', size=1024)
    return smd["Temp"]


def put_button_names(names):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Buttons"]=names


def get_button_names():
    smd = SharedMemoryDict(name='data', size=1024)
    return smd["Buttons"]


def put_hit():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Hit"]=True


def hit_detected():
    smd = SharedMemoryDict(name='data', size=1024)
    try:
        if smd["Hit"]==True:
            smd["Hit"] = False
            return True
        else:
            return False
    except:
        return False


def get_action():
    smd = SharedMemoryDict(name='data', size=1024)
    try:
        action=smd["Action"]
        smd["Action"]=False
        return action
    except:
        return False


def put_action(number):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Action"]=number

def put_playernames(playernames):
    file = open((os.path.join(path, "hmplayers")), 'wb')
    pickle.dump(playernames, file)
    file.close()


def get_playerstatus():
    try:
        file = open((os.path.join(path, "hmplayers")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            return q
        else:
            return False
    except:
        return False

def get_playernames():
    try:
        file = open((os.path.join(path, "hmplayers")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            w = []
            for i in range(0, len(q)):
                if q[i][1] == True:
                    w.append(q[i][0])
            return w
        else:
            return False
    except:
        return False





