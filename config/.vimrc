set background=dark
"colorscheme monokai
colorscheme desert  " 设置主题方案
set number          " 显示行号
"set cursorline      " 突出显示当前行
set backspace=2     " 设置退格键可用
set nocompatible    " 去掉vi一致性模式

syntax on              " 打开语法高亮
syntax enable          " 更优化的syntax on

set tabstop=4       " 设置tab键的宽度
set softtabstop=4   " 设置删除缩进的宽度
set shiftwidth=4    " 每级缩进的长度
set noexpandtab     " 是否展开tab为空格
set cindent         " 类似C语言程序的缩进
set autoindent      " 自动对齐
set smartindent     " 智能对齐方式,基于autoindent
set ai!             " 设置自动缩进

set showmatch       " 设置匹配模式，类似当输入一个左括号时会匹配相应的那个右括号
set shiftwidth=4    " 换行时行间交错使用4个空格

filetype on                   "自动文件类型检测
filetype plugin indent on     "开启文件类型的插件
filetype indent on            "为文件类型开启不同缩进格式

set magic           "设置魔术
set showmatch       "高亮显示匹配的括号
set ruler           "打开状态栏标尺
set hlsearch        "高亮显示搜索结果
set ignorecase      "忽略大小写
set title
set completeopt=longest,menu
set history=10000
set laststatus=2

"
" ===============================================================================
" Ctags
" ===============================================================================
set tags=tags;
set autochdir

"
" ===============================================================================
" TagList :Tlist
" ===============================================================================

let Tlist_Ctags_Cmd = 'ctags'
let Tlist_Use_Right_Window = 1         "在右侧窗口中显示taglist窗口
let Tlist_Show_One_File = 1            "不同时显示多个文件的tag，只显示当前文件的
let Tlist_Exit_OnlyWindow = 1          "如果taglist窗口是最后一个窗口，则退出vim
"let Tlist_Auto_Open = 1                 "设置taglist在vim启动的时候自动打开

" ===============================================================================
" WinManager :WMToggle
" ===============================================================================

"let g:winManagerWindowLayout='FileExplorer|TagList'
let g:winManagerWindowLayout='FileExplorer'
nmap wm :WMToggle<CR>:TlistToggle<CR>

" ===============================================================================
" cscope
" ===============================================================================

" set quickfix
set cscopequickfix=s-,c-,d-,i-,t-,e-

" use both cscope and ctag for 'ctrl-]', ':ta', and 'vim -t'
set cscopetag

" check cscope for definition of a symbol before checking ctags: set to 1
" if you want the reverse search order.
set csto=0

" else add the database pointed to by environment variable
if $CSCOPE_DB != ""
	cs add $CSCOPE_DB
" add any cscope database in current directory
elseif filereadable("cscope.out")
	cs add cscope.out
endif

" show msg when any other cscope db added
set cscopeverbose


" ===============================================================================
" MiniBufExp
" ===============================================================================

let g:miniBufExplMapCTabSwitchBufs=1
let g:miniBufExplMapWindowNavVim=1
let g:miniBufExplMapWindowNavArrows=1
let g:miniBufExplModSelTarget=1
let g:miniBufExplorerMoreThanOne=2
let g:miniBufExplCycleArround=1
"let g:minibufExplMaxSize=2
"let g:minibufExplMinSize=1

" ===============================================================================
" SuperTab :SuperTabHelp
" ===============================================================================

let g:SuperTabRetainCompletionType=2
let g:SuperTabDefaultCompletionType="<C-X><C-O>"

" ===============================================================================
" 热键映射
" ===============================================================================
"cscope插件热键
nmap cs :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap cg :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap cc :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap cd :cs find d <C-R>=expand("<cword>")<CR><CR>
nmap ct :cs find t <C-R>=expand("<cword>")<CR><CR>
nmap ce :cs find e <C-R>=expand("<cword>")<CR><CR>
nmap cf :cs find f <C-R>=expand("<cfile>")<CR><CR>
nmap ci :cs find i ^<C-R>=expand("<cfile>")<CR><CR>


"F4 粘贴模式，防止代码粘贴缩进错乱
set pastetoggle=<F4>

"F5执行编译MAKE
map <F5> :w<CR>:make<CR>
map <C-F5> :make clean<CR>

"F6打开quickfix
"nmap <F6> :cw<CR>
nmap <F6> :botright copen<CR>

"Ctrl+F6关闭quickfix
nmap <C-F6> :ccl<CR>

"F7向后选择quickfix
nmap <F7> :cn<CR>

"F8向前选择quickfix
nmap <F8> :cp<CR>

"F9头文件与源文件切换
map <F9> :A<CR>

"F10打开/关闭taglist
nmap <F10> :TlistToggle<CR>

"F12生成/更新tags文件
function! UpdateTagsFile()
	silent !ctags -R
endfunction
nmap <F12> :call UpdateTagsFile()<CR>

"Ctrl+F12删除tags文件
function! DeleteTagsFile()
	silent !rm tags
endfunction
nmap <C-F12> :call DeleteTagsFile()<CR>

"status line
set statusline=[%F]%y%r%m%*%=[Line:%l/%L,Column:%c][%p%%]
