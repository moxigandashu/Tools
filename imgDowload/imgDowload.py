# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 20:09:29 2018

@author: wucong02
"""

import os 
import requests

os.chdir(r'E:\code\Tools\imgDowload')
def imgDowload(imgurl,imgname):
    img=requests.get(imgurl)
    with open ('%s.jpg'%imgname,'wb') as f:
        f.write(img.content)
        
if __name__=="__main__":
    imgurl='http://ms.bdimg.com/pacific/upload_5962578_1528192058183.png'
    imgDowload(imgurl,'img2')