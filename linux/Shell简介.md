# Shell 简介

## Shell 是什么
Shell，英文中的意思为壳，比如贝壳类生物的外壳。<br>
Linux 中，Shell 是终端用户和操作系统之间的接口。用户通过 Shell 这个“壳”来和操作系统进行交互。<br>
Shell 是 UNIX 命令解释器，一种文本交互方式（另一种是图形交互方式GUI）。作用是分析文本输入，然后把文本转换成相应的计算机操作。<br>
附带一提，一般我们都通过 ssh 命令连接到一台服务器，ssh 是 “Secure Shell” 的缩写，一种网络传输协议。通过一系列操作及加密连接到一个终端后，就会启动一个 Shell 进程并展示命令提示符 "$" （管理员为 "#"），表示等待用户输入。<br>
Shell 程序接收单击 “Enter” 键之前的文本内容，然后对文本进行分析。具体过程为：

1. 根据空格将文本内容划分为多个部分，第一部分为命令名，其余部分为选项和参数。
2. 分析第二部分的文本（主要根据特殊字符）。
3. 执行该命令对应的操作。

比如输入：
```shell
$ ls -l
```
Shell 首先根据空格（因此 Shell 对空格敏感）得到 "ls" 和 "-l" 两部分内容。命令部分为 "ls"，继续分析 "-l"，发现开头是 "-"，从而知道它是一个选项。文本分析结束后 Shell 创建一个子进程执行操作，同时 Shell 进程阻塞等待执行完成。执行结束后，Shell 将结果输出到终端（Shell 的默认输出），然后继续展示命令提示符等待下次输入。

## Shell 命令的分类
* Shell 内建函数 (built-in function)
* 可执行文件 (executable file)
* 别名 (alias)

Shell 内建函数就是直接保存在 Shell 内部的函数，与此相对，可执行文件就是保存在 Shell 外部的脚本。前者可以直接执行，后者 Shell 必须在系统中找到对应的可执行文件，然后才能正确执行。可以输入绝对路径告诉 Shell 要执行命令的位置，比如：
```shell
$ /bin/date
```
如果不指定路径而只给出命令名，Shell 会搜索一些默认路径，然后执行与命令名匹配的第一个可执行文件。可以通过 which 确定可执行文件的具体路径：
```shell
$ which date
```
别名就是用户为了方便记忆或者方便操作，给特定的命令组合配置的别称或简称，可以使用 alias 命令来指定（git 中也有类似操作）：
```shell
$ alias la="ls -a"
```
之后输入 la 命令就等同于输入 ”ls -a“。可以键入 "alias" 不带参数就可以查询已有的别名。<br>
可以通过 type 命令查看命令类型，如果是内建函数，会显示"xx is a shell builtin"，如果是可执行文件，就会显示文件路径，如果是别名，就显示"xx is aliased to xxx"。例如：
```shell
$ type cd
$ type date
$ type ll
```
## Shell 的分类

Shell 其实是统称，所有的文本解释器都可以被称为Shell。常见的 Shell 有：sh，bash，dash 等。
* sh 全称是 Bourne Shell（以作者命名），一种早期 Shell。现在用的不多，但是为兼容历史程序，一般 Linux 都会内置。
* bash 全称是 Bourne Again Shell，是 sh 的增强版，现在普遍作为 Linux 的默认 Shell（GNU/Linux 操作系统中的 /bin/sh 就是 bash 的软链接）。比 sh 提供了更丰富的功能，支持Tab命令补全，支持“↑”，“↓”翻阅历史命令记录，支持 help 解释自身命令。
* dash 鉴于 bash 过于复杂，有人把 ash 从 NetBSD 移植到 Linux 并更名为 dash (Debian Almquist Shell)，并建议将 /bin/sh 指向它，以获得更快的脚本执行速度。Dash Shell 比 Bash Shell 小的多，符合POSIX标准。Debian 系的 Linux 一般都用 dash 作为默认 Shell，如 Ubuntu 等。

可以通过以下命令查看当前 Shell 类型：
```shell
$ echo $SHELL
```
一般来说，建议将 bash 作为默认 Shell。



## 参考文档：
> Vamei，周昕梓著 《树莓派开始，玩转Linux》
>
> Andrew S.Tanenbaum，Herbert Bos著 陈向群，马洪兵等译 《现代操作系统（原书第四版）》
>
>CSDN 博客 [https://blog.csdn.net/monmama/article/details/53390610](https://blog.csdn.net/monmama/article/details/53390610)