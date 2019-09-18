# -*- coding: utf-8-*-  

import os,time
import win32api
import win32gui
#import win32ui
#from ctypes import windll
import win32con

class CONFS:
    # cwd = os.getcwd()+'\\cheat\\clashroyale'
    cwd = os.getcwd()
    if 'clashroyale' not in cwd:
        cwd = cwd+'\\clashroyale'
    '''
    img_applogo = f'{cwd}\\img\\applogo.png'
    img_battle = f'{cwd}\\img\\battle.png'
    img_open = f'{cwd}\\img\\time_open.png'
    img_startunlock = f'{cwd}\\img\\start_unlock.png'
    img_onclick = f'{cwd}\\img\\onclick.png'
    img_close = f'{cwd}\\img\\close.png'
    img_ok = f'{cwd}\\img\\ok.png'

    img_h = f'{cwd}\\img\\time_h.png'
    img_min = f'{cwd}\\img\\time_min.png'
    img_sec = f'{cwd}\\img\\time_sec.png'
    '''
    img = {}
    
    box_types = ['90m','3h','4h','6h','8h','12h','blank','opennow']
    for mtype in box_types:
        img[mtype] = f'{cwd}\\img\\time_{mtype}.png'
        # exec(f'img_{mtype} = \'{cwd}\img\\\\time_{mtype}.png\'')

    box_time = ['h','min','sec','open']
    for mtype in box_time:
        img[mtype] = f'{cwd}\\img\\time_{mtype}.png'

    img_types = ['applogo','battle','start_unlock','onclick','close','ok','bwx','wrx','loginBT']
    for mtype in img_types:
        img[mtype] = f'{cwd}\\img\\{mtype}.png'

    game_items = ['bd','hunter','mk','bb','mh','zap','guards','cc']
    img['card'] = {}
    for item in game_items:
        img['card'][item] = f'{cwd}\\img\\b_{item}.png'


    game_area_width = 403
    game_area_height = 716
    game_box_top = 514
    game_box_bottom = 645
    game_box_width = 92
    game_box_height = 114
    game_box_space = 10      #10

    app_left = 899
    app_top = 5
    app_width = 416
    app_height = 751

    app_cmd = {'exe':'C:\\Users\\sq\\AppData\\Local\\Android\\Sdk\\emulator\\emulator.exe',
    'params':'-avd sq_Pixel_2_API_28 -netfast',
    'dir':'C:\\Users\\sq\\AppData\\Local\\Android\\Sdk\\emulator\\'}

    def __init__(self,window_title):
        
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        # print('system:',params)
        self.hwnd = win32gui.FindWindow(win32con.NULL,window_title)
        if self.hwnd == 0 :
            print('%s not found' % window_title)
            self.startApp(window_title)
            # exit(0)
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

    def startApp(self,window_title):
            # os.system(self.app_cmd)
            # win32api.ShellExecute(0, 'open', r'C:\\Users\\Administrator\\AppData\\Local\\Android\\Sdk\\emulator\\emulator.exe', ' -avd sq_Pixel_2_API_24 -netfast','C:\\Users\\Administrator\\AppData\\Local\\Android\\Sdk\\emulator\\',1)
            win32api.ShellExecute(0,'open',self.app_cmd['exe'],self.app_cmd['params'],self.app_cmd['dir'],1)
            print('start: '+ str(self.app_cmd))
            time.sleep(10)
            self.hwnd = win32gui.FindWindow(win32con.NULL,window_title)
            self.resizeAPP()


if __name__ == '__main__':
  
    print('start:'+"-"*20)
    # game = CLASHROYALE('Android Emulator - sq_Pixel_2_API_28:5554')
    # game = CONFS('Android Emulator - sq_Pixel_2_API_24:5554')
    game = CONFS('Android Emulator - sq_Pixel_2_API_28:5554')
    a = 'app_cmd'
    print(game)
