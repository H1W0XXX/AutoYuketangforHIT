原版GitHub地址：[https://github.com/xrervip/AutoYuketangforHIT](https://github.com/xrervip/AutoYuketangforHIT)
相对于原版，此版本变更如下
1 只能cookie登录
2 移除2倍速
3 修改了雨课堂对应的变更，使得现在（2020年11月）能正常使用
4 以后更新看心情



代码基于 [https://github.com/lingyan12/yuketang](https://github.com/lingyan12/yuketang) 和[https://github.com/xrervip/HIT_auto_report/blob/master/HIT_auto_report.py](https://github.com/xrervip/HIT_auto_report/blob/master/HIT_auto_report.py) 进行修改


**使用方法：**
依赖于python运行环境+chorme+selenium chromedriver驱动

 1. 安装Chorme浏览器
 2. 下载安装**python运行环境**+**selenium 包**+ **chromedriver驱动**    selenium可以直接可以用pip安装。`pip install selenium` 。chormedriver 镜像地址: [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/) 寻找对应您的chrome浏览器的版本即可，解压后将`chromedriver.exe`文件放在chrome浏览器根目录，也就是`chrome.exe`同目录下，同时需要将该目录添加到`环境变量`里 [第二步教程](https://www.cnblogs.com/lfri/p/10542797.html)
 4. 配置`config.json`  ：文件格式如在**附录2** 在URL中替换为雨课堂（学堂在线）对应课程的`成绩单`页，例如： **附录1** `https://hit.yuketang.cn/pro/lms/******/*****/score`
 5. 启动python脚本 
 6. 备注：使用参数 CookieMode 可以在**附录3**`cookie.json` 写入cookie并进行快捷登录（非必须）


此版本的使用方法
1 正常登录获取cookie（看下面）并且修改cookie.json文件
2 修改config.json文件，把自己课程的url填进去
3 运行python
4 耐心等待所有的课程url被获取（如果没有全部获取，要从头开始）
5 开始播放
6 如果接着上次的刷，cookie可能有变动，重新改cookie.json文件（建议直接丢服务器上挂机，中间别断）

---
~~## 附录1：网页页面
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200925164844953.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0ZyYW5rbGluc19GYW4=,size_16,color_FFFFFF,t_70#pic_center)

移除了扫码登录，只能cookie登录


---
## 附录2：config.json
在URL中替换为雨课堂（学堂在线）对应课程的链接即可
**config.json**
把 ~~https://hit.yuketang.cn/pro/lms/8692P78g7Lk/4412088/score~~ 改成自己的课程
```c
[{
	"URL":"https://hit.yuketang.cn/pro/lms/8692P78g7Lk/4412088/score"
}]
```

---
## 附录3：cookie.json
以下内容必须
把 hit.yuketang.cn 改成自己的学校的网站

**cookie.json:**

```json
[{
		"domain": "hit.yuketang.cn",
		"name": "sessionid",
		"path": "/",
		"value": "替换为数值"
	},
	{
		"domain": "hit.yuketang.cn",
		"name": "csrftoken",
		"path": "/",
		"value": "替换为数值"
	},
	{
		"domain": "hit.yuketang.cn",
		"name": "platform_id",
		"path": "/",
		"value": "替换为数值"
	},
	{
		"domain": "hit.yuketang.cn",
		"name": "university_id",
		"path": "/",
		"value": "替换为数值"
	},
	{
		"domain": "hit.yuketang.cn",
		"name": "user_role",
		"path": "/",
		"value": "替换为数值"
	}
]
```
---

## 附录4：如何获取Cookie?
这里谈一个比较简单但是繁琐的方法
 ### 1.首先在浏览器地址栏旁边点击这个按钮 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200925171529155.png#pic_center)
### 2.点击Cookie
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200925171658840.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0ZyYW5rbGluc19GYW4=,size_16,color_FFFFFF,t_70#pic_center)
### 3.获取Cookie
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200925171727355.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0ZyYW5rbGluc19GYW4=,size_16,color_FFFFFF,t_70#pic_center)
然后将域名下Cookie文件夹中的几个cookie获取下来，将`内容`中的数值（`fzbYQfMAyui8j0CQRRaPze0fFA1emawT`）填写到上面 `cookie.json` 中 的`"value": "替换为数值"`



