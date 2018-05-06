# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 10:40:04 2018

@author: wucong02
"""
import os
from selenium import webdriver

username=input('input username:')
password=input('input password:')
os.chdir(r'E:\code\Tools\chromedriver')
options=webdriver.ChromeOptions()
#设置webdriver参数
opener=webdriver.Chrome(r'D:\Software\chromedriver.exe',chrome_options=options)
opener.maximize_window()
opener.get('https://www.weibo.com')
opener.implicitly_wait(5)
acountname=opener.find_element_by_css_selector('#loginname')
acountname.send_keys(username)
password=opener.find_element_by_name('password')
password.send_keys(password)
login=opener.find_element_by_css_selector('a[class="W_btn_a btn_32px"]')
login.click()
opener.implicitly_wait(3)

idenCodeAcc=opener.find_element_by_css_selector('#message_sms_login')
idenCodeAcc.click()
                                                
opener.execute_script('window.scrollTo(0,document.body.scrollHeight)')#滑动到底部
#指定滑动高度
#js="var q=document.documentElement.scrollTop=10000"  
#opener.execute_script(js) 


feeds=opener.find_elements_by_css_selector('[class="WB_feed_detail clearfix"]')
for feed in feeds:
    print(feed.find_element_by_css_selector('[class="WB_info"]').text)
    
    
    
#shantou
browser=webdriver.Chrome(r'D:\Software\chromedriver.exe',chrome_options=options)
browser.maximize_window()
browser.get('http://shantou.baidu.com/index.html#/')
fccount=browser.find_element_by_css_selector('input[id="entered_login"]')
fcpassw=browser.find_element_by_css_selector('input[id="entered_password"]')
imgcode=browser.find_element_by_css_selector('input[id="entered_imagecode"]')
login=browser.find_element_by_css_selector('input[class="login-button"]')
fccount.send_keys('ProductAdsMCC')
fcpassw.send_keys('Pr8ductAdsMCCnew')
imgcode.send_keys('hhsj')
login.click()
browser.implicitly_wait(5)
#用户id
uid='7751028'
userid=browser.find_element_by_id("ctrl-t-1-userId-input")
userid.send_keys(uid)
usearch=browser.find_element_by_id("ctrl-t-1-search")
usearch.click()
browser.implicitly_wait(3)
browser.find_element_by_id('ctrl-t-1-table-cell0-0')
browser.find_element_by_id('ctrl-t-1-table-cell0-0').click()
handels=browser.window_handles
handel=handels.pop()
browser.switch_to_window(handel)

#详情页
browser.find_element_by_link_text('结构化-高级版').click()
browser.implicitly_wait(5)

#商品文件
browser.find_element_by_css_selector('li[class="ui-tab-item"]').click()
browser.implicitly_wait(5)
