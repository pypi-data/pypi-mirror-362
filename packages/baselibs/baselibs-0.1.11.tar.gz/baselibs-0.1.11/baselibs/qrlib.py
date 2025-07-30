#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

'''
二维码库 可识别、生成、组合二维码。
'''

import base64
import io
import json
import logging
import math
import os
import pyqrcode
# import pyssdb
import pyzbar.pyzbar as pyzbar
import random
import re
import requests
# import schedule
import string 
import sys
# import threading
import time
import traceback
import urllib.request 

from PIL import Image ,ImageEnhance
from logging.handlers import TimedRotatingFileHandler

''' 
图像裁剪：将一个图像裁剪后保存为另一个图像 
函数参数：（原始图像srcimg，距离图片左边界距离x, 距离图片上边界距离y，裁剪框宽度w，裁剪框高度h, 输出图像outimg） 
'''
def image_crop (srcimg, x, y, w, h, outimg):
    try:
        if type(srcimg) == str:
            img = Image.open(srcimg)
            # if isinstance(qrimg,Image.Image): 
        else:
            img = srcimg
        region = img.crop((x, y, x+w, y+h)) 
        region.save(outimg) 
        # img.close ()
        return 1
    except Exception as e :
        logging.error('Error in image_crop: '+ traceback.format_exc())
        return None

def imagebox (srcimg):
    # 返回一个图像的大小,tuple
    try:
        if type(srcimg) == str:
            img = Image.open(srcimg)
            # if isinstance(qrimg,Image.Image): 
        else:
            img = srcimg
        box = img.size
        img.close ()
        return box
    except Exception as e :
        logging.error('Error in imagebox: '+ traceback.format_exc())
        return None

def create_QR_image (text, imgfile='', width=100, height=100):
    '''
    生成二维码，返回图像或者保存为文件(PNG); 
    可指定大小，默认为100 x 100 pixel
    参数：
        text        要生成二维码的字符
        imagefile   保存的文件名(PNG格式)
        width       生成的图像宽度，单位：像素
        height       生成的图像高度，单位：像素
    返回：
        如果指定文件名，则返回文件名；
        否则返回Image对象
    '''
    try:
        qrcode = pyqrcode.create(text)
        buf = io.BytesIO()
        qrcode.png(buf, scale=5)
        img = Image.open(buf)
        img = img.resize((width, height))
        
        if imgfile != '':
            img.save(imgfile, 'PNG')
            return imgfile
        else:
            # buf1 = io.BytesIO()
            # img.save(buf1,'PNG')
            return img
    except Exception as e:
        logging.error('Error in gen_QR: '+ traceback.format_exc())
        return None
    
def get_QR(qrimg):
    '''
    # 识别图片中的二维码；
    参数：
        qrimg 可以是文件名或者Image对象
    返回：Json格式
        第一个二维码的字符串
        样例：[{"data": "https://url.cn/5hzV4lW", "rect": [131, 1095, 149, 149]}]
    '''
    try:
        if type(qrimg) == str:
            img = Image.open(qrimg)
        else:
            img = qrimg
        
        # 图像预处理
        # img = ImageEnhance.Brightness(img).enhance(2.0)# 增加亮度
        # img = ImageEnhance.Sharpness(img).enhance(17.0)# 锐利化
        # img = ImageEnhance.Contrast(img).enhance(4.0)# 增加对比度
        # img = img.convert('L')# 灰度化

        barcodes = pyzbar.decode(img)
        jsonret = []
        # 多个二维码的情况
        for barcode in barcodes:
            ret = {}
            ret['data'] = barcodes[0].data.decode("utf-8")
            ret['rect'] = barcodes[0].rect
            jsonret.append(ret)     # json.loads(json.dumps(ret))
        return  jsonret
    except Exception as e:
        logging.error('Error in get_QR: '+ traceback.format_exc())
        return None

def image_paste (image_background, image2, box, outimg:str):
    '''
    图像合并：
    把image2合并到 image_background 上，位置为 box ,最后保存到文件 outimg
    注： image2 大小要提前设置好；
    参数：
        image_background
        image2
        box     位置(left, top)
        outimg
    返回：
        成功或者失败
    '''
    try:
        if type(image_background) == str:
            imgbk = Image.open(image_background)
        else:
            imgbk = image_background
        if type(image2) == str:
            img2 = Image.open(image2)
        else:
            img2 = image2
        # 改变大小？
        # sizebox = box[2:4] # (box[2], box[3])
        # posbox = box[0:2]  
        # newimg = img2.resize(sizebox)
        imgbk.paste (img2, box)
        imgbk.save(outimg) 
    except Exception:
        logging.error('Error in image_paste: '+ traceback.format_exc())
        return None

def get_url (url,charset='utf-8'):
    # 从指定的URL读取网页HTML代码，默认为utf-8编码,读取失败返回空
    try:
        html = ''
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response:
            html = response.read()
            html = html.decode(charset, 'ignore')  
        return html
    except Exception:
        logging.error('Error in get_url: '+ traceback.format_exc())
        return ''

def url_SaveImage (imgurl, imgfilename='', GBL_IMAGE_PATH="./"):
    '''
    下载URL图片并保存到本地目录
    参数：
        imgurl          图片URL地址, 可传未url解码的字符串
        imgfilename     保存的文件名，不传值会自动生成；
    返回：
        返回保存到的文件完整路径名；
    测试用例：

    '''
    try:
        # URLdecode
        imgurl = urllib.parse.unquote(imgurl)

        # 生成文件名
        if imgfilename == '':
            rndfilename  = 'page_'+ get_randstr() + '.jpg'
            imgfilename = GBL_IMAGE_PATH + rndfilename
       
        if not os.path.exists(GBL_IMAGE_PATH):
            os.makedirs(GBL_IMAGE_PATH, exist_ok=True)
        
        urllib.request.urlretrieve(imgurl, imgfilename) 
        return imgfilename
    except Exception as e:
        logging.error('Error in url_SaveImage: '+ traceback.format_exc())
        return None

def image_b64fromfile (imagefile):
    '''
    将图片进行base64编码
    参数：
        imagefile 文件名，字符串
    返回:
        字符串，base64编码格式
    '''
    try:
        with open(imagefile, 'rb') as f:  # 以二进制读取图片
            data = f.read()
            encodestr = base64.b64encode(data) # 得到 byte 编码的数据
            ret = str(encodestr,'utf-8')
        return ret
    except Exception as e:
        logging.error('Error in image_b64fromfile: '+ traceback.format_exc())
        return None

def image_b64tofile (strs, imagefile):
    '''
    将base64编码的图片保存成文件
    参数：
        strs        base64字符串
        imagefile   图片文件名

    返回：
        成功返回1，失败返回 None
    '''
    try:
        imgdata = base64.b64decode(strs)  
        file = open(imagefile,'wb')  
        file.write(imgdata)  
        file.close()  
        return 1
    except Exception as e:
        logging.error('Error in image_b64tofile: '+ traceback.format_exc())
        return None

'''
将base64编码字符转换成Image类型
参数：
    strs        base64字符串

返回：
    成功返回 image对象
    失败返回 None
'''
def image_b64toImage (strs):
    try:
        imgdata = base64.b64decode(strs)  
        buf = io.BytesIO()
        buf.write(imgdata)
        img = Image.open(buf)
        return img
    except Exception as e :
        logging.error('Error in image_b64toImage: '+ traceback.format_exc())
        return None

'''
生成随机的字符串，可用于文件名等
参数：
    strlen  字符串长度，默认为10

返回： 
    成功返回 生成的字符串
    失败返回 None

'''
def  get_randstr (strlen=10):
    try:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(strlen, strlen)))
        return ran_str
    except Exception as e :
        logging.error('Error in get_randstr: '+ traceback.format_exc())
        return None

def get_b64_string (strbase64):
    '''
    接口格式化数据解析
    数据格式：
    "data:image/png;base64,iVBORw"

    参数：
        strbase64   base64编码字符串

    返回 :
        a tuple: ('jpg', 'base64string')
    '''
    try:
        ret = re.match(r"data:image/(.*);base64,(.*)", strbase64)
        if ret:
            return ret.groups()
        else:
            return None
    except Exception as e :
        logging.error('Error in get_b64: '+ traceback.format_exc())
        return None

if __name__ == '__main__':
    pass
    import fire
    fire.Fire()

