---
title: API 网关 Kong
date: 2018-10-24 21:51:14
categories: 网络
tags:
- Gateway
- nginx
- lua
---

## [Kong](https://konghq.com/) 简介

Kong 是一款基于 OpenResty 的 API 网关平台，在客户端和（微）服务之间转发 API 通信。Kong 通过插件的方式扩展自己的功能，其中包括身份验证、安全控制、流量控制、熔断机制、日志、黑名单、API 分发等等众多功能。下图是官网给出的传统项目架构和使用 Kong 的架构：

<img src="/assets/img/legacy-architecture.svg" alt="legacy-architecture" style="float: left;width: 48%;">
<img src="/assets/img/legacy-architecture.svg" alt="legacy-architecture" style="float: right;width: 48%;">

Next-Generation API Platform for Modern Architectures。

<!--more-->

可以看到，使用 Kong 之后，内部服务开发者只需要 focus 具体业务的实现，网关层提供 API 分发、管理、维护等功能，开发者只需要简单的配置就可以把自己开发的服务发布出去，同时置于网关的保护之下。

### [OpenResty](https://openresty.org/cn/) 简介

OpenResty® 是一个基于 Nginx 与 Lua 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。


### Kong 三大组件

- Kong Server ：基于 nginx 的服务器，用来接收 API 请求。
- Apache Cassandra/[PostgreSQL](https://www.postgresql.org/)：用来存储操作数据，本文以 PostgreSQL 为例进行讲解。
- [Kong dashboard](https://github.com/PGBI/kong-dashboard)：UI 管理工具。


### Kong 特性

- 可扩展：通过简单地添加机器来进行水平扩展，可以用较低的负载处理任何请求。
- 模块化：通过 RESTful API 安装和配置插件。
- 在任何基础设施上运行：Kong 可以部署在云端、机房、或者混合环境，包括单个或多个数据中心。

## 安装以及使用

Kong 可以安装运行在大部分 Linux 分布式平台和 macOS 上。全部安装方式请查看[安装 Kong 社区版](https://konghq.com/install/)。

### macOS Homebrew

(1) 安装 Kong

```sh
$ brew tap kong/kong
$ brew install kong
```

(2) 准备数据库

安装 PostgresSQL，在 Kong 启动之前指定数据库和用户。

```sh
$ CREATE USER kong; CREATE DATABASE kong OWNER kong;
```

由于对 Postgres 并不熟悉，我使用 GUI 工具 pgAdmin4 完成 User 和 Database 的创建。


(3) 准备 kong 配置文件

kong 默认使用 `/etc/kong/kong.conf` 作为启动的配置文件，因此我们在 `/etc/kong/` 目录下创建 kong.conf 文件，内容如下：

```sh
database = postgres
pg_port = 5432
pg_user = kong
pg_password = **** # 如果你刚才设置密码的话
```

全部 kong 的配置文件你可以查看 [kong.conf.default](https://github.com/Kong/kong/blob/master/kong.conf.default)。

(4) 启动 kong

```sh
$ kong migrations up
$ kong start
```

这个时候 kong 就启动起来了。然后我们可以通过下面的命令测试：

```sh
$ curl -i http://localhost:8001/
```

(5) 更多 kong 的命令

```sh
$ kong check /etc/kong/kong.conf # 检验 kong 配置文件是否正确
$ kong migrations up [-c /etc/kong/kong.conf] # 通过配置文件准备数据存储
$ kong start [-c /etc/kong/kong.conf] # 启动 kong
$ kong stop 
$ kong reload
```

(6) kong 启动后监听了 4 个端口

- 8000: Kong 监听来自客户端的 HTTP 请求的，并将此请求转发到上游服务。  
- 8443: 与 8000 端口相同，不过只监听 HTTPS 请求。
- 8001: 管理员对 Kong 进行配置管理的端口。
- 8444: 管理员监听 HTTPS 请求的端口。

### Docker

(1) 创建一个名为 kong-net 的 network

```sh
$ docker network create kong-net                
```

(2) 启动数据库（PostgreSQL）

```sh
$ docker run -d --name kong-database \
              --network=kong-net \
              -p 5432:5432 \
              -e "POSTGRES_USER=kong" \
              -e "POSTGRES_DB=kong" \
              postgres:9.6
```

这个时候命令行会显示 `Unable to find image 'postgres:9.6' locally`，然后会自动帮我买下载 postgres 的 image。


(3) 准备数据库

```sh
$ docker run --rm \
    --network=kong-net \
    -e "KONG_DATABASE=postgres" \
    -e "KONG_PG_HOST=kong-database" \
    -e "KONG_CASSANDRA_CONTACT_POINTS=kong-database" \
    kong:latest kong migrations up
```

(4) 启动 Kong

```sh
$ docker run -d --name kong \
    --network=kong-net \
    -e "KONG_DATABASE=postgres" \
    -e "KONG_PG_HOST=kong-database" \
    -e "KONG_CASSANDRA_CONTACT_POINTS=kong-database" \
    -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
    -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
    -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
    -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
    -e "KONG_ADMIN_LISTEN=0.0.0.0:8001, 0.0.0.0:8444 ssl" \
    -p 8000:8000 \
    -p 8443:8443 \
    -p 8001:8001 \
    -p 8444:8444 \
    kong:latest
```

(5) 使用 Kong

```sh
$ curl -i http://localhost:8001/
```

更详细的内容可以查看 [5 分钟快速开始](https://docs.konghq.com/0.14.x/getting-started/quickstart/)


### kong-dashboard

Kong dashboard 是一个基于 node 实现的管理 Kong 网关设置的 GUI 工具。

使用 npm：

```sh
# Install Kong Dashboard
npm install -g kong-dashboard

# Start Kong Dashboard
kong-dashboard start --kong-url http://localhost:8001

# Start Kong Dashboard on a custom port
kong-dashboard start \
  --kong-url http://localhost:8001 \
  --port [port]

# Start Kong Dashboard with basic auth
kong-dashboard start \
  --kong-url http://localhost:8001 \
  --basic-auth user1=password1 user2=password2

# See full list of start options
kong-dashboard start --help
```

使用 Docker：

```sh
# Start Kong Dashboard
docker run --rm -p 8080:8080 pgbi/kong-dashboard start --kong-url http://kong:8001

# Start Kong Dashboard on a custom port
docker run --rm -p [port]:8080 pgbi/kong-dashboard start --kong-url http://kong:8001

# Start Kong Dashboard with basic auth
docker run --rm -p 8080:8080 pgbi/kong-dashboard start \
  --kong-url http://kong:8001
  --basic-auth user1=password1 user2=password2

# See full list of start options
docker run --rm -p 8080:8080 pgbi/kong-dashboard start --help
```

## Kong 使用

本质上 Kong 是作用于请求和响应之间的一层代理，我们可以通过 RESTful 的形式管理 API。

### 添加一个 API

使用 curl 命令行：

```sh
$ curl -i -X POST \
  --url http://localhost:8001/apis/ \
  --data 'name=example-api' \
  --data 'hosts=example.com' \
  --data 'upstream_url=https://lz5z.com'
```

或者使用 `kong-dashboard`，在 http://localhost:8080/#!/apis 编辑查看：

<img src="/assets/img/kong-dashboard.png" alt="kong-dashboard">

这时，Kong 已经做好了对 HOST 是 example.com 的 api 的代理请求，并且将其代理到 https://lz5z.com 上。

```sh
$ curl -i -X GET \
  --url http://localhost:8000/ \
  --header 'Host: example.com'
``` 

## 总结

以上只是 Kong 简单的安装和工具的使用，由于之前对 docker、PostgresSQL 等周边工具并不熟悉，所以学习起来需要扩展的东西比较多，暂时先写到这里吧。关于 Kong 插件的使用已经编写，用户操作、授权、负载均衡、熔断等信息，这里先埋坑，后面有时间再补上吧。












