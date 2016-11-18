title: Hadoop环境搭建
tags:
  - Big Data
  - Hadoop
categories: Big Data
date: 2016-09-15 20:11:00
---
# 开发环境搭建

## 安装虚拟机

使用的是[VMware Workstation](http://www.vmware.com/products/workstation.html)

## 安装操作系统

ubuntu-16.04-desktop-amd64

安装虚拟机和操作系统的教程可以参考之前的Blog: [Ubuntu系统初识](http://www.lz5z.com/Ubuntu%E7%B3%BB%E7%BB%9F%E5%88%9D%E8%AF%86/)

<!-- more -->
## 下载Hadoop

如果你在官网上下载比较慢的话可以去这个网站看下
[http://mirror.bit.edu.cn/apache/hadoop/common/](http://mirror.bit.edu.cn/apache/hadoop/common)

我们选择最新的稳定版本2.7.3

![download](http://p1.bpimg.com/567571/a492d2482490772d.png)

下载速度非常快

## 安装Hadoop

首先解压hadoop文件到/usr/local 路径下，并且重命名为hadoop

```shell
$ sudo tar -zxvf hadoop2.7.3.tar.gz /usr/local hadoop
```

修改文件权限

```shell
$ cd /usr/local/hadoop
$ sudo chown -R hadoop ./hadoop
```

Hadoop 解压后即可使用。输入如下命令来检查 Hadoop 是否可用，成功则会显示 Hadoop 版本信息：

```shell
$ cd /usr/local/hadoop
$ ./bin/hadoop version
```

配置Hadoop环境变量（由于小白还用不惯vim, 暂时使用gedit命令）

```shell
$ sodu gedit ~/.bashrc
```
在里面加入

```shell
export HADOOP_HOME=/usr/local/hadoop
export PATH=${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:$PATH
```

然后输入以下命令是环境变量生效

```shell
$ source ~/.bashrc
```

在Linux中，~目录表示主目录。比如你要到下载文件夹下，就可以输入

```shell
$ cd ~/Downloads
```

## 安装SSH、配置SSH无密码登陆

集群、单节点模式都需要用到 SSH 登陆（类似于远程登陆，你可以登录某台 Linux 主机，并且在上面运行命令），Ubuntu 默认已安装了 SSH client，此外还需要安装 SSH server：

```shell
$ sudo apt-get install openssh-server
```

安装后，可以使用如下命令登陆本机：

```shell
$ ssh localhost
```

但这样登陆是需要每次输入密码的，我们需要配置成SSH无密码登陆比较方便。

首先退出刚才的 ssh，就回到了我们原先的终端窗口，然后利用 ssh-keygen 生成密钥，并将密钥加入到授权中

```shell
$ exit                           # 退出刚才的 ssh localhost
$ cd ~/.ssh/                     # 若没有该目录，请先执行一次ssh localhost
$ ssh-keygen -t rsa              # 会有提示，都按回车就可以
$ cat ./id_rsa.pub >> ./authorized_keys  # 加入授权
```

此时再用 ssh localhost 命令，无需输入密码就可以直接登陆了

# 环境配置

## Hadoop单机配置(非分布式)

Hadoop 默认模式为非分布式模式，无需进行其他配置即可运行。非分布式即单 Java 进程，方便进行调试。

现在我们可以执行例子来感受下 Hadoop 的运行。

官网上给了一个比较简单的例子

```shell
$ mkdir input 
$ cp etc/hadoop/*.xml input  # 将配置文件作为输入文件
$ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar grep input output 'dfs[a-z.]+' # 查询配置文件中符合正规dfs* 字符出现的次数
$ cat output/*   # 查看运行结果
```

## Hadoop伪分布式配置

Hadoop 可以在单节点上以伪分布式的方式运行，Hadoop 进程以分离的 Java 进程来运行，节点既作为 NameNode 也作为 DataNode，同时，读取的是 HDFS 中的文件。

使用以下配置文件

etc/hadoop/core-site.xml:
```xml
<configuration>
	<property>
	    <name>fs.defaultFS</name>
	    <value>hdfs://localhost:9000</value>
	</property>
	<property>
	  <name>hadoop.proxyuser.dev.groups</name>
	  <value>*</value>
	  <description>Allow the superuser oozie to impersonate any members of the group group1 and group2</description>
	</property>
	<property>
	  <name>hadoop.proxyuser.dev.hosts</name>
	  <value>localhost</value>
	<description>The superuser can connect only from host1 and host2 to impersonate a user</description>
	</property>
</configuration>
```

etc/hadoop/hdfs-site.xml:
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```
Hadoop配置文件说明:

Hadoop 的运行方式是由配置文件决定的（运行 Hadoop 时会读取配置文件），因此如果需要从伪分布式模式切换回非分布式模式，需要删除 core-site.xml 中的配置项。

此外，伪分布式虽然只需要配置 fs.defaultFS 和 dfs.replication 就可以运行（官方教程如此），不过若没有配置 hadoop.tmp.dir 参数，则默认使用的临时目录为 /tmp/hadoo-hadoop，而这个目录在重启时有可能被系统清理掉，导致必须重新执行 format 才行。所以我们进行了设置，同时也指定 dfs.namenode.name.dir 和 dfs.datanode.data.dir，否则在接下来的步骤中可能会出错。

配置完成后，执行 NameNode 的格式化:

```shell
$ ./bin/hdfs namenode -format
```

如果刚才有在环境变量中加入 **export PATH=${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:$PATH**，关于Hadoop的所有命令均可以直接使用，而不需要加入路径信息。

上述命令可以写成
```shell
$ hdfs namenode -format
```

接着开启 NameNode 和 DataNode 守护进程

```shell
$ ./sbin/start-dfs.sh  #如果已经开启，请先使用stop-dfs.sh关闭
```

成功启动后，可以访问 Web 界面 http://localhost:50070 查看 NameNode 和 Datanode 信息，还可以在线查看 HDFS 中的文件。

![](http://7xrn7f.com1.z0.glb.clouddn.com/16-11-1/92254301.jpg)

若要关闭 Hadoop，则运行

```shell
$ ./sbin/stop-dfs.sh
```

下次启动 hadoop 时，无需进行 NameNode 的初始化，只需要运行 ./sbin/start-dfs.sh 就可以

## 启动YARN

YARN 的全称是“Yet Another Resource Negotiator”， 也就是新一代的MapReduce 框架

YARN 是从 MapReduce 中分离出来的，负责资源管理与任务调度。YARN 运行于 MapReduce 之上，提供了高可用性、高扩展性。

首先修改配置文件 mapred-site.xml，在源文件中只找到了“mapred-site.xml.template” 文件，所以我们将其复制并重命名

```shell
$ sudo cp ./etc/hadoop/mapred-site.xml.template ./etc/hadoop/mapred-site.xml
```

然后用个gedit进行编辑 

```shell
$ sudo gedit ./etc/hadoop/mapred-site.xml
```
```xml
<configuration>
    <property>
         <name>mapreduce.framework.name</name>
         <value>yarn</value>
    </property>
</configuration>
```

接着修改配置文件 yarn-site.xml：

```xml
<configuration>
    <property>
         <name>yarn.nodemanager.aux-services</name>
         <value>mapreduce_shuffle</value>
        </property>
</configuration>
```

然后就可以启动 YARN 了（需要先执行过 ./sbin/start-dfs.sh）：

```shell
$ ./sbin/start-yarn.sh      # 启动YARN
$ ./sbin/mr-jobhistory-daemon.sh start historyserver  # 开启历史服务器，才能在Web中查看任务运行情况
```
启动 YARN 之后可以通过 Web 界面查看任务的运行情况：http://localhost:8088/cluster

![](http://7xrn7f.com1.z0.glb.clouddn.com/16-11-1/92785083.jpg)

但 YARN 主要是为集群提供更好的资源管理与任务调度，然而这在单机上体现不出价值，反而会使程序跑得稍慢些。因此在单机上是否开启 YARN 就看实际情况了

如果不想启动 YARN，务必把配置文件 mapred-site.xml 删除，需要用时再重新cp。
否则在该配置文件存在，而未开启 YARN 的情况下，运行程序会提示 “Retrying connect to server: 0.0.0.0/0.0.0.0:8032” 的错误，这也是为何该配置文件初始文件名为 mapred-site.xml.template。

关闭 YARN 的脚本如下：
```shell
$ ./sbin/stop-yarn.sh
$ ./sbin/mr-jobhistory-daemon.sh stop historyserver
```

# HBase

## 简介

HBase是一个分布式，版本化，面向列的数据库，构建在 Apache Hadoop和 Apache ZooKeeper之上。

HBase [官方文档](http://abloz.com/hbase/book.html)

## 安装HBase

下载解压到 /usr/local/hbase 

配置HBase环境变量

```
export HBASE_HOME=/usr/local/hbase
export PATH=$PATH:${HBASE_HOME}/bin
```

修改配置文件 hbase-site.xml 

```shell
$ cd $HBASE_HOME/conf
$ sudo gedit hbase-site.xml
```

```xml
<configuration>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://localhost:9000/user/dev</value>
    </property>
    <property>
        <name>hbase.zookeeper.property.dataDir</name>
        <value>/home/dev/zookeeper</value>
    </property>
</configuration>
```

修改启动文件 hbase-env.sh

```
export JAVA_HOME=/usr/local/jdk
export HBASE_CLASSPATH=/usr/local/hbase/conf
export HBASE_MANAGES_ZK=true
```

一个分布式运行的Hbase依赖一个zookeeper集群。所有的节点和客户端都必须能够访问zookeeper。
默认的情况下Hbase会管理一个zookeep集群。这个集群会随着Hbase的启动而启动。
conf/hbase-env.sh里面的 “HBASE_MANAGES_ZK=true” 表示作用是让Hbase启动的时候同时也启动zookeeper。

启动HBase

```shell
$ cd $HBASE_HOME
$ bin/start-hbase.sh
```

启动HBase之后可以通过 Web 页面查看运行状况： http://localhost:16010/master-status

![](http://p1.bqimg.com/567571/ca249d5a624f81d0.png)

## HBase shell操作

用shell连接你的HBase

```shell
$ ./bin/hbase shell
... 

hbase(main):001:0> 
```

创建一个名为 test 的表，这个表只有一个 列族 为 cf。可以列出所有的表来检查创建情况，然后插入些值。

```shell
hbase(main):003:0> create 'test', 'cf'
0 row(s) in 1.2200 seconds
hbase(main):003:0> list 'table'
test
1 row(s) in 0.0550 seconds
hbase(main):004:0> put 'test', 'row1', 'cf:a', 'value1'
0 row(s) in 0.0560 seconds
hbase(main):005:0> put 'test', 'row2', 'cf:b', 'value2'
0 row(s) in 0.0370 seconds
hbase(main):006:0> put 'test', 'row3', 'cf:c', 'value3'
0 row(s) in 0.0450 seconds
```
以上我们分别插入了3行。第一个行key为row1, 列为 cf:a， 值是 value1。HBase中的列是由 列族前缀和列的名字组成的，以冒号间隔。例如这一行的列名就是a.

检查插入情况.

Scan这个表，操作如下

```shell
hbase(main):007:0> scan 'test'
ROW        COLUMN+CELL
row1       column=cf:a, timestamp=1288380727188, value=value1
row2       column=cf:b, timestamp=1288380738440, value=value2
row3       column=cf:c, timestamp=1288380747365, value=value3
3 row(s) in 0.0590 seconds
```

Get一行，操作如下

```shell
hbase(main):008:0> get 'test', 'row1'
COLUMN      CELL
cf:a        timestamp=1288380727188, value=value1
1 row(s) in 0.0400 seconds
```

disable 再 drop 这张表，可以清除你刚刚的操作

```shell
hbase(main):012:0> disable 'test'
0 row(s) in 1.0930 seconds
hbase(main):013:0> drop 'test'
0 row(s) in 0.0770 seconds 
```

关闭shell

```shell
hbase(main):014:0> exit
```



# 总结

如果按照上诉方法搭建好Hadoop相关环境，在重启电脑后，可以用以下命令迅速启动所有程序。

```shell
$ hdfs namenode -format
$ start-dfs.sh  #http://localhost:50070
$ start-yarn.sh  #http://localhost:8088/cluster
$ start-hbase.sh  #http://localhost:16010/master-status
```