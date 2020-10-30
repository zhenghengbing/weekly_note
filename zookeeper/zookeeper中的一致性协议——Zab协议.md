# zookeeper中的一致性协议——Zab协议
  zab协议的全称是Zookeeper Atomic Broadcast（zookeeper原子广播），zookeeper是通过zab协议来保证分布式事务的最终一致性。
## 什么是Zab协议
  zab协议是为分布式协调服务zookeeper专门设计的一周**支持崩溃恢复**的**原子广播协议**，是zookeeper保证数据一致性的核心算法。zab协议借鉴了paxos算法，但又不想paxos那样是一种通用的分布式一致性算法。
  zookeeper中主要依赖zab协议来实现数据一致性，基于该协议，zk实现了 一种主备模型（即Leader和Follower模型）的系统架构来保证集群中各个副本之间的数据一致性。这里的主备系统架构模型，就是指只有一台服务器（leader）负责处理外部的写事务请求，然后leader端将数据同步到其他follwer节点。
  zk客户端会随机的连接到zk集群中的一个节点，如果是读请求，就直接从当前节点读取数据，如果是写请求，那么节点会向leader端提交事务，leader接收到事务提交，会广播该事务，只要超过半数节点写入成功，该事务就会被提交。

### zab协议的特性
  1.zab协议需要确保那些已经在leader服务器上提交的事务被所有的服务器提交  
  2.zab协议需要确保丢弃那些只在leader服务器上提出而没有提交的事务  

## zab协议实现的作用
1.使用一个单一的主进程（leader）来接收并处理客户端的事务请求（写请求），并采用了zab的原子广播协议，将服务器数据的状态变更以**事务proposal**（事务提议）的形式广播到所有的follower服务器上。  
2.保证一个全局的变更序列被顺序引用，zk是一个树形的结构，很多操作都需要先检查才能绝对是否执行，为了保证这一点，zab要保证同一个leader发起的事务要被顺序执行，同事还要保证只有先前的leader提交的的事务被执行之后，当前的leader服务器才可以发起事务。
3.当leader进程出现异常的时候，整个zk集群可以正常工作。
## zab协议原理
  zab协议要求每个leader都要经历三个阶段：发现，同步，广播
**发现**：要求zk必须选出一个leader进程，同事leader会维护一个follower可用客户端列表。将来客户端可以和这些follower节点进行通信。  
**同步**：leader要负责将本身的数据和follower完成同步，做很多副本存储。follower队列将队列中未处理完的请求消费完成后，写入本地事务日志中。  
**广播**：leader可以接受客户端新的事务proposal请求，将新的proposal请求广播给所有的follower。  

## zab协议内容
zab协议包括两种基本的模式：**崩溃恢复**和**消息广播**  
### 协议过程
  当整个集群启动过程中，或者当leader服务器出现网络中断，崩溃退出或重启等异常时，或者集群中超过半数的follower服务器不能与leader保持正常通信，zab协议就会进入崩溃恢复模式，选举出新的leader。当选举出了新的leader，同时集群中超脱半数的服务器和该leader服务器完成了数据同步，zab协议就会退出崩溃恢复模式，进入消息广播模式。
### 消息广播
  在zk集群中，数据副本的传递策略就是通过消息广播模式。消息广播类似于一个二段提交，但是又有所不同，二段提交要求协调者必须等待所有参与者全部反馈确认消息后，才能发送commit消息。而zab协议中的消息广播模式，只要求半数以上的follower返回确认消息就可以发送commit消息了。
#### 消息广播的步骤
1.客户端发起一个写请求
2.leader服务器将客户端的写请求转换为事务proposal提案，同时为每一个proposal分配一个全局的ID，即zxid  
3.leader服务器为每一个follower服务器分配一个单独队列，然后将需要广播的proposal依次放入到队列中去，根据FIFO策略进行消息发送  
4.follower收到proposal之后，首先将其以事务日志的方式写入本地磁盘，写入成功之后返回ack确认消息  
5.leader服务器接收到半数以上的follower返回的ack确认消息之后，发送commit消息，并提交本身的事务  
6.follower接收到commit消息之后，提交事务日志中的上一条事务  

### 崩溃恢复
  一旦leader服务器出现崩溃或者超过半数的follower服务器不能正常连接，就会进入到崩溃恢复模式。  
  崩溃恢复主要包括两部分**leader选举**和**数据恢复**  
#### leader选举
  成为leader的条件：
  1.epoch值是最大的  
  2.若epoch值相等，选择zxid值最大的  
  3.若epoch和zxid值都相等，选择server_id最大的（server_id就是zoo.cfg中的myid）  
  **解析一下epoch和zxid，zxid是每个服务器维护的一个事务id，是一个64位的数字，其中高32位代表的是epoch值，这个值的意义是每经过一个leader选举，epoch值加1，而低32位代表着在这个epoch值下，该服务器进行的事务次数，也是每提交了一次事务加1。**  
  每个节点也就是每个follower服务器在选举前，都默认投票给自己，当接收到其他节点的选票时，会根据leader选举条件更改自己的选票，然后重新发送选票给其他节点。当有一个节点获得 的选票超过半数时，该节点自动成为新的leader，其他节点就变成了follwer节点了。  
#### 数据恢复
  1.完成 Leader 选举后（新的 Leader 具有最高的zxid），在正式开始工作之前（接收事务请求，然后提出新的 Proposal），Leader 服务器会首先确认事务日志中的所有的 Proposal 是否已经被集群中过半的服务器 Commit。
  2.Leader 服务器需要确保所有的 Follower 服务器能够接收到每一条事务的 Proposal ，并且能将所有已经提交的事务 Proposal 应用到内存数据中。等到 Follower 将所有尚未同步的事务 Proposal 都从 Leader 服务器上同步过啦并且应用到内存数据中以后，Leader 才会把该 Follower 加入到真正可用的 Follower 列表中。
##### Zab 数据恢复过程中，如何处理需要丢弃的proposal
  当一个包含了上一个 Leader 周期中尚未提交过的事务 Proposal 的服务器启动时，当这台机器加入集群中，以 Follower 角色连上 Leader 服务器后，Leader 服务器会根据自己服务器上最后提交的 Proposal 来和 Follower 服务器的 Proposal 进行比对，比对的结果肯定是 Leader 要求 Follower 进行一个回退操作，回退到一个确实已经被集群中过半机器 Commit 的最新 Proposal。
##### Zab 数据恢复过程中，如何保证已经提交的proposal被所有的服务器提交
  新的leader的zxid值是最大的，代表的是上一个leader提交的事务它都提交了，所以当有其他的follwer服务器进来之后，如果zxid值是比leader值小，该follwer服务器要执行一次事务提交的操作。
