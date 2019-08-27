# -*- coding: utf-8-*-  

import os
import win32api
import win32gui
import win32con

class CONFS:
    cwd = os.getcwd()
    if 'clashroyale' not in cwd:
        cwd = cwd+'\\clashroyale'

    img_battle = f'{cwd}\\img\\battle.png'
    img_open = f'{cwd}\\img\\time_open.png'
    img_startunlock = f'{cwd}\\img\\start_unlock.png'

    img_h = f'{cwd}\\img\\time_h.png'
    img_min = f'{cwd}\\img\\time_min.png'
    img_sec = f'{cwd}\\img\\time_sec.png'
    
    box_types = ['90m','3h','4h','6h','8h','12h','blank','opennow']
    for mtype in box_types:
        # exec(f'self.img_{mtype} = f\'{self.cwd}\\img\\\\time_{mtype}.png\'')
        exec(f'img_{mtype} = f\'{cwd}\\img\\\\time_{mtype}.png\'')

    # print(img_3h)

    game_area_width = 417   #412
    game_area_height = 741  #730
    game_box_top = 532      #530
    game_box_bottom = 662   #656
    game_box_width = 95     #94
    game_box_height = 118   #116
    game_box_space = 10

    def __init__(self,window_title):


        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        self.hwnd = win32gui.FindWindow(win32con.NULL,window_title)
        if self.hwnd == 0 :
            print('%s not found' % window_title)
            exit(-1)
        window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(self.hwnd)
        if min(window_left,window_top) < 0: #判断是否超出屏幕，可不用
            # or window_right > self.screen_width']\
            # or window_bottom > self.screen_height']:
            # errExit('window is at wrong position')
            print('err!')
            exit(-1)
        self.window_width = window_right - window_left
        self.window_height = window_bottom - window_top

        self.game_area_left = window_left + 9   #左侧边缘
        self.game_area_top = window_top + 32    #顶部边缘
        self.game_area_right = self.game_area_left + self.game_area_width
        self.game_area_bottom = self.game_area_top + self.game_area_height

if __name__ == '__main__':
    windowTitle = 'Android Emulator - sq_Pixel_2_API_28:5554'
    game = CONFS(windowTitle)
    print(game.img_3h)
    print(game)