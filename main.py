# -*- coding: utf-8-*-  
# clash royale
# auto to open box
# author: LG
# date: 20190806
import os,cv2,sys
# import PIL.ImageGrab
from PIL import ImageGrab,Image
import pyautogui
import win32gui,win32api
import win32con
import numpy as np
import time,random
import config
import curses
from ocr import ocr
from sq_waitakey_lib import WAITAKEY
# from sq_grab_lib import grabAPP
from subprocess import call
class CLASHROYALE(WAITAKEY):
    auto = False    #是否自动执行
    def __init__(self,windowTitle):
        super(CLASHROYALE,self).__init__()
        # self.stdscr = curses.initscr()
        # self.initCurses()
        self.windowTitle = windowTitle
        self.getWindow()
        self.autoRun()

    def getWindow(self):
        '''得到窗口相关信息'''
        self.game_params = config.CONFS(self.windowTitle)
        self.putTop()

    def putTop(self):
        if self.auto:
            try:
                win32api.keybd_event(0,0,0,0)
                win32gui.SetForegroundWindow(self.game_params.hwnd)
            except:
                #start emulator
                self.game_params.startApp(self.windowTitle)
                time.sleep(5)
                self.runApp()
    
        else:
            win32api.keybd_event(0,0,0,0)
            win32gui.SetForegroundWindow(self.game_params.hwnd)

    def runApp(self):
        #run clash royale
        if self.clickBT('applogo'):
            time.sleep(20)
            #loginBT      #bwx      #wrx
            img_bts = ['loginBT','bwx','wrx']
            for imgbt in img_bts:
                if self.clickBT(imgbt):
                    time.sleep(15)
        else:
            print('run app err!')

    def clickBT(self,imgname=None,grabscreen=True,threshold=0.8):
        if imgname is None:
            return False
        if grabscreen:
            self.updateImgbg()
        img_bt = cv2.imread(self.game_params.img[imgname])
        is_,pos_ = self.inHere(img_bt,self.imgbg,threshold)
        if is_:
            x,y = pos_[0]
            cx = self.game_params.game_area_left + x + img_bt.shape[1]/2
            cy = self.game_params.game_area_top + y + img_bt.shape[0]/2
            pyautogui.moveTo(cx,cy,duration=0.5)
            pyautogui.click(cx,cy)
            return True
        else:
            # print('not find img '+imgname,self.game_params.img[imgname])
            return False


    @staticmethod
    def errExit(des='err!',ecode=-1):
        print(des)
        exit(ecode)

    def battleWindow(self):
        '''得到战斗界面'''
        self.clickWindow()  #是否有可点的主界面消息

        img_battle = cv2.imread(self.game_params.img['battle'])
        is_battle,pos_battle = self.inHere(img_battle,self.imgbg)

        if not is_battle:
            oldpos = pyautogui.position()
            self.clickBT('battle1',False)
            pyautogui.moveTo(oldpos)
            time.sleep(2)

    def updateImgbg(self):
        game_area_image = self.grabScreen(self.game_params.game_area_left,          self.game_params.game_area_top,self.game_params.game_area_right,        self.game_params.game_area_bottom)
        # game_area_image.show()  #如程序在第二屏则截图是全黑
        self.imgbg = cv2.cvtColor(np.asarray(game_area_image),cv2.COLOR_RGB2BGR)

    def clickWindow(self):
        '''点击无用的系统必须的点击事件'''
        oldpos = pyautogui.position()
        self.updateImgbg()
        isSleep = False
        clicks = ['close','ok','wrx']        #要加入try again事件
        for c in clicks:
            if self.clickBT(c,False):
                isSleep = True
                time.sleep(2)

        #主窗口事件
        img_bot = self.grabScreen(
            self.game_params.game_area_left,
            self.game_params.game_area_top+self.game_params.game_box_bottom,self.game_params.game_area_right,
            self.game_params.game_area_top+self.game_params.game_area_height)
        # img_bot.show()
        img_bot = cv2.cvtColor(np.asarray(img_bot),cv2.COLOR_RGB2BGR)
        img_click = cv2.imread(self.game_params.img['onclick'])
        is_click,spos = self.inHere(img_click,img_bot,0.5)
        if is_click:
            x,y = spos[0]
            cx = self.game_params.game_area_left + x
            cy = self.game_params.game_area_top + self.game_params.game_box_bottom + y
            pyautogui.click(cx,cy)
            isSleep = True
            time.sleep(3)
        else:
            print('no message.')
            # exit(0)
        if isSleep :
            # time.sleep(3)
            self.updateImgbg()
        pyautogui.moveTo(oldpos)




    def grabScreen(self,left,top,right,bottom):
        return ImageGrab.grab((left,top,right,bottom))
        # return grabAPP(self.game_params.hwnd,left,top,right,bottom)

    
    def inHere(self,img1,img2,threshold=0.8):
        '''判断img1是否在img2中，返回True or False'''
        if img1 is None or img2 is None :
            print('None file!')
            return None,{}
        # w,h = 60,20
        # 获取偏移量
        res = cv2.matchTemplate(img1,img2, cv2.TM_CCOEFF_NORMED)  # 查找block图片在template中的匹配位置，result是一个矩阵，返回每个点的匹配结果
        # print('result:',result)
        #设定阈值
        # threshold = 0.8
        loc = np.where( res >= threshold)
        result = False
        mpt = []
        for pt in zip(*loc[::-1]):
            result = True
            mpt.append(pt)
            # break
            # print('pt:',pt)
            # 画出方框
            # cv2.rectangle(img2, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
        #显示图像   
        # cv2.imshow('Detected',img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('inhere: ',result)
        return result,mpt

    
    def analysisCron(self,img):
        '''分析img里的情况'''
        crontable = {}
        img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
        # 4个宝箱是否存在，是否有空，是否有时间完成未打开的
        box_status = self.getBoxStatus(img)
        if len(box_status)<4 :
            crontable['sleep'] = 20
            crontable['err'] = 'box err!'
            # crontable['notice'] = str(self.game_params.game_area_width)+' X '+str(self.game_params.game_area_height)+' OK?'
            crontable['notice'] = str(box_status)
            print('box err!',box_status)
            return crontable
        do_now = False
        for i in range(4):
            n = i+1
            # print(n,box_status[n])
            for mtype in self.game_params.box_types:
                if box_status[n] == mtype:
                    # print(mtype)
                    if mtype=='opennow':
                        do_now = True
                        do_n = n
                    # crontable.append({'seat':n,'do':mtype})
                    crontable['s'+ str(n)] = mtype
                    # self.startUnlock(n)


        # 是否有进行中的情况，有的话计算剩余时间
        if do_now:
            print('\topen now! time:')
            img_sec = cv2.imread(self.game_params.img['sec'])
            is_have,point_type = self.inHere(img_sec,self.imgbg)
            if not is_have:
                # crontable.append({'sleep':3600})
                crontable['sleep'] = 3600
            else:
                # crontable.append({'sleep':60})
                # 截图时间
                time_img = self.grabScreen(
                    self.game_params.game_area_left+(self.game_params.game_box_space+self.game_params.game_box_width)*(do_n-1)+25,
                    self.game_params.game_area_top+self.game_params.game_box_top+4,self.game_params.game_area_left+(self.game_params.game_box_space+self.game_params.game_box_width)*(do_n-1)+97,
                    self.game_params.game_area_top+self.game_params.game_box_top+20)
                # time_img.show()
                # ocr
                sleep_str = ocr(time_img)
                # print(sleep_str)
                s_pos = sleep_str.find('min')
                try:
                    if s_pos>0:
                        sleep_min = int(sleep_str[:s_pos])
                        if sleep_min >59:
                            sleep_time = 60
                        else:
                            sleep_time = sleep_min * 60
                        # print(s_pos,sleep_time)
                    else:
                        sleep_time = 10
                except BaseException as identifier:
                    sleep_time = 60
                crontable['sleep'] = sleep_time
        else:
            # crontable.append({'sleep':10})
            crontable['sleep'] = 60
            for i in range(4):
                if crontable['s'+str(i+1)]!= 'blank':
                    self.startUnlock(i+1)
                    break

        for item in crontable:
            print('\t',item,crontable[item])

        # 对比现在的时间，合理安排开箱次序
        m_str = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())

        # 返回时间次序表
        # crontable.append({'time':m_str})
        crontable['time'] = m_str
        return crontable

    
    def getBoxStatus(self,imgbg):
        '''返回4个箱子的情况'''

        box_status = {}
        img_open = cv2.imread(self.game_params.img['open'])
        # cv2.imshow('',img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # self.imgbg = img

        # 到时间的箱子
        is_open,open_point = self.inHere(img_open,imgbg)
        if is_open:
            print('Box is ready!go!',open_point)
            x,y = open_point[0]
           
            cx = self.game_params.game_area_left+x
            cy = self.game_params.game_area_top+self.game_params.game_box_top+y
            # print(cx,cy)q
            pyautogui.moveTo(cx,cy,duration=0.5)
            for i in range(16):
                pyautogui.click(cx,cy)
                time.sleep(0.5)

        def getBoxSeat(mpoint,mstr):
            for i in range(len(mpoint)):
                x,y = mpoint[i]
                n = self.getSeat(x)
                box_status[n] = mstr
                # print(mstr,n)

        img_type = None
        is_have = None
        point_type = None
        # img_file = []
        for mtype in self.game_params.box_types:
            # print(self.game_params.img[mtype])
            # exec(f'img_file.append(self.game_params.img_{mtype})')
            img_type = cv2.imread(self.game_params.img[mtype])
            # img_type = cv2.imread(img_file.pop())
            if mtype=='opennow':
                is_have,point_type = self.inHere(img_type,imgbg,0.5)
            else:
                is_have,point_type = self.inHere(img_type,imgbg)
            if is_have:
                getBoxSeat(point_type,mtype)
        # box_status_r = sorted(box_status.items(),key=lambda x:x[0])
        # print(len(box_status),box_status)
        # print(box_status[1],box_status[2],box_status[3],box_status[4],)
        return box_status

    
    def startUnlock(self,n=1):
        '''解锁第n个宝箱'''
        # res = True
        if n<1 or n>4 :
            return False
        cx = self.game_params.game_area_left+(self.game_params.game_box_space+self.game_params.game_box_width)*(n-1)+self.game_params.game_box_width/2
        cy = self.game_params.game_area_top+self.game_params.game_box_top+self.game_params.game_box_height/2
        pyautogui.click(cx,cy)
        time.sleep(0.5)
        '''
        self.imgbg = self.grabScreen(self.game_params.game_area_left,self.game_params.game_area_top,self.game_params.game_area_right,self.game_params.game_area_bottom)
        # self.imgbg.show()
        self.imgbg = cv2.cvtColor(np.asarray(self.imgbg),cv2.COLOR_RGB2BGR)
        img_startunlock = cv2.imread(self.game_params.img['start_unlock'])
        # cv2.imshow('',img_startunlock)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()        
        is_start,start_point = self.inHere(img_startunlock,self.imgbg,0.6)
        if is_start:
            print(f'start unlock box {n}.')
            x,y = start_point[0]
            cx = self.game_params.game_area_left+x
            cy = self.game_params.game_area_top+y
            print(cx,cy)
            pyautogui.moveTo(cx,cy,duration=0.5)
            pyautogui.click(cx,cy)
        else:
            print(f'unlock {n} box failed!')
            res = False
        '''
        if not self.clickBT('start_unlock',True,0.6):
            print(f'unlock {n} box failed!')
            return False
        return True

    
    def getSeat(self,pos):
        '''根据pos返回箱子位置，1234'''
        n = int(pos/(self.game_params.game_box_width+self.game_params.game_box_space))+1
        return n

    def analy(self):
        '''分析宝箱时间'''
        # 截图：宝箱情况
        game_cron_img = self.grabScreen(
            self.game_params.game_area_left,
            self.game_params.game_area_top+self.game_params.game_box_top,self.game_params.game_area_right,
            self.game_params.game_area_top+self.game_params.game_box_bottom)
        # game_cron_img.show()
        # 分析时间
        m_str = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
        print(m_str)
        cron_table = self.analysisCron(game_cron_img)
        return cron_table
    
    def flashBoxStatus(self):
        self.putTop()
        self.battleWindow()
        cron_table = self.analy()
        i = 2
        # self.showTime(i,5,'cron_table[item]')
        mstyle = random.randint(1,4)    #随机样式
        hspace = 8  #前面空格
        for item in cron_table:
            i = i+1
            mstr = str(item).rjust(10)+'\t'+str(cron_table[item]).ljust(30)
            # mstr = mstr + ' '*(50-len(mstr))
            self.showTime(i,hspace,mstr,mstyle)
        self.waitSec = cron_table["sleep"]
        # self.waitTime()

    def timeOut(self):
        # print('here!!!!!')
        if self.go:
            self.flashBoxStatus()
            if self.waitSec < 1:
                self.e.set()
                return
            else:
                self.waitTime()

    def autoRun(self):
        self.auto = not self.auto
        self.showTime(1,4,'auto model:'+str(self.auto).ljust(5))

if __name__ == '__main__':
  
    print('start:'+"-"*20)
    # game = CLASHROYALE('Android Emulator - sq_Pixel_2_API_28:5554')
    game = CLASHROYALE('Android Emulator - sq_Pixel_2_API_28:5554')
    
    spos = pyautogui.position()
    game.battleWindow()
    cron_table = game.analy()
    pyautogui.moveTo(spos)
    if cron_table["sleep"] > 0 :
        print(f'wait {cron_table["sleep"]}s ')
        # m_mstr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
        m_mstr = 'press \'q\' to quit,\'r\' to reload box. \'a\' to auto. Reflash after '
        acts = {
            'a':'self.autoRun()',
            'r':'self.flashBoxStatus()',
                }
        game.setStr(m_mstr)
        game.setSec(cron_table["sleep"])
        game.setActs(acts)
        game.startWait()            

        # print('\nloop','='*20)


