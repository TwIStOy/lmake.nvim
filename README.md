# lmake.nvim

Autocomplete rules in BUILD files for lmake. (Only for neovim)

# Requirements
- [neovim](https://github.com/neovim/neovim)
- [coc.nvim](https://github.com/neoclide/coc.nvim) / [deoplete](https://github.com/Shougo/denite.nvim)
- Optional: [denite.nvim](https://github.com/Shougo/denite.nvim)

# Install
For vim-plug
```vim
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'TwIStOy/lmake.nvim', { 'do': ':UpdateRemotePlugins' }
```

# Configuration
If no `deoplete` or `coc.nvim` installed.
```
inoremap <F10> <C-O>complete(col('.'), _lbuild_get_hints())<CR>
```
Press <F10> to trigger lmake's complete.
