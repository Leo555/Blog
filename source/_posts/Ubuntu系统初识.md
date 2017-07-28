---
title: Ubuntu系统初识
date: 2016-08-01 19:28:00
tags: 
- Ubuntu
- Linux
- Python
categories: Linux
---
![](http://p1.bpimg.com/567571/8944a6d72c32f89f.png)
# 简介

Ubuntu是一个以桌面应用为主的Linux操作系统，可在智能手机、平板电脑、个人电脑、服务器和云VPS的上面看到Ubuntu的身影，是目前最为流行的Linux桌面操作系统。本文我们就来学习Ubuntu操作系统的安装和简单使用。
<!-- more -->

# 虚拟机安装Ubuntu

在Linux学习阶段，使用虚拟机的好处是，无论任何时候操作系统出现问题，我们都可以通过快照功能恢复到安全保存的阶段，以降低学习成本。而且可以在本地创建多个虚拟机，这些虚拟机相互独立，又处于同一局域网内，非常适合学习集群方面的知识。

接下来是虚拟机安装Ubuntu的方法

## 下载安裝VMware Workstation

下载地址：[http://www.vmware.com/products/workstation.html](http://www.vmware.com/products/workstation.html)

安装后启动效果如下：
![VMware](http://p1.bpimg.com/567571/45ba835382086b78.png)

VMware安装后会自动将自己设置为Windows的服务，所以会一直常驻内存
![Windows service](http://i1.piimg.com/567571/a25ec0cf714267ba.png)

如果不喜欢开启启动的话可以设置为手动启动，需要使用的时候再手动启动。

安装后如果需要卸载推荐使用 [VMware_Install_Cleaner](http://vmware-install-cleaner.en.softonic.com/)

## 下载Ubuntu操作系统

下载地址： [http://www.ubuntu.com/download/desktop/thank-you/?version=16.04.1&architecture=amd64](http://www.ubuntu.com/download/desktop/thank-you/?version=16.04.1&architecture=amd64)


## 虚拟机安装Ubuntu

打开VMware，**“File--New Virtual Machine”**

![1](http://p1.bqimg.com/567571/be556291e5f74f42.png)

选择典型安装即可

![2](http://p1.bqimg.com/567571/0e8cb4d1b9cea697.png)

注意这里一点要以后再安装，如果选第二个的话，会使用Easy Install安装不完整的Ubuntu，可能会影响之后的使用。

![3](http://p1.bqimg.com/567571/3aa9a99447c8d6a4.png)

选择安装位置，如果以后想要删除此虚拟机，只要删除这个文件夹即可

![4](http://p1.bqimg.com/567571/2dc88f5062860b56.png)

选择虚拟机所占磁盘大小，注意这里指的是最大磁盘大小，所以完全不用担心虚拟机把你的磁盘都用了。

![5](http://p1.bqimg.com/567571/5c24e476001e2b18.png)

安装完成

![6](http://p1.bqimg.com/567571/13d5ce2d9f7b795d.png)

编辑虚拟机设置
点击Edit virtual machine settings

![1](http://i1.piimg.com/567571/1d4dde497a1dfb07.png)

设置ISO image路径

![2](http://i1.piimg.com/567571/00f04e5b5efdcd93.png)

其它选项可以自行修改

启动虚拟机

![3](http://i1.piimg.com/567571/63da4488b80054e7.png)

虚拟机第一次启动后选择 “Try Ubuntu” 

![4](http://p1.bpimg.com/567571/b992ad12cabade3d.png)

Ubuntu启动后的样子

![5](http://i1.piimg.com/567571/536c898b3ae0384e.png)

点击右上角的设置按钮，在“System settings”中设置屏幕分辨率，否则会导致安装Ubuntu过程中无法选择确定按钮。

![6](http://i1.piimg.com/567571/f8729c5b74cb9179.png)

这些设置完成以后就可以真正安装Ubuntu了。

![7](http://i1.piimg.com/567571/6c550f9697439ee8.png)

安装过程一路 **continue**即可

![8](http://i1.piimg.com/567571/fde1b11b91245d7c.png)

选择时区为上海

![9](http://i1.piimg.com/567571/7755afd5b8d5c279.png)

设置电脑名和密码

![10](http://i1.piimg.com/567571/033702c975b5d29a.png)

开始安装，稍等片刻

![11](http://i1.piimg.com/567571/14013024c867d814.png)

以上终于完成安装。
完成安装后第一件事： 给虚拟机保存一个快照，以后如果虚拟机出了问题崩溃了，可以利用快照功能回到快照时的状态

![12](http://p1.bqimg.com/567571/13a5c36c079f891e.png)

不过快照功能会占用比较多的磁盘，所以尽量在比较关键的点上创建快照。

# 更换Python版本

Ubuntu上默认使用Python2.7版本，而我需要使用3.5的版本，但是Ubuntu很多底层采用的是Python2，所以不能卸载Python2，需要将默认Python的指向Python3。

（ctrl+alt+T）打开Terminal，输入sudo apt-get install python3安装python3

![python3](http://p1.bqimg.com/567571/fd1054169f9f330b.png)


刚才的Python3是被默认安装到/usr/local/lib/python3.5目录中

![python3.5](http://p1.bqimg.com/567571/a8a72bf993584d7d.png)

首先，删除/usr/bin/目录下的默认python link文件

```
$ cd /usr/bin  
$ sudo rm -rf python 
```

然后建立新的连接关系：
```
$ sudo ln -s /usr/bin/python3.5 /usr/bin/python
```

查看当前python版本
```
$ python --version
```

![python版本](http://p1.bqimg.com/567571/9c526bc0808c5cea.png)

此时已成功将Ubuntu里面默认的Python版本换成Python3了

# 安装Archsocks

Archsocks是一个可免费可收费的代理服务。
下载地址： [https://github.com/archsocks/archsocks](https://github.com/archsocks/archsocks)

使用firefox下载到 **/home/Downloads** 目录下
双击解压，或者使用命令 tar -xzvf archsocks.tgz.gz 解压
由于archsocks是用python编写，所以请确保上一步安装py3成功。
然后运行archsocks文件即可。
```
$ sudo sh archsocks
```
运行后浏览器自动打开 **127.0.0.1:9501**, 测试google可用。

![google](http://i1.piimg.com/567571/9153e2c1e9b78f5d.png)


# 安装JDK设置环境

## 下载JDK

首先去Oracle官网下载JDK

![JDK](http://p1.bqimg.com/567571/cbbe21f327051a66.png)

这里选择源码安装

## 解压

将下载的tar.gz文件解压。
```
$ sudo tar zxvf ./jdk-8u101-linux-x64.tar.gz
```
为了方便管理，可以将解压后的文件转移到另一个文件夹，当然不做也行。
为了方便下一步设置环境变量，将文件夹换了个短点的名字 —— jdk
可使用如下命令对文件夹重命名
```
$sudo mv jdk-8u101-linux-x64/ jdk/
```

## 设置环境变量

编辑 .bashrc 文件。
在终端输入如下命令：
```
$ vi ~/.bashrc
```
在该文件的末尾，加上以上几行代码：
```
export JAVA_HOME=/home/leo/Downloads/jdk
export CLASSPATH=${JAVA_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```

注意设置JAVA_HOME为刚才解压后移动的位置

为了让更改立即生效，请在终端执行如下命令：
```
$ source ~/.bashrc
```

## 验证

通过以上步骤，JDK已安装完成。
输入以下命令验证 java -version ，如图：

![java](http://i1.piimg.com/567571/f5e3428c5e466ef4.png)


# 总结

万事开头难，所幸我终于开头了。
