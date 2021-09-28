import schedule
import time
import logging

from fancy import ColoredLogger, rootLogger
from chrome_test import chrome_test, YzmFailedError

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")



def main():
    chrome = chrome_test()
    while True:
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
    if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/index/complete':
        rootLogger.info('Already completed today, quitting')
        return False
    if chrome.driver.current_url == 'https://stuhealth.jnu.edu.cn/#/index/cantwrite':
        rootLogger.error('Need to wait 6 hour before another form, retrying in 6 hour')
        time.sleep(6 * 60 * 60)
        main()
        return False
    chrome.submit()
    rootLogger.info('Completed today, quitting')
    return True


if __name__ == '__main__':
    main()
    schedule.every().day.at("00:10").do(main)  # 每天0010自动开始
    while True:
        schedule.run_pending()
        time.sleep(10)
