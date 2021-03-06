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

class WAITAKEYELSE(WAITAKEY):
    def timeOut(self):
        # 时间到了就关闭游戏进程
        m_timestr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
        if self.go:
            m_str = ' kill blue game!'
            print(m_timestr,m_str)
            self.showTime(9,4,m_timestr+m_str)
            os.system(r'taskkill /fi "imagename eq blue*" /f >nul && taskkill /fi "imagename eq hd-*" /f >nul')
            self.go = False
        else:
            print('ESC!')
        self.showTime(self.x,self.y,' '*60)
        self.stopWait()
        return True

    # def __del__(self):
    #     m_str = '=> del '+self.__class__.__name__+' '+time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
    #     print(m_str)
    #     self.showTime(9,4,m_str)


class CLASHROYALE(WAITAKEY):
    auto = False    #是否自动执行
    mstyle = 1      #显示风格、字体、颜色等
    showHelpStatus = False #显示help
    actStaus = []   #下一步状态
    def __init__(self,windowTitle=None):
        super(CLASHROYALE,self).__init__()
        self.game_params = config.CONFS(windowTitle)
        self.putTop()
        self.autoRun()

    def putTop(self):
        if self.auto:
            try:
                win32api.keybd_event(0,0,0,0)
                win32gui.SetForegroundWindow(self.game_params.hwnd)
            except:
                #start emulator
                self.game_params.startApp()
                time.sleep(5)
                self.runApp()
    
        else:
            win32api.keybd_event(0,0,0,0)
            win32gui.SetForegroundWindow(self.game_params.hwnd)

    def runApp(self):
        #run clash royale
        is_,pos_ = self.clickBT('applogo')
        if is_:
            # time.sleep(30)
            self.cron_table['sleep'] = 30
        else:
            print('Not find app logo!')
        self.clickWindow()


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
            pyautogui.moveTo(cx,cy)
            pyautogui.click(cx,cy)
            if self.game_params.debug == 1:
                print('\t',imgname,'clicked!')

            return True,[cx,cy]
        else:
            # print('not find img '+imgname,self.game_params.img[imgname])
            return False,[0,0]


    def battleWindow(self):
        '''得到战斗界面'''
        self.clickWindow()  #是否有可点的主界面消息

        img_battle = cv2.imread(self.game_params.img['battle'])
        is_battle,pos_battle = self.inHere(img_battle,self.imgbg)

        if not is_battle:
            oldpos = pyautogui.position()
            self.waitSec = 20
            is_,pos_ = self.clickBT('battle1',False)
            if not is_:
                m_str = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
                print(m_str,'not in game?',end=' ')
                is__,pos__ = self.clickBT('applogo',False)
                if is__:
                    print('=> START GAME...')
                    time.sleep(self.game_params.app_time)
                    self.game_params.resizeAPP()
                    time.sleep(5)
                else:
                    print('Not find game!')
            pyautogui.moveTo(oldpos)
            time.sleep(2)
        else:
            # 检查上面的任务是否有完成的
            # img_gafts = cv2.imread(self.game_params.img['gafts'])
            is_,pos_ = self.clickBT('gafts')
            if is_:
                time.sleep(0.5)
                is_,pos_ = self.clickBT('gaft1')
                if is_:
                    for i in range(10):
                        pyautogui.click(pos_[0],pos_[1])
                        time.sleep(0.5)
                self.clickWindow()


    def updateImgbg(self):
        game_area_image = self.grabScreen(self.game_params.game_area_left,          self.game_params.game_area_top,self.game_params.game_area_right,        self.game_params.game_area_bottom)
        # game_area_image.show()  #如程序在第二屏则截图是全黑
        self.imgbg = cv2.cvtColor(np.asarray(game_area_image),cv2.COLOR_RGB2BGR)

    def clickWindow(self):
        '''点击无用的系统必须的点击事件'''
        oldpos = pyautogui.position()
        self.updateImgbg()
        isSleep = False
        # clicks = ['loginBT','close','ok','wrx','bwx','wbx','retrylogin','tryagain'] 
        for c in self.game_params.img_cancel:
            is_,pos_ = self.clickBT(c,False)
            if is_:
                if self.game_params.debug == 1:
                    print('\t debug:',c,'clicked!')
                isSleep = True
                time.sleep(3)
                self.updateImgbg()

        #主窗口事件
        img_bot = self.grabScreen(
            self.game_params.game_area_left,
            self.game_params.game_area_top+self.game_params.game_box_bottom,self.game_params.game_area_right,
            self.game_params.game_area_top+self.game_params.game_area_height)
        # img_bot.show()
        img_bot = cv2.cvtColor(np.asarray(img_bot),cv2.COLOR_RGB2BGR)
        img_click = cv2.imread(self.game_params.img['onclick'])
        is_click,spos = self.inHere(img_click,img_bot,0.8)
        if is_click:
            x,y = spos[0]
            cx = self.game_params.game_area_left + x
            cy = self.game_params.game_area_top + self.game_params.game_box_bottom + y
            pyautogui.click(cx,cy)
            isSleep = True
            if self.game_params.debug == 1:
                print('\t','主窗口事件','clicked!')
            time.sleep(3)
        else:
            # print('no message.')
            pass
            # exit(0)
        if isSleep :
            # time.sleep(3)
            # self.updateImgbg()
            self.clickWindow()
        pyautogui.moveTo(oldpos)

    def grabScreen(self,left,top,right,bottom):
        img = ImageGrab.grab((left,top,right,bottom))
        # return grabAPP(self.game_params.hwnd,left,top,right,bottom)
        # img.show()
        return img
    
    def inHere(self,img1,img2,threshold=0.75,debug=False):
        '''判断img1是否在img2中，返回True or False'''
        if img1 is None or img2 is None :
            print('None file!')
            return None,{}
        w,h = img1.shape[:2]
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
            cv2.rectangle(img2, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
        if debug:
            # 显示图像   
            cv2.imshow(str(threshold),img2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print('inhere: ',result)
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
            # print('box err!',box_status,'wait',self.waitSec)
            self.game_params.resizeAPP()
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
        is_AllBlank = True
        if do_now:
            is_AllBlank = False
            # print('\topen now! time:')
            # img_sec = cv2.imread(self.game_params.img['sec'])
            img_h = cv2.imread(self.game_params.img['h'])
            # 截图时间
            time_img = self.grabScreen(
                self.game_params.game_area_left+(self.game_params.game_box_space+self.game_params.game_box_width)*(do_n-1)+self.game_params.offset_time_left,
                self.game_params.game_area_top+self.game_params.game_box_top+self.game_params.offset_time_top,
                self.game_params.game_area_left+(self.game_params.game_box_space+self.game_params.game_box_width)*(do_n-1)+self.game_params.offset_time_right,
                self.game_params.game_area_top+self.game_params.game_box_top+self.game_params.offset_time_bottom)
            if self.game_params.debug == 3:
                time_img.show()
            img_timebg = cv2.cvtColor(np.asarray(time_img),cv2.COLOR_RGB2BGR)
            is_have,point_type = self.inHere(img_h,img_timebg,0.88)
            if is_have:
                img_sec = cv2.imread(self.game_params.img['sec'])
                is_have,point_type = self.inHere(img_h,img_timebg,0.88) 
                if is_have:
                    crontable['sleep'] = 90
                else:
                    crontable['sleep'] = 3600
                    # print('\t'*3,'set 3600!')
            else:
                # crontable.append({'sleep':60})
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
                            sleep_time = sleep_min * 60 - 10
                        # print(s_pos,sleep_time)
                    else:
                        sleep_time = 10
                except BaseException as identifier:
                    sleep_time = 60
                crontable['sleep'] = sleep_time
                # print('\t'*3,'sleep time set ',sleep_time)
        else:
            # crontable.append({'sleep':10})
            crontable['sleep'] = 60
            for startn in self.game_params.box_types[:-2]:
                for i in range(4):
                    if crontable['s'+str(i+1)]== startn:
                        if self.startUnlock(i+1):
                            self.log_unlock(crontable,i+1)
                        crontable['sleep'] = 5
                        is_AllBlank = False
                        break
                if not is_AllBlank:
                    break

        if not is_AllBlank:
            for item in crontable:
                print('\t',item,crontable[item])
        else:
            # 如果4个箱子全为空
            crontable['sleep'] = 3600

        # 对比现在的时间，合理安排开箱次序
        m_str = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())

        # 返回时间次序表
        # crontable.append({'time':m_str})
        crontable['time'] = m_str
        return crontable

    def log_unlock(self,crontable,n):
        with open('openbox.log','a') as f:
            m_str = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
            try:
                m_str = f'{m_str} open {n},{crontable["notice"]}\n'
            except:
                m_str = f'{m_str} open {n},{crontable}\n'
            f.write(m_str)

    
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
            pyautogui.moveTo(cx,cy)
            for i in range(20):
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
                is_have,point_type = self.inHere(img_type,imgbg,0.4)
            else:
                is_have,point_type = self.inHere(img_type,imgbg,0.8)
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
        # print('move to ',cx,cy)
        pyautogui.moveTo(cx,cy,duration=0.2)
        pyautogui.click(cx,cy)
        time.sleep(0.5)
        is_,pos_ = self.clickBT('start_unlock',True,0.6)
        if not is_:
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
        self.cron_table = self.analysisCron(game_cron_img)
        return self.cron_table
    
    def flashBoxStatus(self):
        self.putTop()
        self.battleWindow()
        self.cron_table = self.analy()
        self.waitSec = self.cron_table["sleep"]
        # print('waitsec:',self.waitSec,self.cron_table)
        self.stdscr.clear()
        if self.waitSec > 400 and self.auto :
            #kill game's process
            # print(f'wait {self.waitSec} secs,kill game!')
            m_mstr = 'press "e" to end. It will kill game after '
            self.showTime(9,4,m_mstr)
            m_killgame = WAITAKEYELSE([1,2])
            m_killgame.key_quit = 'e'
            m_killgame.setStr(m_mstr)
            m_killgame.setSec(10)
            # m_killgame.setActs(acts)
            m_killgame.startWait()
            del m_killgame
        self.showBoxStatus()
        return self.cron_table

    
    def showBoxStatus(self):
        i = 2
        # self.mstyle = random.randint(1,4)    #随机样式
        self.mstyle = (self.mstyle + 1) % 4
        hspace = 6  #前面空格
        for item in self.cron_table:
            i = i+1
            mstr = str(item).rjust(10)+'\t'+str(self.cron_table[item]).ljust(35)
            self.showTime(i,hspace,mstr,self.mstyle)
        # self.waitTime()

    def timeOut(self):
        if self.go:
            self.flashBoxStatus()
            if self.waitSec < 1:
                self.stopWait()
                # self.e.set()
                return
            # else:
            #     self.waitTime()
        return False
    def autoRun(self):
        self.auto = not self.auto
        self.showTime(1,4,'auto model:'+str(self.auto).ljust(5))

    def reloadConfig(self):
        self.game_params.loadConfig()
        self.showTime(1,24,'size:'+str(self.game_params.app_width)+'X'+str(self.game_params.app_height))
    
    def resetWaitTime(self):
        # curses.echo()
        setsec = self.stdscr.getstr(1,20,10)
        try:
            self.waitSec = int(setsec)
            # m_str = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
            m_str = time.strftime("%H:%M:%S",  time.localtime())
            m_str = m_str+' reset to '+str(self.waitSec)+'s'
            print(m_str)
            self.showTime(1,24,m_str)
        except:
            self.showTime(1,24,'input err!')
        # curses.noecho()
    def viewLog(self):
        win32api.ShellExecute(0,'open','openbox.log','','',1)

    def changeWaitTime(self,add=True,sec=3600):
        if add:
            self.waitSec += sec
        else:
            if self.waitSec > sec:
                self.waitSec -= sec
            else:
                self.waitSec = int(self.waitSec/2)

    def showHelp(self):
        if self.showHelpStatus:
            self.showHelpStatus = False
            self.stdscr.clear()
            self.showBoxStatus()
            self.stdscr.refresh()
            return
        self.showHelpStatus = True
        helpStr = {
            'a':'autoRun,auto shut down',
            'f':'flash box status',
            'r':'reload config.ini',
            'i':'input secs to reset wait time',
            'v':'show openBox log',
            'h':'show this or not',
            '=/-':'+3600, -3600 or half',
        }
        i = 10
        for item in helpStr:
            i = i+1
            mstr = str(item).rjust(1)+'\t'+str(helpStr[item]).ljust(35)
            self.showTime(i,6,mstr,3)

if __name__ == '__main__':
    # 接收第一个参数，用于定时
    print('start:'+"-"*20)
    game = CLASHROYALE()
    spos = pyautogui.position()
    # game.battleWindow()
    cron_table = game.flashBoxStatus()
    pyautogui.moveTo(spos)
    if cron_table["sleep"] > 0 :
        print(f'wait {cron_table["sleep"]}s ')
        # m_mstr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
        m_mstr = 'press \'q\' to quit,\'h\' to help messeage. Reflash after '
        acts = {
            'a':'self.autoRun()',
            'f':'self.flashBoxStatus()',
            'r':'self.reloadConfig()',
            'i':'self.resetWaitTime()',
            'v':'self.viewLog()',
            'h':'self.showHelp()',
            '=':'self.changeWaitTime()',
            '-':'self.changeWaitTime(False)',
            ']':'self.changeWaitTime(True,60)',
            '[':'self.changeWaitTime(False,60)',
                }
        game.setStr(m_mstr)
        game.setSec(cron_table["sleep"])
        game.setActs(acts)
        game.startWait()            
