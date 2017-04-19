#  _*_ coding: utf-8 _*_
# !/usr/bin/env python

import os
import vim


def creat_cache():
    vim_root = vim.eval('$VIM')            # 获取Vim根目录路径
    path = vim.eval('g:baidu_cache_path')  # 获取用户自定义缓存路径
    path = path.replace('$VIM', vim_root)  # 创建缓存路径
    if not os.path.exists(path):
        os.makedirs(path)                  # 创建缓存目录
    cache = '%s/item.txt' % path           # 缓存文件名及完整路径
    return cache


def scan_cache(info, cache):              # (str, str)
    if not os.path.isfile(cache):
        data = open(cache, 'w')           # 新建缓存文件
        data.close()
    else:
        info = "item/%s" % info
        data = open(cache, 'r')           # 读取缓存文件
        lines = iter(data.readlines())    # 将缓存内容转换为可迭代对象
        for eachline in lines:            # 执行迭代
            if eachline.strip() == info:  # 判断是否匹配到关键词
                return lines.next()       # 返回下一行的数据


def save_data(info, desc, cache):         # (str, str, str)
    data = open(cache, 'a')               # 打开缓存文件
    data.write('\nitem/%s\n' % info)      # 写入关键词
    data.write(desc.encode('utf-8'))      # 写入词条简介
    data.close()


def creat_temp(urls):                    # (str)
    if urls:
        temp = open('.BaiduTemp.txt', 'w+')   # 创建临时文件
        for each in urls:
            temp.write('%s\n' % each)     # 写入其他义项的URL信息
        temp.close()
