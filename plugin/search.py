#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import re
import urllib
import sys
import os
import vim
from bs4 import BeautifulSoup

# 获取网页源代码
def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

# 截取简介
def get_brief(html):
    brief = r'"description" content="(.+?)"'
    brief_re = re.compile(brief)
    brief_sch = re.search(brief_re, html)
    return brief_sch

# 截取词条描述
def get_all(html):
    Soup = BeautifulSoup(html, 'lxml')
    descs = Soup.select('.para')
    return descs

# Vim中显示结果
def show_result(result, show_type):
    if show_type == 'cmdline':
        try:
            print(result.group(1))
        except:
            print("百度百科并没有这个词条..")
    elif show_type == 'window':
        cwinnr = int(vim.eval('s:OpenWindow()'))    #获取__dictSearch__窗口编号
        vim.command(str(cwinnr) + ' wincmd w')      #跳到__dictSearch__窗口
        cbuf = vim.current.buffer                   #获取当前__dictSearch__的buffer
        vim.command('setl modifiable')
        vim.command('%d _')
        try:
            para_num = 1
            while result[para_num] != result[-1]:
                cbuf.append(u'%s' % result[para_num].get_text().replace('\n', ''))
                cbuf.append("\n")
                para_num += 1
            cbuf.append("[Q]uit 退出")
            vim.command('0d _')
            vim.command('setl nomodifiable')
        except:
            vim.command(':close')
            print("百度百科并没有这个词条..")

# 主函数
def main():
    keyword = vim.eval('iconv(a:vtext, &encoding, "utf-8")')
    html = get_html("http://baike.baidu.com/item/%s" % keyword)

    show_type = vim.eval('a:show_type')
    if show_type == 'cmdline':
        show_result(get_brief(html), 'cmdline')
    elif show_type == 'window':
        show_result(get_all(html), 'window')

__all__ = ['main']
