---
title: MongoDB3.2存储策略
date: 2016-9-2 16:46:42
tags: 
- MongDB
- 配置文件
categories: MongoDB
---
# MongoDB存储策略
---

MongoDB在3.2 版本更新后，正式将WiredTiger引擎设为默认引擎。

本文是MongoDB存储策略的一个简单翻译加讲解，存储引擎部分只介绍 **wiredTiger**，只有企业版支持的inMemory和落后于wiredTiger的mmapv1你可以参考[官方文档](https://docs.mongodb.com/manual/reference/configuration-options/)。
官方给出[存储策略](https://docs.mongodb.com/manual/reference/configuration-options/)如下：
<!-- more -->
```
storage:
   dbPath: <string>
   indexBuildRetry: <boolean>
   repairPath: <string>
   journal:
      enabled: <boolean>
      commitIntervalMs: <num>
   directoryPerDB: <boolean>
   syncPeriodSecs: <int>
   engine: <string>
   mmapv1:
      preallocDataFiles: <boolean>
      nsSize: <int>
      quota:
         enforced: <boolean>
         maxFilesPerDB: <int>
      smallFiles: <boolean>
      journal:
         debugFlags: <int>
         commitIntervalMs: <num>
   wiredTiger:
      engineConfig:
         cacheSizeGB: <number>
         journalCompressor: <string>
         directoryForIndexes: <boolean>
      collectionConfig:
         blockCompressor: <string>
      indexConfig:
         prefixCompression: <boolean>
   inMemory:
      engineConfig:
         inMemorySizeGB: <number>
```
## storage.dbPath

类型： 字符串
默认值: linux/OSX: /data/db; windows: \data\db

> The directory where the mongod instance stores its data.

> If you installed MongoDB using a package management system, check the /etc/mongod.conf file provided by your packages to see the directory is specified.

> The storage.dbPath setting is available only for mongod.

> The Linux package init scripts do not expect storage.dbPath to change from the defaults. If you use the Linux packages and change storage.dbPath, you will have to use your own init scripts and disable the built-in scripts.

**dbPath是MongoDB存储数据的磁盘位置**

## storage.indexBuildRetry

类型： boolean
默认值： True

> Specifies whether mongod rebuilds incomplete indexes on the next start up. This applies in cases where mongod restarts after it has shut down or stopped in the middle of an index build. In such cases, mongod always removes any incomplete indexes, and then, by default, attempts to rebuild them. To stop mongod from rebuilding indexes, set this option to false.

>The storage.indexBuildRetry setting is available only for mongod.
>Not available for mongod instances that use the in-memory storage engine.

**这个参数指的是：数据库在索引建立过程中停止，重启后是否重新建立索引。如果索引构建失败，mongod重启后将会删除尚未完成的索引，但是否重建由此参数决定。 设置这个参数的目的是： 如果你创建index的时候，MongoDB突然关闭（可能是因为意外，也可能是你不想建了手动关闭），这时候MongoDB会帮你把未完成的index删除，如果你不想启动MongoDB后重新创建这个index，可以将参数设置为false。虽然创建后也可以删除，但是毕竟数据量大了，创建index会耗费大量资源，对产品的影响不容小觑。**

**后面两句的意思是这个参数只对mongod进程有效，使用inMemory存储引擎无效。后面一样就不翻译了。**

## storage.repairPath

类型： 字符串
默认值： dbPath下面 ```A _tmp_repairDatabase_<num>```

> The working directory that MongoDB will use during the --repair operation. When --repair completes, the storage.repairPath directory is empty, and dbPath contains the repaired files.

> The storage.repairPath setting is available only for mongod.
> Not available for mongod instances that use the in-memory storage engine.

**这个参数是设置MongoDB修复的时候生成的临时文件的位置，配合```--repair```参数使用，当repair完成后，会把repairPath目录清空。**


## storage.journal.enabled

类型： boolean
默认值： 64-bit 操作系统为True，32-bit 为False


> Enable or disable the durability journal to ensure data files remain valid and recoverable. This option applies only when you specify the --dbpath option. The mongod enables journaling by default on 64-bit builds of versions after 2.0.

> The storage.journal.enabled setting is available only for mongod.
Not available for mongod instances that use the in-memory storage engine.

**开启journal日志用于保证MongoDB数据有效性和故障恢复，这个建议开启。**



## storage.journal.commitIntervalMs
类型：number
默认值： MMAPv1：30； WiredTiger：100

> The maximum amount of time in milliseconds that the mongod process allows between journal operations. Values can range from 1 to 500 milliseconds. Lower values increase the durability of the journal, at the expense of disk performance. The default journal commit interval is 100 milliseconds.

> On MMAPv1, if the journal is on a different block device (e.g. physical volume, RAID device, or LVM volume) than the data files, the default journal commit interval is 30 milliseconds. Additionally, on MMAPv1, when a write operation with j:true is pending, mongod will reduce commitIntervalMs to a third of the set value.

> On WiredTiger, the default journal commit interval is 100 milliseconds. Additionally, a write with j:true will cause an immediate sync of the journal.

> The storage.journal.commitIntervalMs setting is available only for mongod.
Not available for mongod instances that use the in-memory storage engine.

**这个参数指mongod进程提交journal日志的时间间隔，阈值为1-500毫秒，这个值越小，数据丢失的可能性越低，磁盘消耗越大，性能越低。使用MMAPv1时默认值为30ms，使用WiredTiger时，默认值为100ms。如果在客户端进行写操作的时候，希望立即同步，可以传递参数 ```j:true```, 写操作会立即fsync到磁盘。**

## storage.directoryPerDB

类型：boolean
默认值：False

> When true, MongoDB uses a separate directory to store data for each database. The directories are under the storage.dbPath directory, and each subdirectory name corresponds to the database name.

**如果为真的话，会将不同DB的数据存储在不同的目录中，路径为storage.dbPath的子目录，目录名为DB的名称。**


## storage.syncPeriodSecs
类型： number
默认值： 60
> The amount of time that can pass before MongoDB flushes data to the data files via an fsync operation.

> Do not set this value on production systems. In almost every situation, you should use the default setting.

> WARNING:
> If you set storage.syncPeriodSecs to 0, MongoDB will not sync the memory mapped files to disk.

>The mongod process writes data very quickly to the journal and lazily to the data files. storage.syncPeriodSecs has no effect on the journal files or journaling.

> The serverStatus command reports the background flush thread’s status via the backgroundFlushing field.

**MongoDB 通过fsync操作将数据flush到磁盘，这个参数指同步的时间间隔。默认值是60秒。官方给出的建议是在产品环境中，不要设置这个参数的值，使用默认值最好了。
如果你把参数值设为0，MongoDB就不会把内存中的数据同步到磁盘了。**

**mongod进程将变更的数据立马写入journal，然后过一段时间再写入磁盘，可以提高磁盘效率。这个参数对journal文件存储没有影响。**

## storage.engine
默认值：wiredTiger

MongoDB一共有三种存储引擎： mmapv1, wiredTiger, inMemory。 inMemory只有在MongoDB企业版中才能使用。

> If you attempt to start a mongod with a storage.dbPath that contains data files produced by a storage engine other than the one specified by storage.engine, mongod will refuse to start.

**启动MongoDB的时候，可以在dbPath中指定存储引擎，如果数据库已经有数据文件，则MongDB会根据文件判断存储引擎的类型。如果启动的时候指定的存储引擎与已有的存储引擎不一致，会导致启动失败。**

# wiredTiger引擎选项

## storage.wiredTiger.engineConfig.cacheSizeGB

> The maximum size of the internal cache that WiredTiger will use for all data.

> With WiredTiger, MongoDB utilizes both the WiredTiger internal cache and the filesystem cache.

> Changed in version 3.2: Starting in MongoDB 3.2, the WiredTiger internal cache, by default, will use the larger of either:

1. 60% of RAM minus 1 GB, or
2. 1 GB.

> For systems with up to 10 GB of RAM, the new default setting is less than or equal to the 3.0 default setting (For MongoDB 3.0, the WiredTiger internal cache uses either 1 GB or half of the installed physical RAM, whichever is larger).

> For systems with more than 10 GB of RAM, the new default setting is greater than the 3.0 setting.

**这个参数限制WiredTiger使用的最大内部缓存的大小。通过WiredTiger，MongoDB充分利用了WiredTiger的内部缓存和文件系统的缓存。这个默认值是MongoDB计算出来了，如果你的内存的比较大，会使用（60%的内存 - 1G，或者1G， 以数值比较大的为准），也就是至少1G。**

**在MongoDB3.0中，WiredTiger缓存使用1G或者安装物理内存的一半，以较大者为准。所以如果你的内存小于10G，3.2的默认值为小于或等于3.0的默认值。如果你的内存大于10G，3.2版本将会使用比3.0版本更大的内存。**

> Via the filesystem cache, MongoDB automatically uses all free memory that is not used by the WiredTiger cache or by other processes. Data in the filesystem cache is compressed.

> Avoid increasing the WiredTiger internal cache size above its default value.

**通过文件系统缓存，MongoDB自动使用除了WiredTiger和其他进程使用的内存以外的全部内存，（看到这里我顿时觉得说MongoDB是纯内存数据库一点也不为过，说它是贵族数据库也毫不夸张）。也就是说，只要你数据量比较大，不管怎么样，它都会把你内存吃光，要么是WiredTiger存储引擎使用，要么是操作系统的文件系统（文件系统也是为MongoDB服务）。不过数据在文件系统里面是经过压缩的。感觉MongoDB为了快无所不尽其极啊。**

**官方建议避免设置WiredTiger缓存大于其默认值。**

> NOTE
The storage.wiredTiger.engineConfig.cacheSizeGB limits the size of the WiredTiger internal cache. The operating system will use the available free memory for filesystem cache, which allows the compressed MongoDB data files to stay in memory. In addition, the operating system will use any free RAM to buffer file system blocks and file system cache.

**这里是说这个参数限制了WiredTiger内部缓存的大小，操作系统会利用剩余的内存作文件系统缓存用了存储压缩过的MongoDB数据文件。此外，操作系统将使用任何可用的内存缓存文件系统块和文件缓存。不知道官方文档为什么要再啰嗦一遍，不是我的锅。**

> The default WiredTiger internal cache size value assumes that there is a single mongod instance per machine. If a single machine contains multiple MongoDB instances, then you should decrease the setting to accommodate the other mongod instances.

**刚才所说的默认值是假设每台电脑上只有一个mongod实例，如果你有部署多个MongDB实例，请合理配置参数。**


> If you run mongod in a container (e.g. lxc, cgroups, Docker, etc.) that does not have access to all of the RAM available in a system, you must set storage.wiredTiger.engineConfig.cacheSizeGB to a value less than the amount of RAM available in the container. The exact amount depends on the other processes running in the container.

**如果你把mongod运行在一个容器中，比如现在最热门的Docker，因为容器并不能获取系统中全部内存，所以你要把这个参数设置的小于容器所拥有的内存，当然还要考虑容器中其它的进程。**

## storage.wiredTiger.engineConfig.journalCompressor

默认值： snappy

**这个参数是指wiredTiger使用的压缩算法，如果你对此没有了解的话，就不要动了。有三个值可选：none；snappy；zlib。第一个表示不压缩。**


## storage.wiredTiger.engineConfig.directoryForIndexes

类型： boolean
默认值： false

> When storage.wiredTiger.engineConfig.directoryForIndexes is true, mongod stores indexes and collections in separate subdirectories under the data (i.e. storage.dbPath) directory. Specifically, mongod stores the indexes in a subdirectory named index and the collection data in a subdirectory named collection.

> By using a symbolic link, you can specify a different location for the indexes. Specifically, when mongod instance is not running, move the index subdirectory to the destination and create a symbolic link named index under the data directory to the new destination.

**是否将索引和collections数据分别存储在storage.dbPath单独的目录中。即index数据保存“index”子目录，collections数据保存在“collection”子目录。默认值为false，仅对mongod有效。**


## storage.wiredTiger.collectionConfig.blockCompressor
默认值： snappy
> The default type of compression to use to compress collection data. You can override this on a per-collection basis when creating collections.

> storage.wiredTiger.collectionConfig.blockCompressor affects all collections created. If you change the value of storage.wiredTiger.collectionConfig.blockCompressor on an existing MongoDB deployment, all new collections will use the specified compressor. Existing collections will continue to use the compressor specified when they were created, or the default compressor at that time.

**collection数据压缩算法，可选值“none”、“snappy”、“zlib”。你可以在创建collection时可以指定值，以覆盖此配置项。如果mongod中已经存在数据，修改此值不会带来问题，旧数据仍然使用原来的算法解压，新数据文件将会采用新的解压缩算法。**


## storage.wiredTiger.indexConfig.prefixCompression
默认值：true

> Enables or disables prefix compression for index data.

> Specify true for storage.wiredTiger.indexConfig.prefixCompression to enable prefix compression for index data, or false to disable prefix compression for index data.

> The storage.wiredTiger.indexConfig.prefixCompression setting affects all indexes created. If you change the value of storage.wiredTiger.indexConfig.prefixCompression on an existing MongoDB deployment, all new indexes will use prefix compression. Existing indexes are not affected.

**是否对索引数据使用“前缀压缩”（prefix compression，一种算法）。前缀压缩，对那些经过排序的值存储，有很大帮助，可以有效的减少索引数据的内存使用量。默认值为true。如果你在已经存在数据的MOngoDB数据库中修改这个值，新创建的数据都会受到影响，而已有的index不会受到影响。	**

---

