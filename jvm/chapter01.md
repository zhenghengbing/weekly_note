
## JVM



- 对jvm的理解?jdk8虚拟机和之前的变化>

- oom,栈溢出StackoverflowError?怎么分析

- JVM常用调优参数

- 内存快照如何抓取,怎么分析Dump文件

- 类加载器

  

1. JVM的位置

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200714083435768.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L29rRm9ycmVzdDI3,size_16,color_FFFFFF,t_70#pic_center)

2. JVM的体系结构

   ![img](https://bkimg.cdn.bcebos.com/pic/bf096b63f6246b6042db690ee7f81a4c500fa2f7?x-bce-process=image/watermark,image_d2F0ZXIvYmFpa2U5Mg==,g_7,xp_5,yp_5)

   **大部分JVM调优都是在Java堆中调优，java栈、本地方方法栈、**

   **程序计数器是不会有垃圾存在的（栈用完就弹出了，并且随着线程结束而回收）**

3. 类加载器

4. 双亲委派机制

5. 沙箱安全机制

6. Native

7. PC寄存器

8. 方法区

9. 栈

10. 三种JVM

    ## HotSpot VM

    HotSpot VM是绝对的主流。大家用它的时候很可能就没想过还有别的选择，
    或者是为了迁就依赖了Oracle/Sun JDK某些具体实现的烂代码而选择用HotSpot VM省点心。
    Oracle / Sun JDK、OpenJDK的各种变种（例如IcedTea、Zulu），用的都是相同核心的HotSpot VM。
    当大家说起“Java性能如何如何”、“Java有多少种GC”、“JVM如何调优”云云，经常默认说的就是特指HotSpot VM。可见其“主流性”。
    JDK8的HotSpot VM已经是以前的HotSpot VM与JRockit VM的合并版，也就是传说中的“HotRockit”，只是产品里名字还是叫HotSpot VM。
    这个合并并不是要把JRockit的部分代码插进HotSpot里，而是把前者一些有价值的功能在后者里重新实现一遍。移除PermGen、Java Flight Recorder、jcmd等都属于合并项目的一部分
    不过要留意的是，这里的HotSpot VM特指“正常配置”版，而不包括“Zero / Shark”版。
    Wikipedia那个页面上把后者称为“Zero Port”。用这个版本的人应该相当少，很多时候它的release版都build不成功

    

    ## J9 VM

    J9是IBM开发的一个高度模块化的JVM。在许多平台上，IBM J9 VM都只能跟IBM产品一起使用。这不是技术限制，而是许可证限制。
    例如说在Windows上IBM JDK不是免费公开的，而是要跟IBM其它产品一起捆绑发布的；
    使用IBM Rational、IBM WebSphere的话都有机会用到J9 VM（也可以自己选择配置使用别的Java SE JVM）。
    根据许可证，这种捆绑在产品里的J9 VM不应该用于运行别的Java程序…大家有没有自己“偷偷的”拿来跑别的程序IBM也没力气管
    （咳咳而在一些IBM的硬件平台上，很少客户是只买硬件不买配套软件的，IBM给一整套解决方案，里面可能就包括了IBM JDK。
    这样自然而然就用上了J9 VM。
    所以J9 VM得算在主流里，虽然很少是大家主动选择的首选。
    J9 VM的性能水平大致跟HotSpot VM是一个档次的。有时HotSpot快些，有时J9快些。
    不过J9 VM有一些HotSpot VM在JDK8还不支持的功能，最显著的一个就是J9支持AOT编译和更强大的class data sharing

    

    ## JRockit

    JRockit以前Java SE的主流JVM中还有JRockit，跟HotSpot与J9一起并称三大主流JVM。
    这三家的性能水平基本都在一个水平上，竞争很激烈。
    自从Oracle把BEA和Sun都收购了之后，Java SE JVM只能二选一，JRockit就炮灰了。
    JRockit最后发布的大版本是R28，只到JDK6；原本在开发中的R29及JDK7的对应功能都没来得及完成项目就被终止了。

11. 堆

12. 新生代、老年代

13. 永久代

14. 堆内存调优

15. GC

    1. 常用算法

16. JMM
