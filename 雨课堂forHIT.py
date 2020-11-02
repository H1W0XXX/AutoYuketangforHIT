#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/9/22 18:36
# @Author: f
# @File  : 雨课堂forHIT.py

"""
代码基于 https://github.com/lingyan12/yuketang 和https://github.com/xrervip/HIT_auto_report/blob/master/HIT_auto_report.py 进行修改
依赖于python运行环境+chrome+selenium chrome驱动
selenium chrome驱动 镜像地址: http://npm.taobao.org/mirrors/selenium

说明：使用参数 CookieMode 可以在cookie，json 写入cookie并进行快捷登录
"""
import os
import re


import platform
import json
from selenium.webdriver.chrome.options import Options
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support import expected_conditions  as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class AutoYuketangforHIT:
    home_url = 'https://yuketang.cn/'  # 改成自己学校的，cookie.json也改成自己学校的
    course_url = ""
    courseID=""
    def __init__(self, mode):

        isCookieMode = True
        if "CookieMode" in mode:
            isCookieMode = True

        self.setDriver()

        """使用CookieMode登录"""
        self.loadCookie(isCookieMode)

        self.readFromJSON()  # 从JSON读入URL

        self.load_url(self.course_url)

        self.login(isCookieMode)

        while True:
            time.sleep(0.1)
            if self.driver.current_url == self.course_url:
                print("成功登录雨课堂")
                break

        self.prepare_list('url_list.txt')
        self.PlayAllVideo('url_list.txt')

        self.driver.quit()

    def PlayAllVideo(self, location):
        """
        播放全部的视频
        :param location:  文件的位置
        :return:
        """

        url_list = self.read_url_list(location)

        for url in url_list:
            self.PlayVideo(url)

        print("完成url_list中全部任务")

    def PlayVideo(self, url):
        """
        播放全部的视频
        :param url: 网课的URL
        :return:
        """
        print(url)
        self.load_and_wait_url(url)  # 切换到新的窗口



        try:
            work_persent = self.wait_and_getText(
                '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[2]/div/div/section[1]/div[2]/div/div/span')
        except TimeoutException:
            work_persent = "任务进度元素加载失败"  # 元素加载失败
        if work_persent == '完成度：100%':
            return
        print(work_persent)
        time.sleep(3)
        print('播放1')
        # js1 = 'document.querySelector("#video-box > div > xt-wrap > xt-controls > xt-inner > xt-playbutton").click();'
        # self.driver.execute_script(js1)
        self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/div/div/section[2]/div[1]/div/div/div/xt-wrap/xt-controls/xt-inner/xt-playbutton').click()
        print('播放2')
        time.sleep(2)
        toTime = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/div/div/section[2]/div[1]/div/div/div/xt-wrap/xt-controls/xt-inner/xt-time/span[2]').get_attribute('textContent')
        time.sleep(1)
        while 1:
            curTime = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/div/div/section[2]/div[1]/div/div/div/xt-wrap/xt-controls/xt-inner/xt-time/span[1]').get_attribute('textContent')
            print(toTime[3:5], curTime[3:5])
            if toTime[3:5] == curTime[3:5]:
                toTime = '00:00:00'
                curTime = '00:11:00'
                return
            else:
                time.sleep(5)



    def prepare_list(self, location):
        """
        为播放准备连接
        :param location: 保存网课连接的文件地址
        :return:
        """

        self.courseID="$"+re.match("https://[a-zA-Z0-9.]*/[a-zA-Z]*/[a-zA-Z]*/[a-zA-Z0-9]*/([0-9]+)/score", self.driver.current_url).group(1)+"$"
        print("当前课程ID："+self.courseID)
        """如果文件不存在的话"""
        if not os.path.exists(location):
            print("URL文件不存在！创建文件")
            fp=open(location, 'w+', encoding='utf-8')
            fp.close()

        fp=open(location, 'r+', encoding='utf-8')
        lines = fp.readlines()  # 读取所有行
        last_line = ""
        if len(lines) != 0:
            last_line = lines[-1]  # 取最后一行
        if self.courseID  not in last_line:
            print("URL未构建或构建不完全")
            fp.close()
            self.get_list(location)
        else:
            fp.close()
            print("检测到校验位，已从历史记录中获取链接")

        print("全部链接已就绪")

        return

    def get_list(self, location):
        """
        爬取全部网课连接
        :param location:保存网课连接的文件地址
        :return:
        """
        with open(location, 'w+', encoding='utf-8') as fp:

            self.driver.get(self.course_url)
            self.wait_element_path(
                "/html/body/div[4]/div[2]/div[2]/div[3]/div/div[2]/div[2]/section[2]/div[2]/ul/li[1]/div[1]/div/span")
            botton = self.driver.find_elements(By.XPATH, "//span[@class='cursorpoint unit-name-hover']")
            print("正在爬取全部视频网页连接")
            for i in botton:
                i.click()
                handle = self.driver.current_window_handle  # 当前主窗口
                handles = self.driver.window_handles  # 全部窗口句柄
                # 对窗口进行遍历
                for newhandle in handles:
                    # 筛选新打开的窗口B
                    if newhandle != handle:
                        # 切换到新打开的窗口B
                        # browser.switch_to_window(newhandle) 旧版本
                        self.driver.switch_to.window(newhandle)
                        current_url = (self.driver.current_url + '\r')
                        if "/video/" in self.driver.current_url:
                            print(self.driver.current_url)
                            fp.writelines(current_url)
                            fp.flush()
                        self.driver.close()
                        self.driver.switch_to.window(handle)
                        time.sleep(0.5)
            fp.writelines(self.courseID)
            fp.flush()
            fp.close()
        return

    def read_url_list(self, location):
        url_list = []
        with open(location, 'r', encoding='utf-8') as fp:
            url_content = fp.readlines()
            for url in url_content:
                if self.courseID not in url:
                    url = url[:-1]
                    url_list.append(url)
            fp.close()
        return url_list

    def login(self, isCookieMode):
        """
          雨课堂登录
          :param isCookieMode:  如果使用cookie，则不需要登录
          :return:
          """

        if isCookieMode:
            return
        print("登录雨课堂")

        self.load_url(self.home_url)
        self.wait_element_path('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button').click()
        while True:
            self.load_url(self.course_url)
            time.sleep(5)
            if self.course_url == self.driver.current_url:
                return

    def loadCookie(self, isCookieMode):
        """
        从cookie载入登录信息
        :return: 是否成功载入cookie
        """
        if not isCookieMode:
            return

        print("从Cookie文件加载登录信息")
        try:
            f = open("./cookie.json", 'r', encoding='utf-8')
        except FileNotFoundError:
            print("未检测到Cookie.json，需要进行手动登录")
            return False

        """载入cookie"""
        cookies = json.load(f)

        self.load_url(self.home_url)
        self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        return True

    def setDriver(self):
        """
        根据系统环境配置chormedriver
        :return:
        """
        chrome_options = Options()
        sysstr = platform.system()

        if (sysstr == "Linux"):  # for Linux
            chrome_options.add_argument('--headless')  # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
            chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--mute-audio")  # 静音播放

        else:  # for other OS
            chrome_options.add_argument("--mute-audio")  # 静音播放

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        print("成功配置chrome驱动")

    def load_and_wait_url(self, target_url, timeout=10.0):
        """
        等待直到url更新为目标url
        :param target_url: 预计更新后的目标url
        :param timeout: 超时时间
        :return:
        """
        self.load_url(target_url)
        while target_url != self.driver.current_url and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
        if timeout <= 0:
            raise TimeoutException()

    def wait_element_path(self, element_xpath):
        """
        等待相应xpath的元素加载完成
        :param element_xpath: 元素xpath
        :return: 对对应的元素
        """
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        return element



    def wait_and_click(self, element_xpath):
        """
        等待相应id的元素加载完成后点击元素
        :param element_xpath: 元素path
        :return:
        """
        element = self.wait_element_path(element_xpath)
        element.click()

    def wait_and_getText(self, element_xpath):
        """
        等待相应id的元素加载完成后点获取其中的文字信息
        :param element_xpath: 元素path
        :return:
        """
        element = self.wait_element_path(element_xpath)
        return element.text

    def readFromJSON(self):
        """
        从JSON中读取数据，并写入URL
        :return:
        """
        try:
            f = open("./config.json", 'r', encoding='utf-8')
        except FileNotFoundError:
            print("config.json文件不存在，请检查！")

        data = json.load(f)
        self.course_url = data[0]["URL"]

        print("读取json文件")

    def load_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)


if __name__ == '__main__':

    mode = ""
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    AutoYuketangforHIT(mode)
