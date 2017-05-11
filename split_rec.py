# -*- coding:utf-8 -*-
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
import StringIO
# import sys
from PIL import Image
import PIL.ImageOps
import urllib
import os
import pytesseract

def saveSampleImg():
	if not os.path.exists('training'):
		os.mkdir('training')
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
def depoint(img,revert=False):   #input: gray image, remove the noise
	pixdata = img.load()
	w,h = img.size
	if revert==False:
		for y in range(0,h):
			for x in range(0,w):
					#remove the frame
					if(y==0 or y==h-1 or x==0 or x==w-1):
						pixdata[x,y] = 255
					count = 0
					if y-1>=0 and pixdata[x,y-1] > 245:
						count = count + 1
					if y+1 < h and pixdata[x,y+1] > 245:
						count = count + 1
					if x-1>=0 and pixdata[x-1,y] > 245:
						count = count + 1
					if x+1 < w and pixdata[x+1,y] > 245:
						count = count + 1
					if count > 2:
						pixdata[x,y] = 255
	else:
		for y in range(h-1,-1,-1):
			for x in range(w-1,-1,-1):
					count = 0
					if y-1>=0 and pixdata[x,y-1] > 245:
						count = count + 1
					if y+1<h and pixdata[x,y+1] > 245:
						count = count + 1
					if x-1>=0 and pixdata[x-1,y] > 245:
						count = count + 1
					if x+1 <w and pixdata[x+1,y] > 245:
						count = count + 1
					if count > 2:
						pixdata[x,y] = 255

#图片x轴的投影，如果有数据（黑色像素点0）值为1否则为0
def get_projection_x(image,invert=False):
	p_x = [0 for x in xrange(image.size[0])]
	for w in xrange(image.size[1]):
		for h in xrange(image.size[0]):
			if invert:
				if image.getpixel((h,w)) == 255:
					p_x[h] = 1
					continue
			else:
				if image.getpixel((h,w)) == 0:
					p_x[h] = 1
					continue
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


def get_img_width(projection_x):
	start_pos = 0
	stop_pos = 0
	pro_len = len(projection_x) - 1
	for idx in xrange(pro_len):
		if projection_x[idx] > 0:
			start_pos = idx
			break
	for idx in xrange(pro_len):
		if projection_x[pro_len - idx] > 0:
			stop_pos = pro_len - idx
			break

	return stop_pos - start_pos


# 旋转卡壳
def rotating_calipers(image):
	# original with
	min_width = 100
	min_angle = 100
	for angle in xrange(-60, 60):
		temp_img = image.rotate(angle, expand=True)
		jection = get_projection_x(temp_img, True)
		cur_width = get_img_width(jection)

		if (cur_width < min_width):
			min_width = cur_width
			min_angle = angle

	return image.rotate(min_angle, expand=True)
#分割后的图片，x轴分割后，同时去掉y轴上线多余的空白
def split_image(image, split_seq=None,save_temp=False):
	#image = PIL.ImageOps.invert(image)#反转颜色
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
		if height <5: # ignore the small image
			continue
		child_img = Image.new('L',(split_seq[idx][1], height))
		child_img.putdata(datas)
		inverted_img = PIL.ImageOps.invert(child_img)
		adjusted_img = rotating_calipers(inverted_img)
		if save_temp:
			tempNumImg = 'temp/0-%d.png' % ind
			adjusted_img.save(tempNumImg)
		ind = ind +1
		#print tempNumImg
		res.append(adjusted_img)
		# recNum = pytesseract.image_to_string(adjusted_img, config='-psm 6 outputbase digits')
		# print recNum

	return res

#saveSampleImg()
def rec_img(imgPath):
	img = Image.open(imgPath).convert("L")
	binarizing(img,170)
	# img.save('C:\\NotBackedUp\\00.png')
	depoint(img)
	depoint(img,True)
	# img.save('C:\\NotBackedUp\\01.png')
	seperated_img = split_image(img)
	recdString = ""
	for cur_img in seperated_img:
		recNum = pytesseract.image_to_string(cur_img, config='-psm 10 outputbase digits')
		recdString = recdString + recNum

	print recdString
	#img.save('temp/%s.png' % recdString)
	if len(recdString)==4:
		# img.save('temp/%s.png' % recdString)
		print "success"
	else:
		print "error ..."
	return recdString

# filePath = 'source/3.png'
# rec_img(filePath)