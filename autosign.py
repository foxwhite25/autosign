import traceback
from datetime import datetime

import schedule
import time
import logging

from imgurpython import ImgurClient

from config import email
from fancy import ColoredLogger, rootLogger
from chrome_test import chrome_test, YzmFailedError

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
from mail import Mail


def email_remind(reason: str):
    if email:
        mail = Mail()
        dt = datetime.today()
        title = f'[{dt.month}-{dt.day}] AutoSign JNU health system failed'
        body = f'Auto sign failed, please check https://stuhealth.jnu.edu.cn/#/login if it is recorded or not.\n' \
               f'If there is a bug please report to https://github.com/foxwhite25/autosign/issues\n\n' \
               f'Reason: \n{reason}'
        mail.send([mail.user], title, body)
        rootLogger.error(f'Email sent! {reason=}')
    else:
        rootLogger.error(reason)


def check(chrome):
    try:
        chrome.check()
    except YzmFailedError:
        main()


def main():
    chrome = chrome_test()
    for tries in range(20):
        try:
            rootLogger.info('Attempt Login')
            chrome.enter_data()
            chrome.run_yzm()
            time.sleep(2)
            chrome.login()
            time.sleep(3)
            if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/login':
                raise YzmFailedError
            rootLogger.info('Login successful')
            break
        except YzmFailedError:
            rootLogger.error('Seems like yidun failed, retrying')
            chrome.driver.refresh()
            time.sleep(3)
            continue
    else:
        email_remind('Yidun Failed 20 times in a row, might have a bug.')
        chrome.driver.save_screenshot('images/ss.png')
        client_id = '26ef60418369362'
        client_secret = '34f16664ae94027ed1d33eb50513f0c4e6e11dde'
        client = ImgurClient(client_id, client_secret)
        image = client.upload_from_path('images/ss.png')
        print("Image link:" + image.link)
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
    rootLogger.info('Completed today, initiate check.')
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
