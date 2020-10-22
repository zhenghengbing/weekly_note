这个是文档标题
==============
这个是次级标题
--------------
等号和减号至少1个，就可以实现对应效果，不过多了看着更明白

使用vscode进行编辑预览导出  
用到的插件：Markdown All in One; Markdown Math; Markdown PDF; Markdown Priview Github;

# 特大标题
## 大标题
### 中号的
#### 小号的
##### 更小号的
###### 依次类推 
井号后的空格是必要的，为了好看，在后边加上同等数量的等号也是不错的嘛，就像这样
# 另一个特大号 #

*斜体字*

**粗体字**

***又斜又粗体字***

```python
def say_hello(name):
    print("hello, ", name)
```
```java
public static void sayHello(String name) {
    System.out.println("hello, " + name);
}
```

这个是文字链接 [百度](https://baidu.com)

这个是网址链接 <https://baidu.com>

这个是高级版文字链接 [百度][1]

这个是高级版网址链接 [Baidu][baidu]

下边这些网址定义放到文档末尾比较合适

[1]: https://baidu.com
[baidu]: https://baidu.com

尝试下引用

首先是普通引用
> 阿巴阿巴
> 还真是那么回事
> 咋不换行啊

> 得另起一行？
>
> 还真是
>
> 看来中间也得有大于号，才能连上啊
接下来

先换个行，接下来是嵌套引用
> 老大
> > 老大大
> > > 老大大大
> > > > 老末

下面这些是普通无序列表
- 第一行
- 第二行

另一个版本的普通无序列表
* 第一行
* 第二行

再一个版本的普通无序列表
* 第一行
* 第二行

这么看来， (-|+|*)是一码事啊

接下来是有序列表
1. 你好啊
2. 吃了吗您呐
6. 还真能纠错啊，可以可以

整个带嵌套的
1. 我是头
   - 我是2头
     1. 我是3头
     2. 呦，我变了，不是数了，可以可以
   - 看来空格数量很重要啊
2. 我是头2

    听说多段换行，前边得有4个空格真的是这样的吗

还真是这样的，你看我就乱了

引用里还能套列表？
> - 可不咋滴
> - 就是说呢
>     - 还能再套
>         - 牛逼啊
>         - 重点是4个空格
>     - 来个代码
>     ```python
>     def say_hello_v2(name):
>       print("吃了嘛您呐，", name)
>     ```
>         def say_hello_v3(name):
>           # print("8个空格居然也行")
>           print("大爷来玩啊，", name)

来个图 ![huang图](http://h.hiphotos.baidu.com/zhidao/pic/item/9f510fb30f2442a70656c087d043ad4bd11302b3.jpg)

真黄

再来个图 ![lv图][lv]

[lv]: http://a.hiphotos.baidu.com/zhidao/pic/item/562c11dfa9ec8a1353fd9b2df603918fa1ecc01c.jpg

绿了绿了

来个小黄图
<img src="http://h.hiphotos.baidu.com/zhidao/pic/item/9f510fb30f2442a70656c087d043ad4bd11302b3.jpg" width="30" height="20">

换行有两种方式  
一个是这样的<br>
还有一种是这样的  
就是在行尾敲俩空格

新起一段的话，加个空行就完事了

分隔符是个什么鬼？

---
这样的？  
记着有空行啊，不然就成标题了

还能用部分的html标记？

<b>是啊，又粗又*直*</b>

支持
```html
<kbd><b><i><em><sup><sub><br>
```
啥啥的，咱也不懂

还能写tex公式<br>
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a}. $$

先到这吧，累得慌了

完结撒花
-----
