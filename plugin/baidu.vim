"import初始化
execute 'python import vim'
execute 'python import sys'
execute 'python cwd = vim.eval("expand(\"<sfile>:p:h\")")'
execute 'python sys.path.insert(0,cwd)'
execute 'python import search'

"检测是否支持Python
if !has('python') && !has('python3')
    finish
endif

if !exists('g:debug_baidu') && exists('g:loaded_baidu')
    finish
endif
let g:loaded_baidu= 1

let s:save_cpo = &cpo
set cpo&vim

"默认映射
if !hasmapto('<Plug>BaiduSearch')
    nmap <silent> <Leader>b <Plug>BaiduSearch
endif
if !hasmapto('<Plug>BaiduVSearch')
    vmap <silent> <Leader>b <Plug>BaiduVSearch
endif
if !hasmapto('<Plug>Win_BaiduSearch')
    nmap <silent> <Leader>w <Plug>Win_BaiduSearch
endif
if !hasmapto('<Plug>Win_BaiduVSearch')
    vmap <silent> <Leader>w <Plug>Win_BaiduVSearch
endif

nmap <silent> <Plug>BaiduSearch      :call GetSelctn(expand("<cword>"), "cmdline")<CR>
vmap <silent> <Plug>BaiduVSearch     :<C-u>call GetVSelctn("cmdline")<CR>
nmap <silent> <Plug>Win_BaiduSearch  :call GetSelctn(expand("<cword>"), "window")<CR>
vmap <silent> <Plug>Win_BaiduVSearch :<C-u>call GetVSelctn("window")<CR>

"调用Python搜索
function! GetSelctn(vtext, show_type) abort
    execute 'python search.main()'
endfunction

function! GetVSelctn(show_type) abort
    let vtext = s:VisualSelctn()
    call GetSelctn(vtext, a:show_type)
endfunction

"可视模式选词
function! s:VisualSelctn() abort
    let regTmp = @a
    execute "normal gv\"ay"
    let vtext = @a
    let @a = regTmp
    return vtext
endfunction

"设置Baidu命令
if !exists(':Baidu')
    command! -nargs=1 Baidu call GetSelctn(<q-args>, "cmdline")
endif

if !exists(':BaiduW')
    command! -nargs=1 BaiduW call GetSelctn(<q-args>, "window")
endif

"设置窗口属性
function! s:WinConfig() abort
    setl filetype=BaiduSearch
    setl buftype=nofile
    setl bufhidden=hide
    setl noswapfile
    setl noreadonly
    setl nomodifiable
    setl nobuflisted
    setl nolist
    setl nonumber
    setl wrap
    setl winfixwidth
    setl winfixheight
    setl textwidth=0
    setl nospell
    setl nofoldenable
    setl conceallevel=3
    setl concealcursor=icvn
    nnoremap <silent><buffer> q :close<CR>
    nnoremap <silent><buffer> <CR> :close<CR>
endfunction

"打开新窗口
function! s:OpenWindow() abort
    let cwin = bufwinnr('__BaiduSearch__')
    if cwin == -1
        silent keepalt bo split __BaiduSearch__
        call s:WinConfig()
        return winnr()
    else
        return cwin
    endif
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
