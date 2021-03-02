# Easy-Download-For-Gelbooru
Gelbooru原图简洁下载器。

**亮点**：可以从浏览器拖动图片或者Tag链接到下载窗口来添加新的下载任务

## 需要安装的库requests，PyQt5，lxml

### py文件讲解
- mian.py 程序入口
- Windows.py 创建PyQt的窗口
- Gelbooru.py 主要处理给予链接的信息页面，获取原图链接以及一些图片信息和获取Tags页面的每一页的所有原图链接
- Img_download.py 根据图片直链，下载图片

*如果没有获取到想要的Tag页面时，请检查是否配置了Cookie(即headers,可以调用Gelbooru.set_headers来设置)*

***请勿滥用***
