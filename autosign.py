import traceback
from datetime import datetime

import schedule
import time
import logging

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
        mail.send([mail.user],title,body)
        rootLogger.error(f'Email sent! {reason=}')
    else:
        rootLogger.error(reason)


def main():
    chrome = chrome_test()
    for tries in range(20):
        try:
            rootLogger.info('Attempt Login')
            chrome.enter_data()
            chrome.run_yzm()
            time.sleep(1)
            if chrome.driver.find_element_by_class_name('yidun_tips__text').text:
                raise YzmFailedError
            chrome.login()
            time.sleep(1)
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
        return False
    if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/index/complete':
        email_remind('Already completed today, quitting')
        return False
    if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/index/cantwrite':
        email_remind('Need to wait 6 hour before another form, retrying in 6 hour')
        time.sleep(6 * 60 * 60)
        main()
        return False
    chrome.submit()
    rootLogger.info('Completed today, quitting')
    time.sleep(10)
    return True


if __name__ == '__main__':
    main()
    schedule.every().day.at("00:10").do(main)  # 每天0010自动开始
    while True:
        try:
            schedule.run_pending()
            time.sleep(10)
        except Exception as ex:
            trace = traceback.format_exc()
            email_remind(trace)
