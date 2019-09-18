# -*- coding: utf-8-*-  

import cv2,time,curses
from main import CLASHROYALE

class PLAYCLASH(CLASHROYALE):
    def __init__(self,winTtile):
        super(PLAYCLASH,self).__init__(winTtile)
        self.closeCurses()

    def closeCurses(self):
        print(' call close curses!')
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        # self.stdscr = None

    def runGame(self):
        img_ok = cv2.imread(self.game_params.img['ok'])
        imgCard = {}
        for card in self.game_params.img['card']:
            imgCard[card] = cv2.imread(self.game_params.img['card'][card]) 
        while True:
            m_mstr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
            # print(m_mstr,end=' ')
            # print(m_mstr)
            self.updateImgbg()
            showtime = False
            for card in self.game_params.img['card']:
                is_,pos_ = self.inHere(imgCard[card],self.imgbg)
                if is_:
                    if not showtime:
                        print(m_mstr,end=' ')
                        showtime = True
                    print(card,end=' ')
            if showtime:
                print('')

            is_ok,_ = self.inHere(img_ok,self.imgbg)
            if is_ok:
                print('game is over!')
                break


if __name__ == '__main__':
  
    print('start:'+"-"*20)
    # game = CLASHROYALE('Android Emulator - sq_Pixel_2_API_28:5554')
    game = PLAYCLASH('Android Emulator - sq_Pixel_2_API_28:5554')
    game.runGame()
        
#每秒判断2-3
#约0.4秒处理完一次

    