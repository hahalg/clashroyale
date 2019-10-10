# -*- coding: utf-8-*-  

import time
from os.path import dirname, join
import win32api
import win32gui
#import win32ui
#from ctypes import windll
import win32con
import configparser 

class CONFS:
    curdir = dirname(__file__)
    img = {}
    
    box_types = ['90m','3h','4h','6h','8h','12h','12h1','blank','opennow']
    box_time = ['h','min','sec','open']
    for m in (box_types + box_time):
        img[m] = f'{curdir}\\img\\time_{m}.png'

    img_types = ['applogo','battle','battle1','start_unlock','onclick','close','ok','bwx','wrx','wbx','loginBT','retrylogin','tryagain']
    for mtype in img_types:
        img[mtype] = f'{curdir}\\img\\{mtype}.png'

    card_items = ['bd','hunter','mk','bb','mh','zap','guards','cc']
    img['card'] = {}
    for item in card_items:
        img['card'][item] = f'{curdir}\\img\\b_{item}.png'

    game_items = ['Set','TrainingCamp','Yes','royale_red','royale_blue','winner_red','winner_blue','do_battle']
    # img['game'] = {}
    for item in game_items:
        img[item] = f'{curdir}\\img\\{item}.png'

    conf = configparser.ConfigParser()
    if len(conf.read(f'{curdir}\\config.ini'))<1:
        game_area_width = 403
        game_area_height = 716
        game_box_top = 514
        game_box_bottom = 645
        game_box_width = 92
        game_box_height = 114
        game_box_space = 10

        #app的位置
        app_left = 899
        app_top = 5
        app_width = 416
        app_height = 751

        app_cmd = {
            'exe':'C:\\Users\\sq\\AppData\\Local\\Android\\Sdk\\emulator\\emulator.exe',    
            'params':'-avd sq_Pixel_2_API_28 -netfast',
            'dir':'C:\\Users\\sq\\AppData\\Local\\Android\\Sdk\\emulator\\',
            }
    else:
        game_area_width = conf.getint('game','area_width')
        game_area_height = conf.getint('game','area_height')
        game_box_top = conf.getint('game','box_top')
        game_box_bottom = conf.getint('game','box_bottom')
        game_box_width = conf.getint('game','box_width')
        game_box_height = conf.getint('game','box_height')
        game_box_space = conf.getint('game','box_space')

        #app的位置
        app_left = conf.getint('app','left')
        app_top = conf.getint('app','top')
        app_width = conf.getint('app','width')
        app_height = conf.getint('app','height')

        app_cmd = {
            'exe':conf.get('app','exe'),    
            'params':conf.get('app','params'),
            'dir':conf.get('app','dir'),
            }
        windowTitle = conf.get('app','name')

    def __init__(self,windowTitle=None):
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        # print('system:',params)
        if windowTitle == None :
            windowTitle = self.windowTitle
        else:
            self.windowTitle = windowTitle
            # exit(0)
        self.hwnd = win32gui.FindWindow(win32con.NULL,windowTitle)
        if self.hwnd == 0 :
            print('%s not found' % windowTitle)
            self.startApp()
        # win32gui.SetForegroundWindow(self.hwnd)
        self.getWindowWH()
        if self.window_width!= self.app_width:
            print('resize APP window!')
            self.resizeAPP()
            self.getWindowWH()
        # if min(window_left,window_top) < 0:
            # or window_right > self.screen_width']\
            # or window_bottom > self.screen_height']:
            # errExit('window is at wrong position')
            # CLASHROYALE.errExit(des=params)
            # print('params err!')
            # exit(-1)
            

        self.game_area_left = self.window_left + 8
        self.game_area_top = self.window_top + 34
        self.game_area_right = self.game_area_left + self.game_area_width
        self.game_area_bottom = self.game_area_top + self.game_area_height

    def resizeAPP(self):
        win32gui.SetWindowPos(
            self.hwnd,win32con.HWND_TOP , 
            self.app_left, self.app_top, self.app_width, self.app_height,
            win32con.SWP_SHOWWINDOW
        )
    def getWindowWH(self):
        window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(self.hwnd)
        print('game状态：',end=' ')
        print(window_left,window_top,window_right,window_bottom)
        self.window_width = window_right - window_left
        self.window_height = window_bottom - window_top
        print('width:',self.window_width,'height:',self.window_height)
        self.window_top = window_top
        self.window_left = window_left

    def startApp(self):
        win32api.ShellExecute(0,'open',self.app_cmd['exe'],self.app_cmd['params'],self.app_cmd['dir'],1)
        print('start: '+ str(self.app_cmd))
        time.sleep(10)
        self.hwnd = win32gui.FindWindow(win32con.NULL,self.windowTitle)
        self.resizeAPP()

if __name__ == '__main__':
    print('start:'+"-"*20)
    # game = CONFS('Android Emulator - sq_Pixel_2_API_24:5554')
    # game = CONFS('Android Emulator - sq_Pixel_2_API_28:5554')
    game = CONFS()
    print(game.curdir)
    print(game.windowTitle)
    print(game.img['h'])
    game.resizeAPP()
