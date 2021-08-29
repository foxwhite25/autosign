from datetime import date
import logging
rootLogger = logging.getLogger()


def get_data(jnuid):
    today = date.today()
    d = today.strftime("%Y-%m-%d/")
    rootLogger.info('Current data:',d)
    # 在提交报告之前，在Chrome使用F12并切换到网络，点击清除资料，提交报告，点开第一个POST
    # 把form资料填入data之中，或者直接复制黏贴（记得不要把jnuid和d替换，并且对{}做转义）
    data = f"""
    {{
      "mainTable": {{
        "way2Start": "",
        "language": "cn",
        "declareTime": "{d}",
        "personNo": "",
        "personName": "",
        "sex": "",
        "professionName": "计算机科学与技术",
        "collegeName": "信息科学技术学院",
        "phoneArea": "",
        "phone": "",
        "assistantName": "潘俏逸",
        "assistantNo": "2016407",
        "className": "",
        "linkman": "",
        "linkmanPhoneArea": "",
        "linkmanPhone": "",
        "personHealth": "",
        "temperature": "",
        "personHealth2": "",
        "schoolC1": "",
        "currentArea": "",
        "backHubei": "",
        "way2Type1": "",
        "way2Type2": "",
        "way2Type3": "",
        "way2Type5": "",
        "way2Type6": "",
        "way2No": "",
        "personC4": "",
        "otherC4": "",
        "isPass14C1": "",
        "isPass14C2": "",
        "isPass14C3": ""
      }},
      "secondTable": {{
        "other13": "",
        "other1": "",
        "other3": "",
        "other5": "",
        "other4": "",
        "other7": "",
        "other6": "",
        "other10": "",
        "other11": "",
        "other12": ""
      }},
      "jnuid": "{jnuid}"
    }}
    """
    return data


def get_login_data():
    # 在登陆之前，在Chrome使用F12并切换到网络，点击清除资料，登陆，点开第一个POST
    # 复制黏贴填入资料
    return """
    {
        "username": "",
        "password": ""
    }
"""
