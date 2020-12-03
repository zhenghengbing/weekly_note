# Class 4 【认识Netty】

# 什么是Netty？
Netty 是一个利用 Java 的高级网络的能力，隐藏其背后的复杂性而提供一个易于使用的 API 的客户端/服务器框架。
Netty 是一个广泛使用的 Java 网络编程框架（Netty 在 2011 年获得了Duke's Choice Award，见[https://www.java.net/dukeschoice/2011](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.java.net%2Fdukeschoice%2F2011)）。它活跃和成长于用户社区，像大型公司 Facebook 和 Instagram 以及流行 开源项目如 Infinispan, HornetQ, Vert.x, Apache Cassandra 和 Elasticsearch 等，都利用其强大的对于网络抽象的核心代码。
# Netty和Tomcat有什么区别？
Netty和Tomcat最大的区别就在于通信协议，Tomcat是基于Http协议的，他的实质是一个基于http协议的web容器，但是Netty不一样，他能通过编程自定义各种协议，因为netty能够通过codec自己来编码/解码字节流，完成类似redis访问的功能，这就是netty和tomcat最大的不同。
_有人说netty的性能就一定比tomcat性能高，其实不然，tomcat从6.x开始就支持了nio模式，并且后续还有APR模式——一种通过jni调用apache网络库的模式，相比于旧的bio模式，并发性能得到了很大提高，特别是APR模式，而netty是否比tomcat性能更高，则要取决于netty程序作者的技术实力了。_
# 为什么Netty受欢迎？
如第一部分所述，netty是一款收到大公司青睐的框架，在我看来，netty能够受到青睐的原因有三：

1. **并发高**
1. **传输快**
1. **封装好**
# Netty为什么并发高
Netty是一款基于NIO（Nonblocking I/O，非阻塞IO）开发的网络通信框架，对比于BIO（Blocking I/O，阻塞IO），他的并发性能得到了很大提高，两张图让你了解BIO和NIO的区别：


![2.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1606898349485-fb13face-fff7-4be7-8b7a-2fd0e4457ae1.png#align=left&display=inline&height=311&margin=%5Bobject%20Object%5D&name=2.png&originHeight=311&originWidth=548&size=7054&status=done&style=none&width=548)


![1.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1606899165962-3b2840af-a74b-4f02-aced-6cf2fd52e5f1.png#align=left&display=inline&height=476&margin=%5Bobject%20Object%5D&name=1.png&originHeight=476&originWidth=572&size=7504&status=done&style=none&width=572)
从这两图可以看出，NIO的单线程能处理连接的数量比BIO要高出很多，而为什么单线程能处理更多的连接呢？原因就是图二中出现的`Selector`。
当一个连接建立之后，他有两个步骤要做，第一步是接收完客户端发过来的全部数据，第二步是服务端处理完请求业务之后返回response给客户端。NIO和BIO的区别主要是在第一步。
在BIO中，等待客户端发数据这个过程是阻塞的，这样就造成了一个线程只能处理一个请求的情况，而机器能支持的最大线程数是有限的，这就是为什么BIO不能支持高并发的原因。
而NIO中，当一个Socket建立好之后，Thread并不会阻塞去接受这个Socket，而是将这个请求交给Selector，Selector会不断的去遍历所有的Socket，一旦有一个Socket建立完成，他会通知Thread，然后Thread处理完数据再返回给客户端——**这个过程是不阻塞的**，这样就能让一个Thread处理更多的请求了。
下面两张图是基于BIO的处理流程和netty的处理流程，辅助你理解两种方式的差别：


![1.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1606898337148-db1427be-5908-4833-a8b3-d9bff05561bc.png#align=left&display=inline&height=372&margin=%5Bobject%20Object%5D&name=1.png&originHeight=372&originWidth=584&size=11386&status=done&style=none&width=584)


![1.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1606899200121-eec63e95-e730-4929-a99f-dedc4df11a1d.png#align=left&display=inline&height=316&margin=%5Bobject%20Object%5D&name=1.png&originHeight=316&originWidth=525&size=14278&status=done&style=none&width=525)
# Netty为什么传输快
Netty的传输快其实也是依赖了NIO的一个特性——_零拷贝_。我们知道，Java的内存有堆内存、栈内存和字符串常量池等等，其中堆内存是占用内存空间最大的一块，也是Java对象存放的地方，一般我们的数据如果需要从IO读取到堆内存，中间需要经过Socket缓冲区，也就是说一个数据会被拷贝两次才能到达他的的终点，如果数据量大，就会造成不必要的资源浪费。
Netty针对这种情况，使用了NIO中的另一大特性——零拷贝，当他需要接收数据的时候，他会在堆内存之外开辟一块内存，数据就直接从IO读到了那块内存中去，在netty里面通过ByteBuf可以直接对这些数据进行直接操作，从而加快了传输速度。
下两图就介绍了两种拷贝方式的区别，摘自[Linux 中的零拷贝技术，第 1 部分](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.ibm.com%2Fdeveloperworks%2Fcn%2Flinux%2Fl-cn-zerocopy1%2Findex.html)
![1.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1606899381771-53f441da-c1e1-41e3-a10f-299307893871.png#align=left&display=inline&height=279&margin=%5Bobject%20Object%5D&name=1.png&originHeight=279&originWidth=481&size=8350&status=done&style=none&width=481)
传统数据拷贝
![2.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1606899395109-ff8e4ea4-fdfe-4377-b662-4725e02f942d.png#align=left&display=inline&height=321&margin=%5Bobject%20Object%5D&name=2.png&originHeight=321&originWidth=554&size=8554&status=done&style=none&width=554)
零拷贝
