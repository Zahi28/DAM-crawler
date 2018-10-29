#  _*_ coding:utf-8 _*_
"""
@author: Zahi
@contact: xu_zixu@outlook.com
@file: pc_main.py
@time: 2018/10/19 12:35
"""
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import json
import re
# 泰勒 id=44266
# 林俊杰 id=3684
# 李荣浩 id=4292
singer_id = input('singer id:')
start_url = 'http://music.163.com/artist?id={}'.format(singer_id)           # 从网易云音乐的歌手页面爬取歌曲id
headers = {                                                                 # 设置响应头
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com'
}
req = Request(url=start_url, headers=headers)                               # urllib 获取服务器端响应
html = urlopen(req).read().decode('utf-8')
soup = BeautifulSoup(html, 'lxml')                                          # bs4 解析
singer_name = soup.find(id="artist-name").get_text()                        # 获取歌手名
links = soup.find('ul', class_='f-hide').find_all('a')                      # 提取到所有的特定的a标签
song_IDs = []
song_names = []
for link in links:
    song_ID = link.get('href').split('=')[-1]                               # 划分字符串，得到歌曲的id以及对应的歌名
    song_name = link.get_text()
    song_IDs.append(song_ID)
    song_names.append(song_name)
song_infos = zip(song_names, song_IDs)
count = 1                                                                   # 对歌曲进行编号 存储为json格式的metadata
with open('music_json.json', 'r', encoding='utf-8')as fp:
    json_file = json.load(fp)
musics_json = json_file["musics"]
for song_info in song_infos:                                                # 对每一首歌曲进行爬取
    headers = {                                                             # 响应头
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'http://music.163.com/',
        'Host': 'music.163.com'
    }
    # 歌曲外链
    song_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_info[1])
    # 歌曲网页页面用来爬取图片
    music_url = 'https://music.163.com/song?id={}'.format(song_info[1])
    # 网易云音乐的api 可以得到歌词
    lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(song_info[1]) + '&lv=1&kv=1&tv=-1'
    # 爬取歌曲封面图片
    req = Request(url=music_url, headers=headers)
    html = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    img_url = soup.find('img', class_='j-img').get('src')                   # 获得封面图片的url
    # 爬取歌词
    req = Request(url=lrc_url, headers=headers)
    html = urlopen(req).read().decode('utf-8')
    json_obj = json.loads(html)                                             # 结果是以json格式的需要调用json库进行解析
    initial_lyric = json_obj['lrc']['lyric']
    regex = re.compile(r'\[.*\]')                                           # 正则表达式去掉时间戳
    lyric = re.sub(regex, '', initial_lyric).strip()
    # 写入文件
    try:
        # json 格式
        # {
        #     "id": 123,
        #     "music": "江南",
        #     "singer": "林俊杰",
        #     "img_path": "images\\id.png",
        #     "music_path": "songs\\id.mp3",
        #     "lyric_path": "lyrics\\id.txt"
        # }
        music_id = '%03d' % count
        music_name = '{}'.format(song_info[0])
        img_path = 'images\\{}.png'.format(music_id)
        music_path = 'songs\\{}.mp3'.format(music_id)
        lyric_path = 'lyrics\\{}.txt'.format(music_id)
        music_json = {'id': music_id,
                      'music': music_name,
                      'singer': singer_name,
                      'img_path': img_path,
                      'music_path': music_path,
                      'lyric_path': lyric_path}
        with open(lyric_path, 'a', encoding='utf-8')as fp:
            fp.write(lyric)
        urlretrieve(img_url, img_path)
        urlretrieve(song_url, music_path)
        musics_json.append(music_json)
        print(song_info[1])
        count = count + 1
    except OSError:                                                          # 部分歌曲名字含有特殊字符，此处直接跳过不做处理
        continue

json_file["musics"] = musics_json
with open('music_json.json', 'w', encoding='utf-8')as fp:
    json.dump(json_file, fp, indent=4, ensure_ascii=False)
'''
可以爬到大部分网易云音乐上的歌曲（版权控制不是特别严格的歌曲）
但是相对严格的此方法无法实现例如：
泰勒的Look What You Made Me Do：会员也许单独购买
或者是会员可以下载但为.ncm的特有格式的
会员可以下载普通会员无法下载，并且下载后为.mp4的格式的可以爬取
'''
