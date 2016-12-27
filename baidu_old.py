#_*_ coding: utf-8 _*_
#!/usr/bin/env python

# import py_compile
# py_compile.compile('tpy.py')

import re
import urllib

# 获取网页源代码
def get_html(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

# 截取词条描述部分
def get_desc(html):
    description = r'label-module="para"\>(.+)'
    desc_re = re.compile(description)
    desc_sch = re.findall(desc_re, html)
    if desc_sch:
        return desc_sch
    else:
        print("百度百科并没有这个词条..")
        exit()

# 提取描述
def pick_desc(desc):
    newline = r'\<\/div\>'
    newline_re = re.compile(newline)
    desc = re.sub(newline_re, "\n", desc)
    rm = r'\<.+?\>|&nbsp;'
    rm_re = re.compile(rm)
    desc = re.sub(rm_re, "", desc)
    return desc

print("请输入关键词:")
keyword = raw_input()
html = get_html("http://baike.baidu.com/item/%s" % keyword)

# 显示基本描述
dty_desc = get_desc(html)
print(pick_desc(dty_desc[0]))

para_num = 1
while dty_desc[para_num]:
    more = raw_input("[M]ore 更多.. [Q]uit 退出:")
    if more == 'q':
        exit()
    elif more == 'm':
        print(pick_desc(dty_desc[para_num]))
        para_num += 1
    else:
        print('Excuse me?')

