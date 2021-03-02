# -*- coding: utf-8 -*-
# @Time    : 2021/02/28
# @update  : 2021/02/28
# @Author  : syncday

import requests
from lxml import etree
from Core.Img_download import download_image
from Core import Windows

class Image:
    Url, Artist, Tag, Id, Posted, Size, Source, Rating, Score = ['', '', [], '', '', '', '', '', '']


class Links:
    TAG = 'https://gelbooru.com/index.php?page=post&s=list&tags='
    POST = 'https://gelbooru.com/index.php?page=post&s=view&id='

headers = None

def set_headers(header:dict):
    global headers
    headers = header

def deal_with_url(url: str):
    try:
        if Links.TAG in url:
            __deal_with_url_of_tag(url)
        elif Links.POST in url:
            __deal_with_url_of_post(url)
        else:
            Windows.change_title('出错')
            print("\r无法处理该链接")
    except requests.ConnectTimeout as e:
        print("\r无法连接到网站[%s]" % e)
        Windows.change_title('出错')


def __deal_with_url_of_post(url: str):
    """处理图片网页的链接"""
    Windows.change_title("获取图片信息...")
    try:
        html = __get_html(url)
    except Exception as e:
        Windows.change_title('出错')
        print("\r获取图片信息失败[%s]"%e)
        return
    artist = __get_post_artist(html)
    tags = __get_post_tags(html)
    statistics = __get_post_statistics(html)
    original_image_url = __get_post_original_image_url(html)

    image = Image()
    if artist is not None and len(artist)>0:
        image.Artist = artist[0]
    if tags is not None and len(tags)>0:
        image.Tag = str(tags)
    if original_image_url is not None and len(original_image_url)>0:
        image.Url = original_image_url[0]
    if statistics is not None and len(statistics)>0:
        for item in statistics:
            item = item.split(': ',1)
            if item is not None and len(item)==2:
                image.__dict__[item[0]] = item[1]
    __download(image)


def __deal_with_url_of_tag(url: str):
    """处理TAG网页的链接"""
    has_next = True
    while has_next:
        pid = url.split('pid=')[-1] if 'pid='in url else '0'
        Windows.change_title("获取pid=%s的Tag网页图片信息..."%pid)
        html = __get_html(url)
        if html is None:
            return
        post_url_list = __get_post_url_list(html)
        if post_url_list is not None and len(post_url_list)==0:
            Windows.change_title("无法获取pid=%s的Tag网页图片信息..." % pid)
        for post_url in post_url_list:
            __deal_with_url_of_post(post_url)
        has_next = True if __get_next_page_url(html) is not None and len(__get_next_page_url(html)) > 0 else False
        if has_next:
            url = "https://gelbooru.com/index.php"+__get_next_page_url(html)[0]


def __get_html(url):
    """获取网页数据"""
    return etree.HTML(requests.get(url, headers=headers, timeout=30).text)


def __get_post_url_list(html) -> list:
    """获取图片列表的帖子链接"""
    return html.xpath('//article[@class="thumbnail-preview"]/a/@href')


def __get_next_page_url(html):
    return html.xpath('//div[@id="paginator"]/b/following-sibling::a[1]/@href')


def __get_post_artist(html) -> list:
    """获取原图作者"""
    return html.xpath('//li[@class="tag-type-artist"]/a/text()')


def __get_post_original_image_url(html) -> list:
    """获取原图下载链接"""
    return html.xpath('//a[@rel="noopener"]/@href')


def __get_post_tags(html) -> list:
    """获取tag"""
    return html.xpath('//li[@class="tag-type-general"]/a/text()')


def __get_post_statistics(html) -> list:
    """获取Statistics数据"""
    statistics = []
    elements = html.xpath('//li[@class="tag-type-general"][last()]/following-sibling::li[2]/following-sibling::li')[:6]
    for e in elements:
        item_text = e.text
        children = e.getchildren()
        for child in children:
            if child.text is None:
                break
            if child.get('href') is not None:
                item_text = item_text + child.get('href')
                break
            item_text = item_text + child.text
            break
        statistics.append(item_text)
    return statistics

def __download(image:Image):
    Windows.change_title("下载图片...")
    download_info = download_image(image.Url,image.Id)
    if download_info.result ==1:
        Windows.change_title("完成")
    elif download_info.result ==0:
        Windows.change_title("取消")
    else:
        Windows.change_title("失败")
    print("\r%s,save_path=%s"%(download_info.info,download_info.path))
