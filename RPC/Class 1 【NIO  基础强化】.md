> # chapter 1
NIO  基础强化
java NIO 三要素： Channel 、 Buffer 、 Selector
Channel （通道）：
传统：1、阻塞 2、单向读写
NIO ：1、非阻塞  2、双向读写
Buffer  （缓存）：
三要素：position 、limit、 capacity
buffer：固定值，只能放入capacity个多种类型数据
position ：写，初始位置为0，写入后移动到下一个可写入位置，最大为capacity-1；读，从写模式切换之后，初始位置为0，读出后移动到下一个可读位置。
limit：
写，capacity - position；读，position（之前写入数据全部可读）
buffer方法：
allocate（int capacity）：分配大小
channel.read(buf):往buf放数据，从channel读
buf.put(byte):往buf放数据
channel.write(buf):从buf读数据，往channel写
buf.get(byte):从buf读数据
buf.rewind():将position置0
clear()与compact()方法:将limit置为capacity，clear，position置0，compact()，未读数据拷贝到buffer起始处，将position置为最后一个未读
mark()与reset()方法:mark（）可标记一个特定的position，之后可调用reset（）回到该位置
Selector （复用器）：
和channel配合使用，channel注册在selector之后，监听channel状态
connect：已连接
accept：等待连接
read：可读
write：可写
