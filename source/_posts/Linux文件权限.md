---
title: Linux 文件权限
date: 2017-10-10 19:06:38
categories: Linux
tags: 
- 权限

---

## linux 文件属性

linux 中用户相对于文件有三种身份：owner、group、others，每种身份各有 read、write、execute 三种权限。

使用 `ls -l` 命令可以查看与文件权限相关的信息：

```shell
$ ls -l
drwxr-xr-x  2 lizhen  staff  68 10 10 19:14 foo
-rw-r--r--  1 lizhen  staff   0 10 10 19:14 test.txt
lrwxr-xr-x  1 lizhen  staff  62  7 10 10:01 subl -> /Applications/Sublime Text.app/Contents/SharedSupport/bin/subl
```

其中第一个字符表示文件类型：d 表示文件为一个目录，- 表示文件为普通文件，l 表示链接， b 表示设备文件。

接下来的字符中，以三个为一组，且均为 r(read)、 w(write)、 x(execute) 三个参数的组合，首先三个字符表示文件所有者权限，后面三个字符表示用户组权限，最后三个表示其他人对文件的权限。这三个权限的位置不会改变，如果没有权限，就会出现减号[ - ]。

<img src="/assets/img/linux_permission.png" alt="linux_permission">

后面的字段分别代表：硬链接个数，所有者，所在组，文件或者目录大小，最后访问/修改时间，文件或者目录名。

<!--more-->

## 更改文件属性

chgrp：改变文件所属群组 change group
chown：改变文件拥有者 change owner
chmod：改变文件的权限 change mod

### chgrp

首先使用 groups 命令查看当前用户在哪些分组中，然后使用 chgrp 命令改变文件所属用户组

```shell
$ chgrp -R admin foo
$ ls -l 
drwxr-xr-x  2 lizhen  admin  68 10 10 19:14 foo
```

-R 表示递归更改文件属组，就是在更改某个目录文件的属组时，如果加上 -R 参数，那么该目录下的所有文件的属组都会更改。可以通过 `/etc/group` 查看当前系统所有的分组。

可以看到文件分组由 staff 变成了 admin。

### chown 

语法

```shell
chown [–R] 属主名 文件名
chown [-R] 属主名：属组名 文件名
```

chown 可以更改文件的 owner，也可以同时更改文件属组。假如当前系统中有一个名为 test 的用户。

```shell
$ sudo chown -R test foo
$ ls -l
drwxr-xr-x  2 test   admin  68 10 10 19:14 foo
```

此时 foo 的 owner 变成了 test。可以通过 `/etc/passwd` 文件查看当前系统所有的用户。

chown 还可以用户修改文件所在的分组。

```shell
$ sudo chown [-R] lizhen:staff foo
$ ls -l
drwxr-xr-x  2 lizhen  staff  68 10 10 19:14 foo
```

文件属性又变回去了。

### chmod

chmod 用来更改文件属性，权限可以使用符号或数字来表示。

使用符号表示权限：

[ + ]	为文件或目录增加权限
[ - ]	删除文件或目录的权限
[ = ]	设置指定的权限

通过使用 u(owner)、g(group)、o(other) 来代表三种身份的权限，此外 a 代表 all，即全部身份。

语法

```shell
chmod u/g/o/a +/-/= r/w/x filename
```

```shell
$ ls -l test.txt
-rw-r--r--  1 lizhen  staff  0 10 10 20:33 test.txt

## 修改 owner 权限增加 execute，group 和 others 减少 read
$ chmod u+x,g-r,o-r test.txt 

$ ls -l test.txt
-rwx------  1 lizhen  staff  0 10 10 20:33 test.txt

## 修改 owner 权限为 rw，group 和 others 为 r
$ chmod u=rw,g=r,o=r test.txt 

$ ls -l test.txt
-rw-r--r--  1 lizhen  staff  0 10 10 20:33 test.txt

## 增加所有用户的执行权限
$ chmod a+x test.txt

$ ls -l test.txt
-rwxr-xr-x  1 lizhen  staff  0 10 10 20:33 test.txt
```


使用数字改变权限：

x: 1
w: 2
r: 4

所以权限 `rwx` 就等于 `4 + 2 + 1 = 7`，也就是 `chmod a=rwx file` 相当于 `chmod 777 file`。

-rw——- (600) 只有所有者才有读和写的权限
-rw-r–r– (644) 只有所有者才有读和写的权限，组群和其他人只有读的权限
-rwx—— (700) 只有所有者才有读，写，执行的权限
-rwxr-xr-x (755) 只有所有者才有读，写，执行的权限，组群和其他人只有读和执行的权限
-rwx–x–x (711) 只有所有者才有读，写，执行的权限，组群和其他人只有执行的权限
-rw-rw-rw- (666) 每个人都有读写的权限
-rwxrwxrwx (777) 每个人都有读写和执行的权限

```shell
$ chmod 711 test.txt 
$ ls -l test.txt 
-rwx--x--x  1 lizhen  staff  0 10 10 20:33 test.txt
```


