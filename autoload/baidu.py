#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import re
import urllib
import sys
import vim
import json
from bs4 import BeautifulSoup

# 获取网页源代码
def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

# 截取词条描述部分
def get_desc(html):
    Soup = BeautifulSoup(html, 'lxml')
    descs = Soup.select('.para')
    if descs:
        return descs
    else:
        print("百度百科并没有这个词条..")
        exit()

# Vim中显示结果
def show_result(descs):
    print(descs[0].get_text())
    para_num = 1
    while descs[para_num]:
        more = raw_input("[M]ore 更多.. [Q]uit 退出:")
        print('---------------------------')
        if more == 'q':
            exit()
        elif more == 'm':
            print(descs[para_num].get_text())
            para_num += 1
        else:
            print('Excuse me?')

# 主函数
def search():
    keyword = vim.eval('iconv(a:vtext, &encoding, "utf-8")')
    html = get_html("http://baike.baidu.com/item/%s" % keyword)
    descs = get_desc(html)
    show_result(descs)




__all__ = ['search']
