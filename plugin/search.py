#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import re
import urllib
import sys
import vim
from bs4 import BeautifulSoup
from cache import creat_cache, scan_cache, save_data, creat_temp

# 获取网页源码
def get_html(url):      #(str)
    try:
        page = urllib.urlopen(url)
    except:
        raise Exception("请检查网络连接.. _(:3 」∠)_")
    else:
        html = page.read()
        return html

# 截取简介
def get_brief(html):
    brief = r'"description" content="(.+?)"'
    brief_re = re.compile(brief)
    brief_sch = re.search(brief_re, html)  #提取<name="description">内的文字
    if brief_sch:
        return brief_sch.group(1)

# 截取所有描述
def get_all(html):
    Soup = BeautifulSoup(html, 'lxml')     #lxml解析网页
    descs = Soup.select('.para')           #提取<class="para">内的文字
    other = r'subview\/\d+\/\d+\.htm\#viewPageContent'
    other_re = re.compile(other)
    other_sch = re.findall(other_re, html) #提取其他义项的部分URL
    creat_temp(other_sch)                  #创建临时文件存放提取信息
    if descs:
        return descs

# 获取其他义项
def get_others():
    item = int(vim.eval('g:item'))         #获取其他义项的索引
    tempfile = open('.BaiduTemp.txt', 'r') #读取临时文件
    lines = tempfile.readlines()
    if item >= len(lines):
        vim.command('let g:item = 0')      #重置索引
        raise Exception("没有更多义项了呦..")
    else:
        for curline in lines[item : item+1]:    #找到第item行
            temp = curline                      #提取部分URL
        html = get_html("http://baike.baidu.com/%s" % temp)
        Soup = BeautifulSoup(html, 'lxml')
        descs = Soup.select('.para')            #再次提取描述文字
        selection = Soup.select('.selected')[0] #找到该义项的标题
        descs.insert(0, selection)              #将标题插入结果
        return descs


# Vim中显示结果
def show_result(result, show_type):                  #((str|list), str)
    if not result:
        raise Exception("百度百科并没有该词条..")
    else:
        if show_type == 'cmdline':                   #命令行中输出结果
            print(result)
        elif show_type == 'window':                  #新建窗口输出结果
            cwinnr = int(vim.eval('s:OpenWindow()')) #获取新窗口编号
            vim.command(str(cwinnr) + ' wincmd w')   #跳转到该窗口
            cbuf = vim.current.buffer                #获取当前窗口Buffer
            vim.command('setl modifiable')           #使窗口内数据可修改
            vim.command('%d _')
            for para in result:                      #执行迭代并输出结果
                cbuf.append(u'\t%s' % para.get_text().replace('\n', ''))
                cbuf.append("\n")
            cbuf.append("\t\t\t\t\t\t\t\t\t\t\t  [M]ore 更多其他义项.. [Q]uit 退出")
            vim.command('0d _')
            vim.command('setl nomodifiable')         #锁定窗口内数据

# 主函数
def main():
    try:
        keyword = vim.eval('iconv(a:vtext, &encoding, "utf-8")')
        show_type = vim.eval('a:show_type')  #获取Vim传入的数据
        print('关键词: %s' % keyword)

        locate = creat_cache()               #创建缓存文件并返回完整路径
        cache = scan_cache(keyword, locate)  #扫描缓存内是否有该关键词的数据
        if cache and show_type == 'cmdline':
            show_result(cache, 'cmdline')    #直接输出
        else:
            html = get_html("http://baike.baidu.com/item/%s" % keyword)

            if show_type == 'cmdline':
                brief = get_brief(html)
                show_result(brief, 'cmdline')
                save_data(keyword, brief, locate) #将结果保存到缓存
            elif show_type == 'window':
                show_result(get_all(html), 'window')
            elif show_type == 'other':
                show_result(get_others(), 'window')

    except Exception as err:      #捕获常规异常
        print('Error: %s' % err)
    except:
        print('Unknown Error: 未知错误')

__all__ = ['main']
