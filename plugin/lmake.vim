if exists('g:loaded_lmake')
  finish
endif

let g:loaded_lmake = 1

autocmd FileType bzl call lmake#keybinding()