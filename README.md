[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">暨南大学健康打卡自动打卡脚本</h3>

  <p align="center">
    每天固定时间自动打卡
    <br />
    <a href="https://stuhealth.jnu.edu.cn/#/login">查看原网站</a>
    ·
    <a href="https://github.com/foxwhite25/autosign/issues">回报BUG</a>
    ·
    <a href="https://github.com/foxwhite25/autosign/issues">请求功能</a>
  </p>
</p>



<!-- 目录 -->
<details open="open">
  <summary><h2 style="display: inline-block">目录</h2></summary>
  <ol>
    <li>
      <a href="#关于这个脚本">关于这脚本</a>
      <ul>
        <li><a href="#特点">特点</a></li>
      </ul>
    </li>
    <li>
      <a href="#如何下载并且安装">如何下载并且安装</a>
      <ul>
        <li><a href="#必備條件">必備條件</a></li>
      </ul>
    </li>
    <li><a href="#使用方法">使用方法</a></li>
    <li><a href="#协议">协议</a></li>
    <li><a href="#联系">联系</a></li>
  </ol>
</details>



<!-- 关于这个脚本 -->
## 关于这个脚本
每天打卡是不是很麻烦，还需要每天登陆，滑条验证，点击提交，要做太多事情了（

这个脚本使用selenium和cv2破解滑条验证，并提交默认表单。



<!-- 如何安装 -->
## 如何下载并且安装

要得到一份本地副本，你只需要做以下这些简单的东西

### 安装

1. 克隆这个仓库
   ```sh
   git clone https://github.com/foxwhite25/autosign.git
   ```
2. 如果你没有安装需要的库，请使用pip安装
   ```sh
   pip install -r requirements.txt
   ```
3. 下载对应版本的Chrome Driver并放在根目录 
   ```
   http://npm.taobao.org/mirrors/chromedriver/
   ```
5. 修改 `config.py` 或者添加环境变量 `JNU_ID` 和 `JNU_PW`。分别为你的学号和密码
6. 打开 `start.bat` 或者shell中输入`python ./autosign.py`并看看是否能够成功登陆

<!-- USAGE EXAMPLES -->
## 使用方法
###Windows:
打开 `start.bat` 
###Linux:
输入`python ./autosign.py` 前景运行

输入`nohup python ./autosign.py &` 背景运行

输出将会保存于`nohup.out`文件

<!-- LICENSE -->
## 协议

GPL v3许可证分发。有关更多信息，请参见`LICENSE`。



<!-- CONTACT -->
## 联系

狐白白 - 1725036102 

项目地址: [https://github.com/foxwhite25/autosign](https://github.com/foxwhite25/autosign)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/foxwhite25/autosign.svg?style=for-the-badge
[contributors-url]: https://github.com/foxwhite25/autosign/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/foxwhite25/autosign.svg?style=for-the-badge
[forks-url]: https://github.com/foxwhite25/autosign/network/members
[stars-shield]: https://img.shields.io/github/stars/foxwhite25/autosign.svg?style=for-the-badge
[stars-url]: https://github.com/foxwhite25/autosign/stargazers
[issues-shield]: https://img.shields.io/github/issues/foxwhite25/autosign.svg?style=for-the-badge
[issues-url]: https://github.com/foxwhite25/autosign/issues
[license-shield]: https://img.shields.io/github/license/foxwhite25/autosign.svg?style=for-the-badge
[license-url]: https://github.com/foxwhite25/autosign/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[inkedin-url]: https://linkedin.com/in/foxwhite25