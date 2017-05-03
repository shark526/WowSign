#-*-coding:utf-8-*- 
import urllib
import StringIO
from PIL import Image
import os
import pytesseract
"""
pip install pytesseract
pip install pytesseract-ocr
pip install tesserocr
sudo pip install pillow
"""
if not os.path.exists('training'):
    os.mkdir('training')

def saveSampleImg():
    for i in xrange(50):
        #save images
        img = Image.open(StringIO.StringIO(urllib.urlopen('http://169ol.com/Stream/Code/getCode').read()))
        imgPath = "training/%d.png" %i
        #print imgPath
        img.save(imgPath)

def binarizing(img,threshold): #input: gray image, get black and white images
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def depoint(img):   #input: gray image, remove the noise
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255

#图片x轴的投影，如果有数据（黑色像素点）值为1否则为0
def get_projection_x(image):
    p_x = [0 for x in xrange(image.size[0])]
    for w in xrange(image.size[1]):
        for h in xrange(image.size[0]):
            if image.getpixel((h,w)) == 0:
                p_x[h] = 1
    return p_x

#获取分割后的x轴坐标点
#返回值为[起始位置, 长度] 的列表
def get_split_seq(projection_x):
    res = []
    for idx in xrange(len(projection_x) - 1):
        p1 = projection_x[idx]
        p2 = projection_x[idx + 1]
        if p1 == 1 and idx == 0:
            res.append([idx, 1])
        elif p1 == 0 and p2 == 0:
            continue
        elif p1 == 1 and p2 == 1:
            res[-1][1] += 1
        elif p1 == 0 and p2 == 1:
            res.append([idx + 1, 1])
        elif p1 == 1 and p2 == 0:
            continue
    return res

#分割后的图片，x轴分割后，同时去掉y轴上线多余的空白
def split_image(image, split_seq=None):
    if split_seq is None:
        split_seq = get_split_seq(get_projection_x(image))
    length = len(split_seq)
    imgs = [[] for i in xrange(length)]
    res = []
    for w in xrange(image.size[1]):
        line = [image.getpixel((h,w)) for h in xrange(image.size[0])]
        for idx in xrange(length):
            pos = split_seq[idx][0]
            llen = split_seq[idx][1]
            l = line[pos:pos+llen]
            imgs[idx].append(l)
    ind = 0
    for idx in xrange(length):
        datas = []
        height = 0
        for data in imgs[idx]:
            flag = False
            for d in data:
                if d == 0:
                    flag = True
            if flag == True:
                height += 1
                datas += data
        child_img = Image.new('L',(split_seq[idx][1], height))
        child_img.putdata(datas)
        res.append(child_img)
        tempNumImg = '0-%d.png' % ind
        child_img.save(tempNumImg)
        ind = ind +1
        print tempNumImg

    return res
"""
#saveSampleImg()
imgPath = 'training/0.png'
img = Image.open(imgPath).convert("L")
binarizing(img,175)
#img.save('0-1.png')
depoint(img)
img.save('00.png')
split_image(img)
"""
imgPath = '0-1.png' 
imgT = Image.open(imgPath)
imgT.load()
print pytesseract.image_to_string(imgT)

print('done.')


