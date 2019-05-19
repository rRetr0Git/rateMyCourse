# selenium自动化测试

标签（空格分隔）： python Bug

---

文档参考了一下博客文章：
[以后再有人问你selenium是什么，你就把这篇文章给他](https://blog.csdn.net/TestingGDR/article/details/81950593)
如需要使用，请根据链接中的指示搭建相应环境，共2大步骤：
- 在Windows搭建和部署Selenium工具
- 配置浏览器和驱动
##1.4 Selenium WebDriver API的使用
在程序开头加上导入代码，并根据自己浏览器创建相应的driver
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver = webdriver.Ie()
```
###1.4.1 控制浏览器
代码|对应功能
:---:|:---:
driver.get(str1)|打开对应网址
driver.maximize_window()|窗口最大化
driver.set_window_size(width, height)|设定窗口大小
driver.back()|后退
driver.forward()|前进
driver.close()|关闭浏览器
driver.quit()|退出

###1.4.2 元素定位操作
需要返回一个元素，使用
driver.find_element_by_<Method>(<Parameter>)
需要返回多个元素，使用
driver.find_elements_by_<Method>(<Parameter>)
selenium提供了以下定位元素的方法：
Method字段值|定位依据
:---:|:---:
id|ID的属性值
name|name的属性值
class_name|class的名称值
tag_name|tag的名称值
link_text|链接文字
partial_link_text|部分链接文字
xpath|XPath
css_selector|CSS选择器

代码示例：
```python
from selenium import webdriver

driver = webdriver.Ie()
driver.get("https://www.icourse.club")

element = driver.find_element_by_tag_name("body")
```

###1.4.3 鼠标事件操作
常用单击操作，代码为
```
element.click()
```
###1.4.4 键盘事件操作
常用键入操作，代码为
```
element.send_keys(str)
```
其它鼠标和键盘事件操作不一一列举，有需要请点击文章开头的链接。
