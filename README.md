# *Baidu.vim*

[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

### 简单实现Vim划词搜索功能
* 支持快速搜索光标下词条以及可视模式下的选词搜索
* 支持Baidu及BaiduAll命令进行搜索
* 要求Vim版本支持Python特性
* 使用时需要联网
* 仅限百度百科已有的词条

![Example](Example.gif)

### 安装
- 通过Vundle.vim
```VIML
    Plugin 'm8524769/baidu.vim'
    :PluginInstall
```
- 通过vim-plug
```VIML
    Plug 'm8524769/baidu.vim'
    :PlugInstall
```

### 默认快捷键映射
```VIML
    " 命令行显示搜索结果
    nmap <silent> <Leader>b <Plug>BaiduSearch
    vmap <silent> <Leader>b <Plug>BaiduVSearch
    " 新窗口显示搜索结果
    nmap <silent> <Leader>w <Plug>Win_BaiduSearch
    vmap <silent> <Leader>w <Plug>Win_BaiduVSearch
    " `q` 或 `Enter` 退出BaiduSearch窗口
    " `m` 显示其他义项
```
- 你也可以按自己的喜好自定义快捷键

### 默认缓存路径
```VIML
    let g:baidu_cache_path = '$VIM/vimfiles/bundle/Baidu.vim/cache'
```

#### Update_1 Date: 2016/12/30 周五 13:35:27
- 优化异常处理机制
- 更改`:BaiduW`命令为`:BaiduAll`
- 集成Airline插件，在Statusline显示关键词
- 新增`m`可显示其他义项（目前只能显示第二个义项）

#### Update_2 Date: 2017/1/2 周一 8:54:12
- 多义词条现可正常显示所有义项
- 优化显示其他义项的性能及速度
- 新增缓存机制
  * 保存历史命令行搜索结果以提高性能
  * 断网仍可查看历史搜索结果
- 优化异常处理
- 用户可自定义缓存路径
  * 只能在Vim根目录下的某个文件夹

#### Update_3 Date: 2017/1/28 周六 0:36:20
- 可识别以下划线分隔的多个英文单词
    * 例如 'A_B_C' 的关键词会默认以窗口模式输出各个结果
    * 'A', 'B', 'C'均可写入缓存以便下次读取

#### Update_4 Date: 2017/3/1 周三 21:58:48
- 搜索关键词支持以逗号，分号或空格隔开
  * 例如 'A_B, C; D E'
- 新增多词窗口内关键词高亮
- 修复已知Bug

# *Happy Viming !!*

#### 参考项目
- https://github.com/iamcco/dict.vim
