from PIL import Image
from PIL import ImageEnhance
import pytesseract,os


def ocr(img,type='string',**kw):
    scale = 4
    width = int(img.size[0]*scale)
    height = int(img.size[1]*scale)
    img=img.resize((width, height),Image.ANTIALIAS)
    # im=im.convert('L')
    # im.show()
    # im=ImageEnhance.Contrast(im)
    # im=im.enhance(3)
    # im.show()
    if type=='digits':
        ocr_config = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789-+'
        res = pytesseract.image_to_string(img,config=ocr_config,**kw)
    else:
        res = pytesseract.image_to_string(img,**kw)
    # print(res)
    return res

if __name__ == '__main__':
    cwd = os.getcwd()+''
    img = f'{cwd}\\3752.png'
    img=Image.open(img)
    # print(Image.toString(img))
    print(ocr(img))
    
