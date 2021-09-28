import os

config = (os.getenv('JNU_ID'), os.getenv('JNU_PW'))  # 可以修改为(学号，密码)，必须为str
headless = True  # 是否启用Headless模式，启用时不会弹出Chrome窗口
