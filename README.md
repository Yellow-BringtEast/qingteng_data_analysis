# 项目说明

## 重要声明

本项目主要基于青藤之恋匿名投票贴评论数据，分析当代年情人赛博相亲时，对有关异地恋、彩礼、性别对立等话题的思考。基于大样本数据，全面剖析当代年轻人的恋爱观和婚姻观。本项目仅供学习交流使用，请勿用于商业用途，否则后果自负。

## 项目介绍

本项目数据基于Mitmproxy中间人攻击和微信PC端小程序抓包获取，所有数据经过脱敏处理，仅包含项目分析所需基本字段，不包含个人隐私信息。

## 项目进度

- [x] 框架搭建
- [x] 数据获取
- [x] 数据清洗
- [x] 数据分析
- - [x] 词云分析
- - [x] 情感倾向分析
- [x] 数据可视化

## 数据获取

### 微信小程序抓包

Mitmproxy中间人攻击是一种网络代理工具，可以截获和修改网络请求和响应。

1. 安装Mitmproxy

```bash
pip install mitmproxy
```

安装完成后，可以使用`mitmproxy --version`查看是否安装成功。
![mitmproxy_install](res/mitmproxy_install1.png)

2. 安转mitmproxy-ca证书

- 打开终端，输入以下命令：`mitmproxy`，启动后，会在当前用户目录下生成一个`.mitmproxy`
  文件夹，进入该文件夹，点击`mitmproxy-ca-cert.cer`文件进行安装。

![mitmproxy_install](res/mitmproxy_install2.png)

![mitmproxy_install](res/mitmproxy_install3.png)

![mitmproxy_install](res/mitmproxy_install4.png)

![mitmproxy_install](res/mitmproxy_install5.png)]

![mitmproxy_install](res/mitmproxy_install6.png)

### 数据获取

1. 进入script目录，在终端中运行`mitmdump -s get_data.py -q`。

2. 开启代理

- 在设置中搜索`代理`，点击代理服务器设置。

![data_crawl](res/data_crawl1.png)

- 点击`手动代理`，输入`127.0.0.1`和`8080`端口，点击`保存`。

![data_crawl](res/data_crawl2.png)

3. 进入微信小程序，点击`村口` -> `村口投票`

![匿名投票贴](res/vote1.png)

4. 点击相关投票贴，滑动到底，即可完成数据采集，请注意控制滑动速度，滑动速度过快会被临时封禁。

5. 采集完成后，关闭终端，关闭手动代理，数据保存到`data`目录下。

### 数据分析

#### 词云分析

词云分析是一种数据可视化的方法，通过将文本转换为词频矩阵，然后将矩阵转换为词云图，从而得到文本的关键词。本项目提供jieba和[阿里云NLP基础服务](https://ai.aliyun.com/nlp?spm=5176.28508143.J_4VYgf18xNlTAyFFbOuOQe.161.e939154afbZt8q&scm=20140722.X_data-89d981f73a0142b256b9._.V_1)进行分词，基础版包括分词、词性标注等多个模型，并且每个模型提供每日50w次免费调用次数。

#### 情感分析

情感分析是指对文本进行情感分析，包括情感倾向分析和情感倾向预测。本项目使用[阿里云NLP基础服务](https://ai.aliyun.com/nlp?spm=5176.28508143.J_4VYgf18xNlTAyFFbOuOQe.161.e939154afbZt8q&scm=20140722.X_data-89d981f73a0142b256b9._.V_1)进行分析。

### 数据可视化


## 结语
- 本项目仓促上线，难免存在错误，欢迎大家指正。
- 如有侵权，请联系我删除。
- 如有建议，欢迎在Issues中提出。
- 如果觉得对您有帮助，请给个star。

## 致谢
- 感谢[Mitmproxy](https://mitmproxy.org/)提供的代理工具。
- 感谢[微信小程序](https://mp.weixin.qq.com/)提供的匿名投票数据。
- 感谢[阿里云NLP基础服务](https://ai.aliyun.com/nlp?spm=5176.28508143.J_4VYgf18xNlTAyFFbOuOQe.161.e939154afbZt8q&scm=20140722.X_data-89d981f73a0142b256b9._.V_1)
- 感谢jieba分词工具。
