from PIL import Image
from PIL import ImageEnhance
import pytesseract,os


def ocr(img):
    scale = 4
    width = int(img.size[0]*scale)
    height = int(img.size[1]*scale)
    img=img.resize((width, height),Image.ANTIALIAS)
    # im=im.convert('L')
    # im.show()
    # im=ImageEnhance.Contrast(im)
    # im=im.enhance(3)
    # im.show()
    res = pytesseract.image_to_string(img)
    # print(res)
    return res

if __name__ == '__main__':
    cwd = os.getcwd()+'\\cheat\\clashroyale'
    img = f'{cwd}\\img\\t1.png'
    img=Image.open(img)
    # print(Image.toString(img))
    print(ocr(img))
    
