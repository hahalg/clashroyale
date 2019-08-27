# -*- coding: utf-8-*-  

# 对后台应用程序截图，程序窗口可以被覆盖，但如果最小化后只能截取到标题栏、菜单栏等。
import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image

def grabAPP(hwnd,left,top,right,bot):
    # 获取句柄窗口的大小信息
    # 可以通过修改该位置实现自定义大小截图
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    left, top, right, bot = int(left),int(top),int(right),int(bot)
    w = right - left
    h = bot - top
    # print(f'left:{left}, top:{top}, right:{right}, bot:{bot}')

    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwndDC = win32gui.GetWindowDC(hwnd)

    # 创建设备描述表
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)

    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    # 截图至内存设备描述表
    img_dc = mfcDC
    mem_dc = saveDC
    mem_dc.BitBlt((0, 0), (w, h), img_dc, (100, 100), win32con.SRCCOPY)

    # 将截图保存到文件中
    # saveBitMap.SaveBitmapFile(mem_dc, 'screenshot.bmp')


    # 改变下行决定是否截图整个窗口，可以自己测试下
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    # print(result)

    # 获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # 存储截图
    if result == 1:
        #PrintWindow Succeeded
        # im.save("test.png")
        # im.show()
        return im
    else:
        print('grab img err!')
        return False
 
if __name__ == '__main__':
    import time
    time.sleep(10)

    # 获取要截取窗口的句柄
    hwnd = win32gui.FindWindow(win32con.NULL,'Android Emulator - sq_Pixel_2_API_24:5554')
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    img = grabAPP(hwnd,left,top,right,bot)
    img.show()
