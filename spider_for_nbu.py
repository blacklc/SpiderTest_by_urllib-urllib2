#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年11月30日

@author: lichen
'''

import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class spider_for_nbu(object):
    """
    定制爬虫类:爬取NBU页面信息
    """
    
    
    def __init__(self,nbusite=None,postdata_userName=None,postdata_password=None):
        """
        类初始化方法
        """
        #NBU页面URL
        self.__NBUsite=nbusite
        #初始化request data
        self.__postdata_userName=postdata_userName
        self.__postdata_password=postdata_password

    def get_nbusite(self):
        return self.__NBUsite
    
    def get_postdata_user_name(self):
        return self.__postdata_userName


    def get_postdata_password(self):
        return self.__postdata_password

    def set_nbusite(self, value):
        self.__NBUsite = value

    def set_postdata_user_name(self, value):
        self.__postdata_userName = value

    def set_postdata_password(self, value):
        self.__postdata_password = value

    def del_nbusite(self):
        del self.__NBUsite

    def del_postdata_user_name(self):
        del self.__postdata_userName


    def del_postdata_password(self):
        del self.__postdata_password

    _NBUsite = property(get_nbusite, set_nbusite, del_nbusite, "_NBUsite's docstring")
    _postdata_userName = property(get_postdata_user_name, set_postdata_user_name, del_postdata_user_name, "_postdata_userName's docstring")
    _postdata_password = property(get_postdata_password, set_postdata_password, del_postdata_password, "_postdata_password's docstring")

    def getStorageUtilization(self):
        """
        获取NBU可用备份空间与已用备份空间
        
        :return Used 已用备份空间map
                Available 可用备份空间map
        """
        #Selenum+PhantomJS解决方案
        #创建phantomjs浏览器模拟对象
        p_browser=webdriver.PhantomJS(executable_path="/Library/Python/2.7/site-packages/selenium/webdriver/phantomjs/phantomjs",service_args=["--ignore-ssl-errors=yes",]) #参数ignore-ssl-errors=yes代表忽视加密的ssl连接错误
        p_browser.get(self._NBUsite)
        #提交用户登陆表单
        p_browser.find_element_by_xpath('//div[@class="loginbox"]/div[@class="holder"]/div/div[@id="wwgrp_SubmitLogin_userName"]/div[@id="wwctrl_SubmitLogin_userName"]/input').clear() 
        p_browser.find_element_by_xpath('//div[@class="loginbox"]/div[@class="holder"]/div/div[@id="wwgrp_SubmitLogin_userName"]/div[@id="wwctrl_SubmitLogin_userName"]/input').send_keys(self.__postdata_userName) 
        p_browser.find_element_by_xpath('//div[@class="loginbox"]/div[@class="holder"]/div/div[@id="wwgrp_SubmitLogin_password"]/div[@id="wwctrl_SubmitLogin_password"]/input').clear()
        p_browser.find_element_by_xpath('//div[@class="loginbox"]/div[@class="holder"]/div/div[@id="wwgrp_SubmitLogin_password"]/div[@id="wwctrl_SubmitLogin_password"]/input').send_keys(self.__postdata_password)
        p_browser.find_element_by_xpath('//div[@class="loginbox"]/div[@class="holder"]/div/input[@value="Login"]').click()
        print "已点击登陆"
        if(get_wait_data(wait_time=15,browser=p_browser,id_probe='availStorageSpaceInPercentSpanId')):
            context=p_browser.page_source
            p_browser.quit()
            pattern_uss=re.compile(r'<span id="usedStorageSpaceSpanId">(?P<usedStorageSpace>.*)</span>')
            pattern_ussp=re.compile(r'<span id="usedStorageSpaceInPercentSpanId">(?P<usedStorageSpaceInPercent>.*)</span>')
            pattern_ass=re.compile(r'<span id="availStorageSpaceSpanId">(?P<availStorageSpace>.*)</span>')
            pattern_assp=re.compile(r'<span id="availStorageSpaceInPercentSpanId">(?P<availStorageSpaceInPercent>.*)</span>')
            usedStorageSpace=re.search(pattern_uss,context)
            availStorageSpace=re.search(pattern_ass,context)
            usedStorageSpaceInPercent=re.search(pattern_ussp,context)
            availStorageSpaceInPercent=re.search(pattern_assp,context)
            Used={
                  "usedStorageSpace":usedStorageSpace.groupdict()["usedStorageSpace"],
                  "usedStorageSpaceInPercent":usedStorageSpaceInPercent.groupdict()["usedStorageSpaceInPercent"]
                  }
            Available={
                       "availStorageSpace":availStorageSpace.groupdict()["availStorageSpace"],
                       "availStorageSpaceInPercent":availStorageSpaceInPercent.groupdict()["availStorageSpaceInPercent"]
                       }
            return Used,Available

def get_wait_data(browser,id_probe,wait_time=10):
    """
    获取异步加载数据
    
    :param  browser
            模拟浏览器对象
    :param  wait_time
            扫描页面时间间隔；默认为10秒内每隔500ms扫描一次页面变化
    :param  id_probe
            只有AJAX加载成功才会出现的异步加载数据的html_id
    
    :return Ture or False 表示是否获得异步加载数据
    """
    try:
        wait_for_ajax_element=WebDriverWait(browser,wait_time)
        #until方法需要传入一个函数方法类型参数
        wait_for_ajax_element.until(
                                    #定义匿名函数:以driver为参数，以return driver.find_element_by_id(id_probe)为函数体
                                    lambda driver:driver.find_element_by_id(id_probe).is_displayed() 
                                    )
        print "获取异步加载数据成功"
        return True
    except:
        print "获取异步加载数据失败"
        return False

