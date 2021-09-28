# -*- encoding: utf-8 -*-
import logging
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import config,headless
from fancy import rootLogger
from yidun import yidun_crack

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.headless = headless
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


class YzmFailedError(Exception):
    pass


class chrome_test(object):
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://stuhealth.jnu.edu.cn/#/login')
        # self.driver.get('http://localhost:63342/yidun/slider.html?_ijt=1v4ljncju1r9naf69h6p4nt0k6')

    def run_yzm(self):
        # 滚动到顶部进行tab页切换
        self.driver.execute_script("window.scrollTo(0,0)")
        # 网页异步加载，等待拖动按钮出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'yidun_slider'))
        )
        time.sleep(1)
        rootLogger.info('Processing yidun')
        button_element = self.driver.find_element_by_class_name('yidun_slider')
        ActionChains(self.driver).move_to_element(button_element).perform()
        # 下载验证码进行识别
        yidun = yidun_crack()
        bg_img_src = self.driver.find_element_by_class_name("yidun_bg-img").get_attribute("src")
        bg_img_path = yidun.download_img(bg_img_src)
        front_img_src = self.driver.find_element_by_class_name("yidun_jigsaw").get_attribute("src")
        front_img_path = yidun.download_img(front_img_src)
        yidun.bg_img_path = bg_img_path
        yidun.front_img_path = front_img_path
        distance = yidun.tell_location()
        tracks = yidun.generate_tracedata(distance)
        # 进行拖动
        ActionChains(self.driver).click_and_hold(button_element).perform()
        t1 = int(time.time() * 1000)
        for i in range(len(tracks)):
            x = tracks[i]
            x_offset = x[0] if i == 0 else x[0] - tracks[i - 1][0]  # x轴距离差
            y_offset = x[1]
            ActionChains(self.driver).move_by_offset(x_offset, y_offset).perform()
            t = int(time.time() * 1000) - t1
            rootLogger.info(f"{t=}, {x_offset=}")
            tracks[i][2] = t
        ActionChains(self.driver).release().perform()
        # yidun.draw_tracks(tracks)

    def enter_data(self):
        username, password = config
        self.driver.find_element_by_name('appId').send_keys(username)
        self.driver.find_element_by_name('password').send_keys(password)
        rootLogger.info(f'Entered {username=}, password={len(password)* "*"}.')

    def login(self):
        self.driver.find_element_by_class_name('btn').click()
        rootLogger.info(f'Clicked Login Button.')

    def submit(self):
        self.driver.find_element_by_id('10000').click()
        rootLogger.info(f'Checked box.')
        self.driver.find_element_by_id('tj').click()
        rootLogger.info(f'Submitted form.')

    def __del__(self):
        self.driver.close()
