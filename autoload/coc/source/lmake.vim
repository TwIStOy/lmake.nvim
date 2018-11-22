function! coc#source#lmake#init() abort
  return {
    \ 'shortcut': 'lmake',
    \ 'priority': 1,
    \ 'filetypes': ['bzl'],
    \ 'firstMatch': ':'
    \ }
endfunction

function! coc#source#lmake#complete(opt, cb) abort
  call a:cb(_lbuild_get_hints())
endfunction