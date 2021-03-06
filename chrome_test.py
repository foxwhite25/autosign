# -*- encoding: utf-8 -*-
import datetime
import logging
import random
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import config, headless
from yidun import yidun_crack

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.headless = headless
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument(
    "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'"
)
rootLogger = logging.getLogger('chrome')


class YzmFailedError(Exception):
    pass


class chrome_test(object):
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver.exe')
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
        yidun = yidun_crack()
        button_element = self.driver.find_element(By.CLASS_NAME, 'yidun_slider')
        ActionChains(self.driver).move_to_element(button_element).perform()
        time.sleep(1)
        # 下载验证码进行识别
        bg_img_src = self.driver.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute("src")
        front_img_src = self.driver.find_element(By.CLASS_NAME, "yidun_jigsaw").get_attribute("src")
        bg_img_path = yidun.download_img(bg_img_src)
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
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'appId'))
            )
        except TimeoutException:
            self.driver.save_screenshot('images/ss.png')
        username, password = config
        self.driver.find_element(By.NAME, 'appId').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        rootLogger.info(f'Entered {username=}, password={len(password) * "*"}.')

    def login(self):
        self.driver.find_element(By.CLASS_NAME, 'btn').click()
        rootLogger.info(f'Clicked Login Button.')

    def submit(self):
        today = datetime.date.today().isoformat()
        for id in ['cjtw', 'wujtw', 'wajtw']:
            self.driver.find_element(By.ID, id).send_keys("{:.1f}".format(36 + random.random()))
        for id in ["twyjcrq", "twejcrq", "twsjcrq"]:
            self.driver.execute_script(f"document.getElementById('{id}').removeAttribute('readonly',0);")
            self.driver.find_element(By.ID, id).send_keys(today)
        self.driver.find_element(By.ID, '10000').click()
        rootLogger.info(f'Checked box.')
        self.driver.find_element(By.ID, 'tj').click()
        rootLogger.info(f'Submitted form.')

    def check(self):
        rootLogger.info("Start checking")
        self.driver.get('https://stuhealth.jnu.edu.cn/#/index/submitlist')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'fa'))
        )
        check = self.driver.find_element(
            By.XPATH,
            '/html/body/app-root/app-index/div/div[1]/app-submit-list/'
            'section/section/div/div/div/div/div/div[2]/span[2]'
        )
        if 'fa-check' in check.get_attribute('class'):
            rootLogger.info("Check successful, quitting")
        else:
            rootLogger.error("Check failed, retrying")
            raise YzmFailedError

    def __del__(self):
        self.driver.close()
