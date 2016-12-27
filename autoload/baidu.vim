"获取词条
function! GetSelctn(vtext) abort
    execute python . 'baidu.search()'
endfunction

"python/python3 import init
exec python . 'import vim'
exec python . 'import sys'
exec python . 'import baidu'
