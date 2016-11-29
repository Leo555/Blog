---
title: Python 环境搭建
date: 2016-07-01 22:38:42
tags: 
- Python
categories: Python
---
<img src="/assets/img/Python_logo.png" alt="我是一只的图片" width="20%">
# Python 环境搭建
---
因为工作的需要，要运行一个Py脚本，电脑里的只有一个原生的py27，去年安装的，于是就从零开始搭建py环境。

<!-- more -->
## 安装 
首先去[Python官网][2]下载安装最新版的py，这里我选择的是最新的Python3.5.2, 建议使用Python3.4以后的版本，因为3.4之后，Python自带了Pip。 3.5.2是目前最新的有64位的Python版本，选择最容易安装的[Windows x86-64 executable installer][3]下载。

下载完成后双击 *python-3.5.2-amd64.exe* 进行安装。
默认没有选择 *Add Pyhon 3.5 to PATH*  这里**手动勾选**。选择自定义安装，并且将安装路径设为 C:\Python35。

如果没有勾选的话也没有关系，安装完成以后将 *C:\Python35* 和 *C:\Python35\Scripts* 加入到环境变量即可。
C:\Python35\Scripts 里面是pip 和easy_install的主程序，加入环境变量之后就可以轻松使用pip安装外部依赖了。

安装之后打开环境变量，发现Python的环境变量被放在最前面，所以后面之前安装的Python27就不起作用了，作为处女座怎么能忍受没有用的东西存在呢，于是删除Python27的环境变量。

打开命令行工具cmder（如果之前已经打开，记得重启刷新Windows环境变量），输入`python`

```
$ python
Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
可以看到强大的64 bit Python就安装好了。

## pip 
如果你前面跟我的安装方式一样的话，pip和setuptools也都已经默认安装到电脑上了，而且可以随意使用。
cmder输入 `pip list`, 如果出现下面就直接去3。
```
$ pip list
pip (8.1.1)
setuptools (20.10.1)
```
当然，有的小伙伴就是不喜欢按照套路出牌，如果输入`pip list` 出现下面的情况的话，就需要你手动安装pip了。
```
The term 'pip' is not recognized as the name of a cmdlet...
```
之前用老版本的Python的时候，pip和setuptools也是需要手动安装的，安装方式：

首先检查刚才下的Python安装文件里面有没有pip.exe，我的文件所在位置是C:\Python35\Scripts， 把它加入环境变量。
此时再试下命令 `$pip list`, 有反应就可以直接去3。

如果没有的话，先去下载[setuptools][4]，安装，再下载[pip][5]，安装。
安装pip和setuptools的方式一样：cd 到文件路径(可以看到setup.py文件)，输入命令
```
$ python setup.py install
```
然后再试下命令 `$pip list`。
## pip安装外部依赖
pip安装成功了，我们用它安装一个数据分析的Library [Pandas][6]
```
$ pip install pandas
```
之后就可以开始快乐的Python之旅了。

---


  [1]: https://www.python.org/static/img/python-logo.png
  [2]: https://www.python.org/downloads/
  [3]: https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe
  [4]: https://pypi.python.org/packages/89/86/ab1bf3a2550dcf43e2f5e77d72e9edb53dc701e78cbf07ef88ff8a08333e/setuptools-23.1.0.zip#md5=6125a9e3baeaae26f72b257a5defdc62
  [5]: https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz#md5=87083c0b9867963b29f7aba3613e8f4a
  [6]: http://pandas.pydata.org/