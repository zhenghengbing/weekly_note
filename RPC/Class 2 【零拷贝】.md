# 零拷贝

# 原始IO
![1.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1603783599374-4bfb0667-f4d1-4f4c-a5bc-66119730cbe7.png#align=left&display=inline&height=634&margin=%5Bobject%20Object%5D&name=1.png&originHeight=634&originWidth=1080&size=125208&status=done&style=none&width=1080)


1、CPU 发出对应的指令给磁盘控制器，然后返回；
2、磁盘控制器收到指令后，于是就开始准备数据，会把数据放入到磁盘控制器的内部缓冲区中，然后产生一个中断；
3、CPU 收到中断信号后，停下手头的工作，接着把磁盘控制器的缓冲区的数据一次一个字节地读进自己的寄存器，然后再把寄存器里的数据写入到内存，而在数据传输的期间 CPU 是无法执行其他任务的。
问题：
整个数据的传输过程，都要需要 CPU 亲自参与搬运数据的过程，而且这个过程，CPU 是不能做其他事情的
# DMA：
![2.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1603783933369-1a69ffa2-c57c-4954-b6f0-f59de0640db2.png#align=left&display=inline&height=507&margin=%5Bobject%20Object%5D&name=2.png&originHeight=507&originWidth=1080&size=100644&status=done&style=none&width=1080)

- 用户进程调用 read 方法，向操作系统发出 I/O 请求，请求读取数据到自己的内存缓冲区中，进程进入阻塞状态；

- 操作系统收到请求后，进一步将 I/O 请求发送 DMA，然后让 CPU 执行其他任务；

- DMA 进一步将 I/O 请求发送给磁盘；

- 磁盘收到 DMA 的 I/O 请求，把数据从磁盘读取到磁盘控制器的缓冲区中，当磁盘控制器的缓冲区被读满后，向 DMA 发起中断信号，告知自己缓冲区已满；

- **DMA 收到磁盘的信号，将磁盘控制器缓冲区中的数据拷贝到内核缓冲区中，此时不占用 CPU，CPU 可以执行其他任务**；

- 当 DMA 读取了足够多的数据，就会发送中断信号给 CPU；

- CPU 收到 DMA 的信号，知道数据已经准备好，于是将数据从内核拷贝到用户空间，系统调用返回

改进：
数据搬运工作由DMA完成，解放了CPU
# 传统文件传输：
![3.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1603784120315-675a6931-6ddf-4fee-a333-c0f1eef436ef.png#align=left&display=inline&height=666&margin=%5Bobject%20Object%5D&name=3.png&originHeight=666&originWidth=1080&size=118953&status=done&style=none&width=1080)

问题：
四次上下文切换，四次数据拷贝
# 零拷贝实现方式：
## 1、mmap+write
![4.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1603784285152-77234d8f-8d7a-4f5c-90aa-da28463dcab7.png#align=left&display=inline&height=665&margin=%5Bobject%20Object%5D&name=4.png&originHeight=665&originWidth=1080&size=119457&status=done&style=none&width=1080)
将内核缓冲区映射到用户缓冲区（四次上下文切换，三次数据拷贝）
## 2、sendfile
![5.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1603784414868-413f607d-afac-4920-ac9e-d8d460167ea6.png#align=left&display=inline&height=674&margin=%5Bobject%20Object%5D&name=5.png&originHeight=674&originWidth=1080&size=153178&status=done&style=none&width=1080)
数据不再拷贝到用户态（两次上下文切换，三次数据拷贝）
#### 改进型（网卡需支持 SG-DMA（_The Scatter-Gather Direct Memory Access_）技术）
![6.png](https://cdn.nlark.com/yuque/0/2020/png/2774814/1603784570077-36926d73-e062-4e29-8460-e591a1002438.png#align=left&display=inline&height=639&margin=%5Bobject%20Object%5D&name=6.png&originHeight=639&originWidth=1080&size=150381&status=done&style=none&width=1080)
socket缓冲区只需要数据信息（描述符、长度），不需要传输内容（两次数据拷贝，两次上下文切换）
# 使用零拷贝项目：Kafka、 Netty、Nginx
# 总结
早期 I/O 操作，内存与磁盘的数据传输的工作都是由 CPU 完成的，而此时 CPU 不能执行其他任务，会特别浪费 CPU 资源。
于是，为了解决这一问题，DMA 技术就出现了，每个 I/O 设备都有自己的 DMA 控制器，通过这个 DMA 控制器，CPU 只需要告诉 DMA 控制器，我们要传输什么数据，从哪里来，到哪里去，就可以放心离开了。后续的实际数据传输工作，都会由 DMA 控制器来完成，CPU 不需要参与数据传输的工作。
传统 IO 的工作方式，从硬盘读取数据，然后再通过网卡向外发送，我们需要进行 4 上下文切换，和 4 次数据拷贝，其中 2 次数据拷贝发生在内存里的缓冲区和对应的硬件设备之间，这个是由 DMA 完成，另外 2 次则发生在内核态和用户态之间，这个数据搬移工作是由 CPU 完成的。
为了提高文件传输的性能，于是就出现了零拷贝技术，它通过一次系统调用（`sendfile` 方法）合并了磁盘读取与网络发送两个操作，降低了上下文切换次数。另外，拷贝数据都是发生在内核中的，天然就降低了数据拷贝的次数。
Kafka 和 Nginx 都有实现零拷贝技术，这将大大提高文件传输的性能。
零拷贝技术是基于 PageCache 的，PageCache 会缓存最近访问的数据，提升了访问缓存数据的性能，同时，为了解决机械硬盘寻址慢的问题，它还协助 I/O 调度算法实现了 IO 合并与预读，这也是顺序读比随机读性能好的原因。这些优势，进一步提升了零拷贝的性能。
需要注意的是，零拷贝技术是不允许进程对文件内容作进一步的加工的，比如压缩数据再发送。
另外，当传输大文件时，不能使用零拷贝，因为可能由于 PageCache 被大文件占据，而导致「热点」小文件无法利用到 PageCache，并且大文件的缓存命中率不高，这时就需要使用「异步 IO + 直接 IO 」的方式。
在 Nginx 里，可以通过配置，设定一个文件大小阈值，针对大文件使用异步 IO 和直接 IO，而对小文件使用零拷贝。
