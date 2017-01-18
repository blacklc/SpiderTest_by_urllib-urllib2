#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年12月7日

@author: lichen
'''

import cookielib
import re
import urllib2
import ssl

class spider_F5(object):
    """
    定制爬虫类:爬取F5页面信息
    """
    
    
    def __init__(self,F5_top_level_url=None,username=None,password=None,cookie=None):
        """
        类初始化方法
        """
        self.__F5_top_level_url=F5_top_level_url #F5根URL(由https://主机名或ip:端口号组成)
        
        self.__username=username
        self.__password=password
        
        self.__password_mgr=urllib2.HTTPPasswordMgrWithDefaultRealm() #初始化密码管理对象(利用该对象可为一url指定用户名与密码)
        self.__password_mgr.add_password(None,self.__F5_top_level_url,self.__username, self.__password) #使用密码管理对象为F5根URL添加用户名与密码
        
        #创建cookie对象
        if not cookie:
            self.__cookie=cookielib.CookieJar()
        else:
            self.__cookie=cookie
        self.__handler_cookie=urllib2.HTTPCookieProcessor(self.__cookie) #创建一个cookie处理器 
        
        self.__handler_Basic_Authentication= urllib2.HTTPBasicAuthHandler(self.__password_mgr)
        
        self.__opener= urllib2.build_opener(*[self.__handler_Basic_Authentication,self.__handler_cookie]) #创建opener
        urllib2.install_opener(self.__opener) #加载opener;即可在使用urlopen时实现上述功能
    
        #自定义http request headers
        self.__headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0", #以浏览器的形式访问页面
                        "Referer":"https://172.16.1.102"} #应对CSRF攻击手段;指定http请求来源
    
        self.__request=None #创建requset对象

    def get_cookie(self):
        return self.__cookie


    def set_cookie(self, value):
        self.__cookie = value


    def del_cookie(self):
        del self.__cookie


    def get_f_5_top_level_url(self):
        return self.__F5_top_level_url


    def get_username(self):
        return self.__username


    def get_password(self):
        return self.__password


    def get_password_mgr(self):
        return self.__password_mgr


    def get_handler_basic_authentication(self):
        return self.__handler_Basic_Authentication


    def get_handler_cookie(self):
        return self.__handler_cookie


    def get_opener(self):
        return self.__opener


    def get_headers(self):
        return self.__headers


    def get_request(self):
        return self.__request

    def set_f_5_top_level_url(self, value):
        self.__F5_top_level_url = value


    def set_username(self, value):
        self.__username = value


    def set_password(self, value):
        self.__password = value


    def set_password_mgr(self, value):
        self.__password_mgr = value


    def set_handler_basic_authentication(self, value):
        self.__handler_Basic_Authentication = value


    def set_handler_cookie(self, value):
        self.__handler_cookie = value


    def set_opener(self, value):
        self.__opener = value


    def set_headers(self, value):
        self.__headers = value


    def set_request(self, value):
        self.__request = value


    def del_f_5_top_level_url(self):
        del self.__F5_top_level_url


    def del_username(self):
        del self.__username


    def del_password(self):
        del self.__password


    def del_password_mgr(self):
        del self.__password_mgr


    def del_handler_basic_authentication(self):
        del self.__handler_Basic_Authentication


    def del_handler_cookie(self):
        del self.__handler_cookie


    def del_opener(self):
        del self.__opener


    def del_headers(self):
        del self.__headers


    def del_request(self):
        del self.__request

    _F5_top_level_url = property(get_f_5_top_level_url, set_f_5_top_level_url, del_f_5_top_level_url, "_F5_top_level_url's docstring")
    _cookie = property(get_cookie, set_cookie, del_cookie, "_cookie's docstring")
    _username = property(get_username, set_username, del_username, "_username's docstring")
    _password = property(get_password, set_password, del_password, "_password's docstring")
    _password_mgr = property(get_password_mgr, set_password_mgr, del_password_mgr, "_password_mgr's docstring")
    _handler_Basic_Authentication = property(get_handler_basic_authentication, set_handler_basic_authentication, del_handler_basic_authentication, "_handler_Basic_Authentication's docstring")
    _handler_cookie = property(get_handler_cookie, set_handler_cookie, del_handler_cookie, "_handler_cookie's docstring")
    _opener = property(get_opener, set_opener, del_opener, "_opener's docstring")
    _headers = property(get_headers, set_headers, del_headers, "_headers's docstring")
    _request = property(get_request, set_request, del_request, "_request's docstring")
    
    def get_poolMemberName(self,page_source):
        """
        截取F5 Pool成员名
        
        :param  page_source
                需要分析提取的网页源码
        
        :return F5 Pool成员名
        """
        pattern=re.compile(r'<a.*?>(?P<poolMember_name>.*?)</a>',re.S)
        return re.search(pattern,page_source).groupdict()["poolMember_name"]
    
    def get_poolMemberStatus(self,page_source):
        """
        截取F5 Pool成员状态
        
        :param  page_source
                需要分析提取的网页源码
        
        :return F5 Pool成员状态
        """
        pattern=re.compile(r'\((?P<poolMember_status>.*?)\)',re.S)
        return re.search(pattern,page_source).groupdict()["poolMember_status"]
    
    def get_poolMemberImg(self,page_source):
        """
        截取F5 Pool成员状态图标
        
        :param  page_source
                需要分析提取的网页源码
        
        :return F5 Pool成员状态图标
        """
        pattern=re.compile(r'_.*?_(?P<poolMember_Img>.*?).gif',re.S)
        return re.search(pattern,page_source).groupdict()["poolMember_Img"]
    
    def get_F5PoolStatus(self,pool_name=None):
        """
        获取F5Pool成员状态
        
        :param  pool_name
                F5 Pool名
                
        :return 
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        f5_poolstatus_url="%s/tmui/Control/jspmap/tmui/locallb/pool/resources.jsp?name=%s&startListIndex=0&showAll=true" %(self._F5_top_level_url,pool_name)
        self._request=urllib2.Request(url=f5_poolstatus_url,headers=self._headers) #创建request对象
        try:
            response=urllib2.urlopen(self._request,timeout=60) #建立http request并获取http response
            #提取各pool状态
            pattern=re.compile(r'<tr class="color\d" style="".*?<td class="first".*?>.*?</td.*?<td.*?>(?P<poolMember_img>.*?)</td.*?<td.*?>(?P<poolMember>.*?)</td.*?<td.*?>.*?</td.*?<td class="last".*?>(?P<poolMember_status>.*?)</td.*?</tr>',re.S)
            result=re.finditer(pattern,response.read()) #返回一个匹配文本中所有的子串的匹配结果的迭代器
            for poolMember_info in result:
                #获取pool成员名
                poolMember_name=self.get_poolMemberName(poolMember_info.groupdict()["poolMember"])
                #获取pool成员状态
                poolMember_status=self.get_poolMemberStatus(poolMember_info.groupdict()["poolMember_status"])
                #获取pool成员状态图标
                poolMember_Img=self.get_poolMemberImg(poolMember_info.groupdict()["poolMember_img"])
                print poolMember_name,poolMember_status,poolMember_Img
        #由于URLError是HTTPError的父类，所以将子类异常写到父类异常之前
        except urllib2.HTTPError,e:
            print e.code #HTTPError实例有一个code属性，为http错误状态码
        except urllib2.URLError,e:
            print e.reason #若出现url错误，则打印出具体错误信息
    
    
    
    
    
    
    
    
    
    
    