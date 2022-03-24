import os

config = (os.getenv('JNU_ID'), os.getenv('JNU_PW'))
# 可以修改为(学号，密码)，必须为str
headless = False
# 是否启用Headless模式，启用时不会弹出Chrome窗口
email_config = ('', '')
# 修改为(邮箱，密码)，必须为str，如果非gmail请找到你的邮箱的smtp并填入mail.py
email = False
# 是否使用邮件提醒，如果为否上面可以不用填
