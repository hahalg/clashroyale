# -*- coding: utf-8-*-  

import cv2,time,curses
from main import CLASHROYALE
from ocr import ocr

class PLAYCLASH(CLASHROYALE):
    available_cards = []
    imgbg = None
    def __init__(self,**kw):
        super(PLAYCLASH,self).__init__(**kw)
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
                    self.available_cards.append(card)
                    # if not showtime:
                    #     print(m_mstr,end=' ')
                    #     showtime = True
                    # print(card,end=' ')
            # if showtime:
            #     print('')
            self.analyCards()
            self.available_cards.clear()

            is_ok,_ = self.inHere(img_ok,self.imgbg)
            if is_ok:
                # print('game over!')
                time.sleep(3)
                self.updateImgbg()
                self.gameResult()
                break

    def analyCards(self):
        if len(self.available_cards)<1:
            return
        # m_mstr = time.strftime("%Y%m%d-%H:%M:%S",  time.localtime())
        # print(m_mstr,self.available_cards)

    def startTrain(self):
        #click ==
        self.clickBT('Set')
        time.sleep(0.5)
        #click Training Camp
        self.clickBT('TrainingCamp')
        time.sleep(0.5)
        #click yes
        self.clickBT('Yes')
        time.sleep(0.5)

    def downCups(self):
        if self.clickBT('do_battle'):
            self.runGame()
            # time.sleep(5)
            self.clickBT('ok')
        else:
            print('Can not start battle!')

    def getCups(self):
        cups_img = self.grabScreen(
            self.game_params.game_area_left+230,
            self.game_params.game_area_top+55,
            self.game_params.game_area_left+230+50,
            self.game_params.game_area_top+57+16
            )
        # cups_img.show()
        cups_str = ocr(cups_img,type='digits')
        # print(cups_str)
        if cups_str == '':
            return 0
        return cups_str

    def downCupsCount(self,n=1):
        for i in range(n):
            self.updateImgbg()
            st_cups = self.getCups()
            self.downCups()
            time.sleep(2)
            end_cups = self.getCups()
            print('start:',st_cups,'end:',end_cups,end='\t')
            try:
                print('result:',(int(end_cups)-int(st_cups)))
            except:
                print('')


    def gameResult(self):
        print('='*20+'game reslut:')
        if self.imgbg is None:
            self.updateImgbg()
        img_royale_red = cv2.imread(self.game_params.img['royale_red'])
        is_red,red_royale = self.inHere(img_royale_red,self.imgbg,0.97)
        if is_red:
            print('red crown:',len(red_royale),red_royale)
        img_royale_blue = cv2.imread(self.game_params.img['royale_blue'])
        is_blue,blue_royale = self.inHere(img_royale_blue,self.imgbg,0.97)
        if is_blue:
            print('blue crown:',len(blue_royale),blue_royale)

        sign = ''
        img_win_blue = cv2.imread(self.game_params.img['winner_blue'])
        win_blue,_ = self.inHere(img_win_blue,self.imgbg,0.95)
        if win_blue:
            print('blue win!',end=' ')
            sign = '+'
        img_win_red = cv2.imread(self.game_params.img['winner_red'])
        win_red,_ = self.inHere(img_win_red,self.imgbg,0.95)
        if win_red:
            print('red win!',end=' ')
            sign = '-'
        cups_img = self.grabScreen(
            self.game_params.game_area_left+310,
            self.game_params.game_area_top+410,
            self.game_params.game_area_left+310+24,
            self.game_params.game_area_top+410+15
            )
        # cups_img.show()
        cups_str = ocr(cups_img,type='digits')
        print(cups_str)
        print('='*20+'game over')

        
        

if __name__ == '__main__':
  
    print('start:'+"-"*20)
    # game = CLASHROYALE('Android Emulator - sq_Pixel_2_API_28:5554')
    game = PLAYCLASH()
    '''
    game.battleWindow()
    game.startTrain()
    print('wait to play game...')
    game.runGame()
    '''
    game.gameResult()
    # game.downCupsCount(2)
        
#每秒判断2-3
#约0.4秒处理完一次

    