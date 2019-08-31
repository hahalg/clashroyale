# -*- coding: utf-8-*-  

import os
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

    img_battle = f'{cwd}\\img\\battle.png'
    img_open = f'{cwd}\\img\\time_open.png'
    img_startunlock = f'{cwd}\\img\\start_unlock.png'
    img_onclick = f'{cwd}\\img\\onclick.png'
    img_close = f'{cwd}\\img\\close.png'
    img_ok = f'{cwd}\\img\\ok.png'

    img_h = f'{cwd}\\img\\time_h.png'
    img_min = f'{cwd}\\img\\time_min.png'
    img_sec = f'{cwd}\\img\\time_sec.png'
    
    box_types = ['90m','3h','4h','6h','8h','12h','blank','opennow']
    for mtype in box_types:
        exec(f'img_{mtype} = \'{cwd}\img\\\\time_{mtype}.png\'')
    
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

    def __init__(self,window_title):
        
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        # print('system:',params)
        self.hwnd = win32gui.FindWindow(win32con.NULL,window_title)
        if self.hwnd == 0 :
            print('%s not found' % window_title)
            exit(-1)
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
            self.hwnd,win32con.HWND_BOTTOM, 
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


        


if __name__ == '__main__':
  
    print('start:'+"-"*20)
    # game = CLASHROYALE('Android Emulator - sq_Pixel_2_API_28:5554')
    game = CONFS('Android Emulator - sq_Pixel_2_API_24:5554')
