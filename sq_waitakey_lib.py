# -*- coding: utf-8-*-  
# 等待用户输入，超时退出
import time
import threading
import curses

class WAITAKEY(object):
    '''等待输入，输入后退出，或者超时退出'''
    waitSec = 10
    go = True
    def __init__(self):
        self.stdscr = curses.initscr()
        self.initCurses()

    def setStr(self,printstr=''):
        self.printstr = printstr
    def setSec(self,waitSec=''):        
        self.waitSec = waitSec

    def startWait(self):
        self.e = threading.Event()

        self.wait_thread = threading.Thread(target=self.waitEvent)
        self.input_thread = threading.Thread(target=self.getInput)

        self.input_thread.daemon = True

        self.wait_thread.start()
        self.input_thread.start()


    def setActs(self,acts):
        self.acts = acts

    def getInput(self):
        # stdscr.nodelay(0)
        self.stdscr.attron(curses.color_pair(1))    
        self.stdscr.addstr(0, 0, self.printstr)
        self.stdscr.refresh()

        akey = chr(self.stdscr.getch())
        # stdscr.nodelay(sec)
        # akey = input(mstr)
        # print('您输入了:',akey)
        # if akey == 'q':
        if akey == 'q':
            print(' quit')
            self.go = False
            self.e.set()
            return

        for item in self.acts:
            if akey == item:
                exec(self.acts[item])
                self.stdscr.refresh()

        self.getInput()
        # return akey

    def waitEvent(self):
        # print(f' wait {sec}s')
        # e.wait(sec)
        self.waitTime()
        # time.sleep(sec)
        if __name__ == '__main__':
            m_mstr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
            print(m_mstr)

    def waitTime(self):
        x,y = 0,len(self.printstr)
        showlen = 8
        while True:
            mmStr = str(self.waitSec)
            # mmStr = (' '*(showlen-len(mmStr)) + mmStr + 's').ljust(showlen)
            mmStr = (mmStr+'s').ljust(showlen)
            # 设置文字的前景色和背景色
            self.stdscr.attron(curses.color_pair(4))    
            self.stdscr.addstr(x, y, mmStr)
            # print(mmStr)
            self.stdscr.refresh()
            # curses.cbreak()
            # stdscr.keypad(1)
            # stdscr.nodelay(1)
            # time.sleep(1)
            self.e.wait(1)
            self.waitSec = self.waitSec - 1
            if self.waitSec < 1:
                self.timeOut()
                break
        # stdscr.keypad(0)

    def timeOut(self):
        pass

    def initCurses(self):
        # 初始化并返回一个window对象
        
        self.stdscr.clear()
        self.stdscr.refresh()
        # 如何要用带颜色的字就必须调这个方法
        curses.start_color()
        # 设置颜色对，其实就是前景色和背景色
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.noecho()

    def showTime(self,x,y,mstr,style=1):

        if not isinstance(mstr,str):
            # self.stdscr.addstr(x+3, y, str(type(mstr)))
            if isinstance(mstr,time.struct_time):
                mstr = time.strftime("%Y%m%d-%H:%M:%S",mstr)
            else:
                mstr = str(mstr)

        self.stdscr.attron(curses.color_pair(style))
        self.stdscr.addstr(x, y, mstr)
        self.stdscr.refresh()

if __name__ == '__main__':

    m_mstr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
    print(m_mstr)
    acts = {
        'a':'self.showTime(3,10,\'like do it\')',
        'b':'self.showTime(4,10,\'yes!!!!\',2)',
            }
    # waitk = waitAKey('press \'q\' to quit,\'f\' to flash box:',20,acts)
    waitk = WAITAKEY()
    waitk.setStr(m_mstr)
    waitk.setSec(40)
    waitk.setActs(acts)
    waitk.startWait()
    waitk.showTime(6,5,'come here!')
    acts = {
        'a':'self.showTime(3,10,\'after like do it\')',
        'b':'self.showTime(4,10,\'after yes!!!!\',2)',
        'c':'self.showTime(5,10,\'after yes!!!!\',3)',
        't':'self.showTime(5,10,time.localtime(),3)',
            }
    waitk.setActs(acts)