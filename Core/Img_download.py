# -*- coding: utf-8 -*-
# @Time    : 2021/02/09
# @update  : 2021/02/09
# @Author  : syncday

import requests
import time
from os import path
from collections import namedtuple
from contextlib import closing

DownloadInfo = namedtuple('DownloadInfo', ['result', 'info', 'url', 'name', 'type', 'size', 'path', 'time'])


def __fix_save_path(image_size: int, image_type: str, filename: str, dir_path: str, redownload_exists: bool):
    """确定下载文件的文件名和下载位置"""
    dir_path = path.dirname(__file__) if dir_path is None or len(dir_path)==0 else dir_path
    save_path = path.join(dir_path, filename)
    if redownload_exists is True or image_size == 0:
        return save_path + '.' + str(image_type)
    if path.exists(save_path + '.' + str(image_type)):
        if int(image_size) == path.getsize(save_path + '.' + image_type):
            return None
        save_path = save_path + '-' + str(image_size)
    if path.exists(save_path + '.' + image_type):
        return None
    return save_path + '.' + image_type


def download_image(url:str, file_name:str, dir_path:str=None, headers:dict=None, redownload_exists:bool=False,
                   ignore_warning=False) -> DownloadInfo:
    image_size = 0  # 默认图片大小，用于异常处理
    image_type = 'jpg'  # 默认图片类型，用于异常处理
    image_save_path = None
    start_time = time.time()  # 开始时间戳
    try:
        with closing(requests.get(url, headers=headers, stream=True, timeout=30)) as response:
            chunk_size = 1024  # 单次请求数据的最大值,1KB
            content_length = response.headers.get('Content-Length')
            content_type = response.headers.get('Content-Type')

            if ignore_warning is False and 'image' not in content_type and 'video' not in content_type:
                image_size = None
                image_type = None
                raise Exception("该链接指向的不是图片资源，Content-Type[%s]" % content_type)
            if ignore_warning is False and content_length is None:
                image_size = None
                image_type = None
                raise Exception("无法获取链接指向资源的大小")

            image_size = int(content_length)
            image_type = content_type[6:] if 'image' in content_type or 'video' in content_type else image_type
            image_save_path = __fix_save_path(image_size, image_type, file_name, dir_path, redownload_exists)
            if image_save_path is None:
                return DownloadInfo(0, '下载取消[图片%s已存在]'%file_name, url, file_name, image_type, image_size, None, 0)
            unit = 'KB' if image_size < 1024 * 1024 else 'MB'
            unit_size = 1024 if unit == 'KB' else 1024 * 1024

            downloaded_size = 0
            with open(image_save_path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    downloaded_size = downloaded_size + len(data)
                    process = (downloaded_size / image_size) * 100
                    if image_size > 0:
                        print("\r\r下载%s.%s：%d%%(%.1f%s/%.1f%s) - %s" % (file_name,image_type, process, downloaded_size / unit_size, unit,
                                                                   image_size / unit_size, unit, url),
                              end="")
            print("\r\r", end="")
        return DownloadInfo(1, '下载成功', url, file_name, image_type, image_size, image_save_path,
                            "%.1f" % (time.time() - start_time))
    except Exception as e:
        return DownloadInfo(-1, '下载失败[%s]' % e, url, file_name, image_type, image_size, None, 0)
