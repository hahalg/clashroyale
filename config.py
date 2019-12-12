# -*- coding: utf-8-*-  

import time
from os.path import dirname
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

    img_types = ['applogo','battle','battle1','start_unlock','onclick']
    img_cancel = ['close','ok','bwx','wrx','wbx','loginBT','retrylogin','retrylogin1','tryagain']
    for mtype in (img_types + img_cancel):
        img[mtype] = f'{curdir}\\img\\{mtype}.png'

    # game_items = ['bd','hunter','mk','bb','mh','zap','guards','cc']
    # img['card'] = {}
    # for item in game_items:
    #     img['card'][item] = f'{curdir}\\img\\b_{item}.png'

    card_items = ['bd','hunter','mk','bb','mh','zap','guards','cc']
    img['card'] = {}
    for item in card_items:
        img['card'][item] = f'{curdir}\\img\\b_{item}.png'
    game_items = ['Set','TrainingCamp','Yes','royale_red','royale_blue','winner_red','winner_blue','do_battle']
    # img['game'] = {}
    for item in game_items:
        img[item] = f'{curdir}\\img\\{item}.png'


    def __init__(self,windowTitle=None):
        print('dir:',self.curdir)
        self.loadConfig()
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        # print('system:',params)
        if windowTitle is None :
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
            

        self.game_area_left = self.window_left + self.game_left_space
        self.game_area_top = self.window_top + self.game_top_space
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
        print('start: '+ str(self.app_cmd) + ' wait ',self.exe_time,'s')
        time.sleep(self.exe_time)
        self.hwnd = win32gui.FindWindow(win32con.NULL,self.windowTitle)
        self.resizeAPP()

    def loadConfig(self):
        conf = configparser.ConfigParser()
        if len(conf.read(f'{self.curdir}\\config.ini'))<1:
            '''
            self.game_area_width = 403
            self.game_area_height = 716
            self.game_box_top = 514
            self.game_box_bottom = 645
            self.game_box_width = 92
            self.game_box_height = 114
            self.game_box_space = 10

            #app的位置
            self.app_left = 899
            self.app_top = 5
            self.app_width = 416
            self.app_height = 751

            self.app_cmd = {
                'exe':'C:\\Users\\sq\\AppData\\Local\\Android\\Sdk\\emulator\\emulator.exe',    
                'params':'-avd sq_Pixel_2_API_28 -netfast',
                'dir':'C:\\Users\\sq\\AppData\\Local\\Android\\Sdk\\emulator\\',
                }
            '''
            print(f'{self.curdir}\\config.ini is not find!')
            exit(-1)
        else:
            self.game_area_width = conf.getint('game','area_width')
            self.game_area_height = conf.getint('game','area_height')
            self.game_top_space = conf.getint('game','top_space')
            self.game_left_space = conf.getint('game','left_space')
            self.game_box_top = conf.getint('game','box_top')
            self.game_box_bottom = conf.getint('game','box_bottom')
            self.game_box_width = conf.getint('game','box_width')
            self.game_box_height = conf.getint('game','box_height')
            self.game_box_space = conf.getint('game','box_space')

            #app的位置
            self.app_left = conf.getint('app','left')
            self.app_top = conf.getint('app','top')
            self.app_width = conf.getint('app','width')
            self.app_height = conf.getint('app','height')

            self.app_cmd = {
                'exe':conf.get('app','exe'),    
                'params':conf.get('app','params'),
                'dir':conf.get('app','dir'),
                }
            self.windowTitle = conf.get('app','name')
            self.offset_time_left = conf.getint('offset','time_left')
            self.offset_time_top = conf.getint('offset','time_top')
            self.offset_time_right = conf.getint('offset','time_right')
            self.offset_time_bottom = conf.getint('offset','time_bottom')

            self.exe_time = conf.getint('common','exe_time')
            self.app_time = conf.getint('common','app_time')
            self.debug = conf.getint('common','debug')

if __name__ == '__main__':
    print('start:'+"-"*20)
    # game = CONFS('Android Emulator - sq_Pixel_2_API_24:5554')
    # game = CONFS('Android Emulator - sq_Pixel_2_API_28:5554')
    game = CONFS()
    print(game.curdir)
    print(game.windowTitle)
    print(game.img['h'])
    game.resizeAPP()
