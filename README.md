# Extractor.py
####It's a burp extension.
-----------------------
####　　为Burp Suite的扩展。监听Burp中的Proxy、Spider、Repeater、Intruder工具，利用正则表达式，提取Response中的链接或Email等信息。
========

##Notes：

* 1.可以提取google搜索结果的所有链接。 
* 2.可以提取baidu搜索结果的所有链接。 
* 3.可以只提取搜索结果中所有链接的域名。 
* 4.可以提取网页（包括google或baidu等搜索结果）中所有的Email. 
* 5.可以自定义正则表达式提取网页中所需信息（这个需要对正则表达式比较熟悉，里面预设了提取链接、域名和Email的正则）。

========
##Usages:

* 扩展是用python写的，因此需要在Extender配置python环境，加载jython-standalone-2.7.0.jar[下载地址](http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/2.7.0/jython-standalone-2.7.0.jar)，然后就可以加载本扩展了。

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot1.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot2.png)

* 为了方便，建立了两个文件：google.repeater和baidu.repeater，分别为google搜索和baidu搜索的Request。导入到Repeater中，在q=keyword中，把keyword替换为自己需要搜索的关键词然后点击Go，就可以提取需要的Response中链接或Email信息了。

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot3.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot4.png)

* 提取的信息输出到了Extender的Output，界面显示有限，最好保存到文件中。

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot5.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot6.png)

* 可以Send to Intruder，设置好Payload，一般google最多能显示1000条记录，每页100条，参数start从0到1000条，线程最好设置1，多线程时，输出的提取信息有时不会换行。（当然google搜索需要翻墙啊）

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot7.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot8.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot9.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot10.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot5.png)

* 可以抓包浏览器，extractor会监听Burp的Proxy，提取Response中的信息。

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot11.png)

* 可以Send to Spider，去自动爬，对提取Email很好啊。

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot12.png)

![](https://github.com/llq007/extractor/blob/master/Screenshot/screenshot13.png)	


