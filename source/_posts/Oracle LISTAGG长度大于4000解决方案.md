---
title: Oracle LISTAGG长度大于4000解决方案
date: 2016-10-24 10:11:35
tags: 
- Oracle
- listagg
categories: 杂记
---

# 背景

<img src="http://i1.piimg.com/567571/8338c9170ee94051.jpg" width="50%">

公司业务网站上有一个可以 Free input 的 textarea，长度没有限制，可是存到 DB 的时候 Oracle varchar2 最大长度限制是4000，于是聪明的同事使用分而治之的方式解决了这个问题。如果长度大于某个值就新建一个 record 存储，然后使用 seq_num 记录表示其顺序。
<!-- more -->
# listagg

上周做 report 的时候需要把这个 column 的数据生成给别的部门的同事，于是首先想到的是用 Oracle 的 listagg 函数。

![listagg](http://p1.bqimg.com/567571/d767c741445ffd2e.gif)

listagg 可以将多行合并成为一行。
具体使用如下：

比如有这样一张表 Employee

| employee_id | department_id | first_name | last_name |
|:-:| :-: | :-:| :-: |
| 1 | 1 | Leo | Li |
| 2 | 1 | Jack | Li |
| 3 | 1 | Lucy | Li |

需要得到所有 "last_name" 为Li的 "first_name"， 并且用"; "分隔，显示效果如下:

| department_id | first_names | last_name |
| :-:| :-: | :-: |
| 1 | Leo; Jack; Lucy | Li |

于是可以使用 sql:

```sql
SELECT MAX(department_id) department_id,
  listagg(first_name, '; ') within GROUP (
ORDER BY employee_id) first_names,
  MAX(last_name) last_name
FROM Employee
WHERE department_id = 1
AND last_name       = 'Li';
```
或者

```sql
SELECT department_id department_id,
       LISTAGG(first_name, '; ')
      WITHIN GROUP (ORDER BY employee_id) first_names,
      last_name
FROM employee
GROUP BY department_id,last_name
ORDER BY department_id;
```

# 遇到的问题

由于该 textare 是 Free Input 的，你不能确定用户到底输入了多少个字符，于是我第一次尝试使用 listagg 的时候发现超过 varchar2 的最大长度4000了。怎么办呢？首先想到的是截取字符串，如果超过4k就截取前面4k的部分：

```sql
SELECT SUBSTR(LISTAGG(**, '; ') WITHIN GROUP(ORDER BY **), 0, 3999)...
```
然并暖（:-D），因为在超过4k长度的那部分，使用 listagg 就已经报错了，并不是 select 的时候报错的

于是 Google 之，输入关键词 **listagg 4000 characters**，在 Oracle 社区发现已经有大神给出了[解决方案](https://community.oracle.com/thread/2548234)。

# 解决方案

```SQL 
SQL> set long 10000
SQL> select listagg(id, ',') within group (order by id)
  2    from (select level as id from dual connect by level < 1050)
  3  /
  from (select level as id from dual connect by level < 1050)
                                *
ERROR at line 2:
ORA-01489: result of string concatenation is too long
```

```SQL
SQL> select rtrim(xmlagg(xmlelement(e,id,',').extract('//text()') order by id).GetClobVal(),',')
  2    from (select level as id from dual connect by level < 1050)
  3  /

RTRIM(XMLAGG(XMLELEMENT(E,ID,',').EXTRACT('//TEXT()')ORDERBYID).GETCLOBVAL(),','
--------------------------------------------------------------------------------
1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...
```

将 level 参数不断扩大发现均能查到结果，不确定最大支持多长的字符，不过20000也能查到结果，相信能满足大部分需求。

# 总结

如果使用 listagg 出现 ***result of string concatenation is too long*** 的错误时候，可以尝试使用 XMLAGG 代替。