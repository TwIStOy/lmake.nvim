function! lmake#denite() abort
  if exists('g:loaded_denite')
    Denite lmake-all-targets
  endif
endfunction

function! lmake#keybinding() abort
  if exists('g:lmake_disable_quick_search') && g:lmake_disable_quick_search
    return
  endif
  inoremap <F10> <C-O>:call lmake#denite()<CR>
endfunction