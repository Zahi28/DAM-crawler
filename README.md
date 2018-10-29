# 音乐资源网页爬取（网易云音乐）

## 事先的准备：

在计算机上安装：urllib, beautifulsoup4；两个爬虫所需的库

以windows为例，运行：

>pip3 install urllib

>pip3 install beautifulsoup4

## 运行方法：

在命令行中转到本目录，运行：

>python pc_main.py

会提示输入歌手id

>singer id:

关于id需要去网易云音乐网页的[歌手页面](https://music.163.com/discover/artist)，选择一个想要爬取的歌手，
比如林俊杰，点击进入歌手页面；url中的“artist?id=3684”最后的一串数字就是歌手的id

在命令行中输入该id

>singer id:3684

便会爬取相关资源：

>download 那些你很冒险的梦

>download 醉赤壁

>download 当你

>...

直到下载完成

歌曲保存在songs目录下；歌词保存在lyrics目录下；封面保存在images目录下；metadata数据为music_json.json

## 说明

本方法通过网易云音乐外链爬取歌曲文件，通过网易云音乐提供的api链接爬取歌词，通过网页上的歌曲封面爬取图片信息

由于版权控制此方法可以爬取较多数歌手的及大部分音乐，对于一些版权控制及其严格的，此处掠过，不做强行的爬取，例如
泰勒的love story开通会员后下载格式为ncm，暂时还没有找到好的解决方案，再如泰勒的look what you make me do这种需要单独付费的
一般也爬取不到内容；这两类虽然会有一个MP3文件产生但并没有内容，用来构建网页时须将这部分小文件过滤掉

# 声明：

_由于版权保护的问题，此方法只用于课程需要，不可作为商业用途，保护正版！_
