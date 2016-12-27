if !exists('g:debug_baidu') && exists('g:loaded_baidu')
    finish
endif
let g:loaded_baidu= 1

let s:save_cpo = &cpo
set cpo&vim

if !hasmapto('<Plug>BaiduSearch')
    nmap <silent> <Leader>b <Plug>BaiduSearch
endif

" if !hasmapto('<Plug>BaiduVSearch')
"     vmap <silent> <Leader>b <Plug>BaiduVSearch
" endif

nmap <silent> <Plug>BaiduSearch  :call GetSelctn(expand("<cword>"))<CR>
" vmap <silent> <Plug>BaiduVSearch :<C-u>call baidu#VSearch()<CR>

if !exists(':baidu')
    command! -nargs=1 baidu call GetSelctn(<q-args>)
endif

let &cpo = s:save_cpo
unlet s:save_cpo
