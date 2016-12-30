#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import re
import urllib
import sys
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

# 获取其他义项
def get_others(html):
    other = r'class="selected".+?(subview\/\d+\/\d+\.htm\#viewPageContent)'
    #  other_re = re.compile(other)
    #  other_sch = re.search(other_re, html)
    other_sch = re.search(other, html, re.S)
    if not other_sch:
        raise Exception("没有其他义项了呦..")
    else:
        #  print(other_sch.group(1))
        html = get_html("http://baike.baidu.com/%s" % other_sch.group(1))
        Soup = BeautifulSoup(html, 'lxml')
        descs = Soup.select('.para')
        return descs


# Vim中显示结果
def show_result(result, show_type):
    if not result:
        raise Exception("百度百科貌似并没有这个词条..")
    else:
        if show_type == 'cmdline':
            print(result.group(1))
        elif show_type == 'window':
            cwinnr = int(vim.eval('s:OpenWindow()'))
            vim.command(str(cwinnr) + ' wincmd w')
            cbuf = vim.current.buffer
            vim.command('setl modifiable')
            vim.command('%d _')
            for para in result:
                cbuf.append(u'\t%s' % para.get_text().replace('\n', ''))
                cbuf.append("\n")
            cbuf.append("[M]ore 更多其他义项.. [Q]uit 退出")
            vim.command('0d _')
            vim.command('setl nomodifiable')

# 主函数
def main():
    try:
        keyword = vim.eval('iconv(a:vtext, &encoding, "utf-8")')
        html = get_html("http://baike.baidu.com/item/%s" % keyword)
        print('关键词: %s' % keyword)

        show_type = vim.eval('a:show_type')
        if show_type == 'cmdline':
            show_result(get_brief(html), 'cmdline')
        elif show_type == 'window':
            show_result(get_all(html), 'window')
        elif show_type == 'other':
            show_result(get_others(html), 'window')

    except IOError:
        print('IO Error: 请检查网络连接..')
    except AttributeError:
        print('Attribute Error: 尝试访问未知的对象属性')
    except IndexError:
        print('Index Error: 索引超出序列范围')
    except ValueError:
        print('Value Error: 参数类型不正确')
    except SyntaxError:
        print('Syntax Error: 语法错误')
    except NameError:
        print('Name Error: 尝试访问一个没有声明的变量')
    except Exception as err:
        print('Error: %s' % err)
    except:
        print('Unknown Error: 未知错误')

__all__ = ['main']
