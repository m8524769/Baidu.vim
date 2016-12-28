# *Baidu.vim*

###简单实现Vim划词搜索功能
* 支持快速搜索光标下词条以及可视模式下的选词搜索
* 支持Baidu及BaiduW命令进行搜索
* 要求Vim版本支持Python或Python3+
* 使用时需要联网
* 仅限百度百科已有的词条

###安装
```VIML
    Plugin 'm8524769/baidu.vim'
    :PluginInstall
```

###默认快捷键映射
```VIML
    " 命令行显示搜索结果
    nmap <silent> <Leader>b <Plug>BaiduSearch
    vmap <silent> <Leader>b <Plug>BaiduVSearch
    " 新窗口显示搜索结果
    nmap <silent> <Leader>w <Plug>Win_BaiduSearch
    vmap <silent> <Leader>w <Plug>Win_BaiduVSearch
    " <q> 或 <CR> 退出Baidu窗口
```
- 你也可以按自己的喜好自定义快捷键

###命令行搜索
- 例:
```VIML
    :Baidu 江泽民
    :BaiduW 三个代表重要思想
```
##*Happy Viming !!*