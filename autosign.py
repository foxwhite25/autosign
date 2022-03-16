import traceback
from datetime import datetime

import schedule
import time
import logging
import colorlog
from imgurpython import ImgurClient
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(name)-15s] [%(levelname)-7s]: %(message)s (%(filename)s:%(lineno)d)",
        "%Y-%m-%d %H:%M:%S")
)

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

from mail import Mail
from config import email
from chrome_test import chrome_test, YzmFailedError


def email_remind(reason: str):
    if email:
        mail = Mail()
        dt = datetime.today()
        title = f'[{dt.month}-{dt.day}] AutoSign JNU health system failed'
        body = f'Auto sign failed, please check https://stuhealth.jnu.edu.cn/#/login if it is recorded or not.\n' \
               f'If there is a bug please report to https://github.com/foxwhite25/autosign/issues\n\n' \
               f'Reason: \n{reason}'
        mail.send([mail.user], title, body)
        logger.info(f'Email sent! {reason=}')
    else:
        logger.error(reason)


def check(chrome):
    try:
        chrome.check()
    except YzmFailedError:
        main()


def main():
    chrome = chrome_test()
    for tries in range(100):
        logger.info(f"Launched {tries}tries")
        try:
            logger.info('Attempt Login')
            chrome.enter_data()
            chrome.run_yzm()
            time.sleep(0.5)
            chrome.driver.save_screenshot('images/ss.png')
            chrome.login()
            try:
                text_box = chrome.driver.find_element(By.CLASS_NAME, 'alert')
                logger.error(text_box.text)
                raise YzmFailedError
            except NoSuchElementException:
                pass
            time.sleep(3)
            if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/login':
                raise YzmFailedError
            logger.info('Login successful')
            break
        except YzmFailedError:
            logger.error('Seems like yidun failed, retrying')
            chrome.driver.refresh()
            time.sleep(3)
            continue
    else:
        email_remind('Yidun Failed 100 times in a row, might have a bug.')
        raise YzmFailedError
    if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/index/complete':
        email_remind('Already completed today, checking')
        check(chrome)
        return False
    if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/index/cantwrite':
        email_remind('Need to wait 6 hour before another form, retrying in 6 hour')
        time.sleep(6 * 60 * 60)
        main()
        return False
    chrome.submit()
    logger.info('Completed today, initiate check.')
    time.sleep(3)
    check(chrome)
    return True


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        trace = traceback.format_exc()
        email_remind(trace)
    schedule.every().day.at("00:10").do(main)  # 每天0010自动开始
    schedule.every().day.at("12:10").do(main)
    while True:
        try:
            schedule.run_pending()
            time.sleep(10)
        except Exception as ex:
            trace = traceback.format_exc()
            email_remind(trace)
