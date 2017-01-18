#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年12月5日

@author: lichen
'''

import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class spider_IBM_Guardium(object):
    """
    定制爬虫类:爬取IBM_Guardium页面信息
    """
    
    
    def __init__(self,guardiumsite=None,postdata_userName=None,postdata_password=None):
        """
        类初始化方法
        """
        #guardium页面URL
        self.__guardium_site=guardiumsite
        #初始化request data
        self.__postdata_userName=postdata_userName
        self.__postdata_password=postdata_password

    def get_guardium_site(self):
        return self.__guardium_site


    def get_postdata_user_name(self):
        return self.__postdata_userName


    def get_postdata_password(self):
        return self.__postdata_password


    def set_guardium_site(self, value):
        self.__guardium_site = value


    def set_postdata_user_name(self, value):
        self.__postdata_userName = value


    def set_postdata_password(self, value):
        self.__postdata_password = value


    def del_guardium_site(self):
        del self.__guardium_site


    def del_postdata_user_name(self):
        del self.__postdata_userName


    def del_postdata_password(self):
        del self.__postdata_password

    guardium_site = property(get_guardium_site, set_guardium_site, del_guardium_site, "guardium_site's docstring")
    postdata_userName = property(get_postdata_user_name, set_postdata_user_name, del_postdata_user_name, "postdata_userName's docstring")
    postdata_password = property(get_postdata_password, set_postdata_password, del_postdata_password, "postdata_password's docstring")

    def get_dbServerIp(self,page_source):
        """
        截取数据库IP
        
        :param  page_source
                需要分析提取的网页源码
        
        :return 返回数据库IP
        """
        pattern=re.compile(r'<td.*?colid="host".*?>(?P<ip>.*?)</td>',re.S)
        return re.search(pattern,page_source).groupdict()["ip"]
        
    def get_dbServerType(self,page_source):
        """
        截取数据库类型
        
        :param  page_source
                需要分析提取的网页源码
        
        :return 返回数据库类型
        """
        pattern=re.compile(r'<td.*?colid="dbServerType".*?>(?P<dbservertype>.*?)</td>',re.S)
        return re.search(pattern,page_source).groupdict()["dbservertype"]
    
    def get_STAPStatus(self,page_source):
        """
        截取S-TAP状态
        
        :param  page_source
                需要分析提取的网页源码
        
        :return status_img S-TAP状态图标
                stap_status S-TAP状态
        """
        pattern=re.compile(r'<td.*?colid="stapStatus".*?>.*?(?P<status_img><span.*?></span>)(?P<stap_status>.*?)</div></td>',re.S)
        result=re.search(pattern,page_source)
        status_img=result.groupdict()["status_img"]
        stap_status=result.groupdict()["stap_status"]
        return status_img,stap_status

    def get_dbServerStatus(self,page_source):
        """
        截取数据库引擎状态
        
        :param  page_source
                需要分析提取的网页源码
        
        :return dbserverstatus_img 数据库引擎状态图标
                dbserver_status 数据库引擎状态
        """
        pattern=re.compile(r'<td.*?colid="ieStatus".*?>.*?(?P<dbserverstatus_img><span.*?></span>)(?P<dbserver_status>.*?)</div></td>',re.S)
        result=re.search(pattern,page_source)
        dbServerStatus_img=result.groupdict()["dbserverstatus_img"]
        dbServer_Status=result.groupdict()["dbserver_status"]
        return dbServerStatus_img,dbServer_Status

    def get_DBStatus(self):
        """
        获取数据库状态
        
        :return db_status 数据库状态map(待定)
        """
        #Selenum+PhantomJS解决方案
        #创建phantomjs浏览器模拟对象
        p_browser=webdriver.PhantomJS(executable_path="/Library/Python/2.7/site-packages/selenium/webdriver/phantomjs/phantomjs",service_args=["--ignore-ssl-errors=yes",]) #参数ignore-ssl-errors=yes代表忽视加密的ssl连接错误
        p_browser.get(self.__guardium_site)
        #提交用户登陆表单
        p_browser.find_element_by_xpath('//div[@id="loginInput"]/input[@name="username"]').clear() 
        p_browser.find_element_by_xpath('//div[@id="loginInput"]/input[@name="username"]').send_keys(self.__postdata_userName) 
        p_browser.find_element_by_xpath('//div[@id="loginInput"]/input[@name="password"]').clear()
        p_browser.find_element_by_xpath('//div[@id="loginInput"]/input[@name="password"]').send_keys(self.__postdata_password)
        p_browser.find_element_by_id("loginButton").click()              
        print "已点击登陆"
        listen_xpath='/html/body/div/div[@id="dijit_layout_ContentPane_0"]/div/div/div[@id="gridx_Grid_0"]/div[@class="gridxMain"]/div[@class="gridxBody gridxBodyRowHoverEffect"]/div[@visualindex="0"]/table/tbody/tr/td[@colid="stapStatus"]'
        p_browser.switch_to.frame(p_browser.find_element_by_xpath('//iframe[contains(@src,"adminviews")]')) #加载iframe内的html内容
        if(self.get_wait_data(wait_time=15,browser=p_browser,method=self.get_DBStatus,xpath_probe=listen_xpath)):
            context=p_browser.page_source
            #p_browser.get_screenshot_as_file("/Users/lichen/Documents/workspace/SpiderTest/resources/test.png") #创建页面快照
            p_browser.quit()
            #提取各数据库状态
            pattern=re.compile(r'<div class="gridxRow.*?visualindex.*?(?P<dbstatus><tr>.*?</tr>).*?</div>',re.S)
            result=re.finditer(pattern,context) #返回一个匹配文本中所有的子串的匹配结果的迭代器
            for dbstatus in result:
                #获取数据库IP
                ip=self.get_dbServerIp(dbstatus.groupdict()["dbstatus"])
                #获取数据库类型
                dbServertype=self.get_dbServerType(dbstatus.groupdict()["dbstatus"])
                #获取S-TAP状态
                status_img,stap_status=self.get_STAPStatus(dbstatus.groupdict()["dbstatus"])
                #获取数据库引擎状态
                dbServerStatus_img,dbServer_Status=self.get_dbServerStatus(dbstatus.groupdict()["dbstatus"])
                print ip,dbServertype,status_img,stap_status,dbServerStatus_img,dbServer_Status

    def get_wait_data(self,browser,xpath_probe,method,wait_time=10):
        """
        获取异步加载数据
    
        :param  browser
                模拟浏览器对象
        :param  wait_time
                扫描页面时间间隔；默认为10秒内每隔500ms扫描一次页面变化
        :param  id_probe
                只有AJAX加载成功才会出现的异步加载数据的html_id
        :param  method
                请求数据方法;若获取数据失败，则再次调用请求数据方法
    
        :return True or False 表示是否获得异步加载数据
        """
        try:
            wait_for_ajax_element=WebDriverWait(browser,wait_time)
            #until方法需要传入一个函数方法类型参数
            wait_for_ajax_element.until(
                                        #定义匿名函数:以driver为参数，以return driver.find_element_by_id(id_probe)为函数体
                                        lambda driver:driver.find_element_by_xpath(xpath_probe).is_displayed())
            print "获取异步加载数据成功"
            return True
        except:
            print "获取异步加载数据失败"
            print "再次尝试获取异步加载数据"
            browser.quit()
            method()














