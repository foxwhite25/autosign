import json

import requests
from requests.structures import CaseInsensitiveDict
import schedule
import time
import logging
import random

from config import get_data, get_login_data

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel('DEBUG')


def main():
    ran_time = random.randint(1, 30)
    rootLogger.info(f"Wait for {ran_time}s before continuing to create random time")
    time.sleep(ran_time)
    url = "https://stuhealth.jnu.edu.cn/api/write/main"
    url_login = "https://stuhealth.jnu.edu.cn/api/user/login"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["accept-language"] = "zh-CN,zh;q=0.9"
    headers["origin"] = "https://stuhealth.jnu.edu.cn"
    headers["referer"] = "https://stuhealth.jnu.edu.cn/"
    headers["sec-ch-ua"] = '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"'
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-fetch-dest"] = "empty"
    headers["sec-fetch-mode"] = "cors"
    headers["sec-fetch-site"] = "same-origin"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    headers["Content-Type"] = "application/json"
    data_login = get_login_data()
    try:
        rootLogger.info('Start login')
        resp = requests.post(url_login, headers=headers, data=data_login.encode('utf-8'))
        rootLogger.info('Response Code:' + str(resp.status_code))
        rootLogger.info('Response json:' + resp.text)
        jnuid = json.loads(resp.text)['data']['jnuid']
        rootLogger.info('Fetched jnuid:' + jnuid)
        data = get_data(jnuid)
        rootLogger.info('Start posting sign form')
        resp = requests.post(url, headers=headers, data=data.encode('utf-8'))
        rootLogger.info('Response Code:' + str(resp.status_code))
        rootLogger.info('Response json:' + resp.text)
    except Exception as e:
        rootLogger.error(e)


if __name__ == '__main__':
    main()
    schedule.every().day.at("08:50").do(main)  # 每天0850自动开始

    while True:
        schedule.run_pending()
        time.sleep(1)
