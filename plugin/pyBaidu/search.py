# _*_ coding: utf-8 _*_
# !/usr/bin/env python

import re
import vim
import socket
from bs4 import BeautifulSoup
from cache import *
if vim.eval('g:py_version') == '2':
    import urllib
else:
    from urllib import request as urllib


#  获取网页源码
def get_html(url):      # (str)
    try:
        socket.setdefaulttimeout(4)   # 全局默认超时时间为4秒
        page = urllib.urlopen(url)
    except:
        raise Exception('请检查网络连接.. _(:3」∠)_')
    else:
        html = page.read()
        return html


#  截取简介
def get_brief(html):
    Soup = BeautifulSoup(html, 'lxml')
    brief = Soup.select('meta[name="description"]')
    if brief:
        return brief[0].get('content')


#  截取所有描述
def get_all(html):
    Soup = BeautifulSoup(html, 'lxml')     # lxml解析网页
    descs = Soup.select('.para')            # 提取<class="para">内的文字
    urls = Soup.select('.polysemantList-wrapper > li > a')
    urls = [each.get('href') for each in urls]
    creat_temp(urls)                        # 创建临时文件存放提取信息
    if descs:
        return descs


#  获取其他义项
def get_others():
    try:
        tempfile = open('.BaiduTemp.txt', 'r')  # 读取临时文件
        lines = tempfile.readlines()
    except IOError:
        raise Exception('没有其他义项..')
    else:
        item = int(vim.eval('g:item'))         # 获取其他义项的索引
        if item >= len(lines):
            vim.command('let g:item = 0')      # 重置索引
            raise Exception('没有更多义项了呦..')
        else:
            for curline in lines[item:item+1]:    # 找到第item行
                info = curline                      # 提取部分URL
            html = get_html('http://baike.baidu.com' + info)
            Soup = BeautifulSoup(html, 'lxml')
            descs = Soup.select('.para')            # 再次提取描述文字
            title = Soup.select('.selected')[0]  # 找到该义项的标题
            descs.insert(0, title)               # 将标题插入结果
            return descs


#  获取连词结果
def get_multiple(words):
    word_list = re.split(r'[_,;\s]*\s*', words)  # 分离关键词
    descs = []
    locate = creat_cache()                     # 创建缓存文件并返回完整路径
    for each in word_list:                     # 分别搜索各词
        if each == '':
            continue
        descs.append('</%s >---------------------------' % each)
        cache = scan_cache(each, locate)       # 扫描缓存内是否有该词的数据
        if cache:
            descs.append(cache)
        else:
            html = get_html('http://baike.baidu.com/item/' + each)
            brief = get_brief(html)
            if brief:
                descs.append(brief)
                save_data(each, brief, locate)  # 将结果保存到缓存
            else:
                descs.append('百度百科未收录该词条.. (/ω＼)')
    return descs


#  Vim中显示结果
def show_result(result, show_type):                  # ((str|list), str)
    if not result:
        raise Exception('百度百科未收录该词条.. (/ω＼)')
    else:
        if show_type == 'cmdline':                   # 命令行中输出结果
            print(result)
        else:                                         # 新建窗口输出结果
            cwinnr = int(vim.eval('s:OpenWindow()'))  # 获取新窗口编号
            vim.command(str(cwinnr) + ' wincmd w')    # 跳转到该窗口
            cbuf = vim.current.buffer                 # 获取当前窗口Buffer
            vim.command('setl modifiable')            # 使窗口内数据可修改
            vim.command('%d _')
            if show_type == 'window':
                for para in result:
                    cbuf.append(u'\t%s' % para.get_text().replace('\n', ''))
                    cbuf.append('\n')
                cbuf.append('\t'*10 + '  [M]ore 更多其他义项.. [Q]uit 退出')
            elif show_type == 'multiple':
                for each in result:
                    cbuf.append('%s' % each)
                cbuf.append('\t'*16 + '[Q]uit 退出')
            vim.command('0d _')
            vim.command('setl nomodifiable')         # 锁定窗口内数据


#  主函数
def main():
    try:
        keyword = vim.eval('iconv(a:vtext, &encoding, "utf-8")')
        show_type = vim.eval('a:show_type')             # 获取Vim传入的数据
        print('关键词: %s' % keyword)

        for each in keyword:
            if each in ['_', ',', ';', ' ']:            # 判断关键词是否被分隔
                show_type = 'multiple'                  # 更改输出形式为multiple(窗口显示)
                show_result(get_multiple(keyword), 'multiple')
                break

        if show_type == 'cmdline':
            locate = creat_cache()               # 创建缓存文件并返回完整路径
            cache = scan_cache(keyword, locate)  # 扫描缓存内是否有该关键词的数据
            if cache:
                show_result(cache, 'cmdline')    # 直接输出
            else:
                html = get_html('http://baike.baidu.com/item/' + keyword)
                brief = get_brief(html)
                show_result(brief, 'cmdline')
                save_data(keyword, brief, locate)  # 将结果保存到缓存

        elif show_type != 'multiple':
            html = get_html('http://baike.baidu.com/item/' + keyword)
            if show_type == 'window':
                show_result(get_all(html), 'window')
            if show_type == 'other':
                show_result(get_others(), 'window')

    except socket.timeout:
        print('请求超时.. _(:3」∠)_')
    except Exception as err:              # 捕获常规异常
        print('Error: %s' % err)


__all__ = ['main']
