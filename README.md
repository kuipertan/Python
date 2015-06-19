# Python
Python code

Prepare vim settings before coding

set tabstop=4 设定tab宽度为4个字符
set shiftwidth=4 设定自动缩进为4个字符
set expandtab 用space替代tab的输入
set noexpandtab 不用space替代tab的输入

如果文件已经是tab了，下面转成空格：
:set expandtab
:%ret! 4
