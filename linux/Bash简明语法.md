# Bash 简明语法

## 变量

**变量类型**：所有的变量都只能存储 **String** 类型

**变量赋值**：使用等号赋值，且等号两边**不允许有空格**，赋值例子：

```shell
$ name=Tom # 简单赋值
$ msg="Hello world" # Bash 是 Shell 的一种，对空格敏感，如果变量值包含空格，需要用 "" 或 '' 包裹起来
$ now=`date` # 将 date 命令的执行结果存入变量 now，该功能由 `` 实现
$ name2=$name # 将一个变量的值赋给另一个变量
$ read name # 读取终端输入，并将输入值存入 name 变量
```

**变量引用**：使用 **"$"+变量名** 来引用一个变量。例子：

```shell
$ name=Tom
$ echo $name # 打印变量 name 的内容
$ echo Hi$name # 可以将变量拼到字符串最后，Bash 会自动用值替换
$ echo ${name}AreYouOK # 变量不在文本末尾，需要用 {} 将其框出，不然 Bash 无法分辨其边界
$ echo "$name, r u OK?" # 如果文本中包含空格，需要用引号引起来。双引号间的变量会自动替换为值，单引号不行
```

**数值运算**：使用 **$(())** 可以进行简单的数值运算，比如 +、-、*、/、() 等。例子：

```shell
$ echo $((1+2)) # 输出 3
$ result=$((1+2)) # 将结果赋给变量
```



## 选择结构



## 循环结构



## 函数



## Bash脚本

一个简单的示例（demo.sh）：

```shell
#!/bin/bash
# 打印文字
echo "Hello, world!"
```

第一行声明执行该脚本执行的Shell，如果该脚本有执行权限，可以直接执行：

```shell
$ ./demo.sh
```

否则，可以使用指定Shell执行：

```shell
$ bash demo.sh
```

使用 **#** 进行代码注释<br>

bash 脚本是**按行执行**<br>

### 脚本返回码

当一个 bash 脚本执行结束后，会返回执行成功的默认值 **0**<br>

脚本中可以使用 **exit 1** 指定其他返回码，执行到 exit 行会自动退出并返回指定的返回码<br>

可以使用 **$?** 捕获上个脚本的返回码：

```shell
$ ./demo.sh
$ echo $?
```

在 Linux 中，一行可以执行多个命令，并且可以利用返回码控制流程：

```shell
$ cd targetDir && echo "success" # cd 命令执行成功（返回0）则打印 success
$ cd targetDir || echo "failed" # cd 命令执行失败（返回非0值）则打印 failed
$ cd targetDir || exit 1 # 一般用在脚本中间，如果命令执行失败则直接退出并返回指定退出码
```

### 调用参数

使用 **$+数字** 进行变量的引用，**$0** 是脚本自身，脚本 param.sh 内容为：

```shell
#!/bin/bash
echo $0
echo $1
echo $2
```

使用 "./param.sh hello world" 输出内容为：

```
./param.sh
hello
world
```

使用 "bash param.sh hello world" 输入内容为：

```
param.sh
hello
world
```

### 跨脚本调用

* 直接使用 Shell 进行调用，会新创建一个子进程，然后执行脚本

```shell
#!/bin/bash
sh another.sh
```

* 使用 source 调用，在同一个进程中执行脚本，可以理解为直接将另一个脚本的内容（包括函数定义）复制过来执行：

```shell
#!/bin/bash
source another.sh
```



## 参考文档

> Vamei，周昕梓著 《树莓派开始，玩转Linux》