# docker 使用入门
[TOC]
本文仅从实用角度介绍 docker 在 Linux 平台的简单使用。<br>
文中内容已在 centos7 中进行验证。<br>
使用 docker --help 查看命令帮助。
## docker 安装
```shell
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
```
## 权限添加
命令执行后，普通用户执行 docker 命令需要加上 sudo 前缀，如果想直接运行 docker 命令，可以通过如下方法修改：
```shell
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
$ newgrp docker
```
如果命令不生效，继续执行：
```shell
$ sudo chown root:docker /var/run/docker.sock
```
要是还不无效，继续执行：
```shell
$ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
$ sudo chmod g+rwx "$HOME/.docker" -R
```
要是还不行，暂时没辙了，再想法吧。
## docker 运行 centos7
首先拉取官方centos7镜像
```shell
$ docker pull centos:centos7
```
成功后可以通过如下命令查看image:
```shell
$ docker image ls
```
运行镜像，指定 32768 端口映射 docker 内 22 端口，方便远程 ssh 连接
```shell
$ docker run -d -p 32768:22 --name centos7 --privileged=true centos:centos7 /usr/sbin/init
```
查看运行中的container
```shell
$ docker container ls
```
可以看到 container 状态和 container_id。
## 设置 centos7
运行起来的 centos 是最小安装，无法进行 ssh 连接，需要进一步设置。<br>
根据 container_id 进入容器内部
```shell
$ docker exec -it $container_id /bin/bash
```
进入 container 之后，安装基础包
```shell
# yum install -y openssh-server vim lrzsz wget gcc-c++ pcre pcre-devel zlib zlib-devel ruby openssl openssl-devel patch bash-completion zlib.i686 libstdc++.i686 lsof unzip zip bzip2 initscripts net-tools sudo openssh-clients
```
接下来生成 ssh_key:
```shell
# ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
# ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
# ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
然后重启 ssh 服务
```shell
# systemctl restart sshd
```
修改 root 用户密码：
```shell
# passwd root
```
添加 huairuo 用户(可以添加到wheel用户组，直接具有sudo权限)：
```shell
# useradd -G wheel -m huairuo
# passwd huairuo
```
至此，已经可以通过 ssh 进入到 docker 了，连接端口即为上文映射的端口。
## docker 容器备份
首先查看所有的container:
```shell
$ docker container ls
```
假设需要备份的 container_id 为 30b8f18f20b4，备份生成的镜像名为 container-backup，则备份命令为：
```shell
$ docker commit -p 30b8f18f20b4 container-backup
```
执行后可以通过如下命令查看已生成的 image:
```shell
$ docker image ls
```
可以将备份的 image 另存为 tar 包，以便日后使用
```shell
$ docker save -o container-backup.tar container-backup
```
将 tar 包还原为 image：
```shell
$ docker load -i container-backup.tar
```
结果查看
```shell
$ docker image ls
```
## container 初始容量调整
container 默认大小是 10G，使用过程中可能出现存储空间不足的问题。已验证的一种修改方法如下：
1. 关闭 docker 服务：

    ```shell
    $ sudo systemctl stop docker
    ```
2. **慎重！** 删除 docker 文件（包括 image 和 container)
    ```shell
    $ sudo rm -rf /var/lib/docker
    ```
3. 修改 docker.service 文件
    ```shell
    $ sodu vim /usr/lib/systemd/system/docker.service
    ```
    需要修改的行是：
    ```ini
    ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
    ```
    修改为：
    ```ini
    ExecStart=/usr/bin/dockerd --storage-driver devicemapper --storage-opt dm.loopdatasize=500G --storage-opt dm.loopmetadatasize=10G --storage-opt dm.fs=ext4 --storage-opt dm.basesize=100G -H fd:// --containerd=/run/containerd/containerd.sock
4. 配置文件刷新
    ```shell
    $ sudo systemctl daemon-reload
    ```
5. 重启 docker
    ```shell
    $ sudo systemctl start docker
    ```
6. 重新拉取或载入镜像，进行后续操作。
## 完成啦啦啦~~~