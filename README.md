# platform20200916

## 程序描述

### 需求概述
支持XML文件或restful API返回的JSON数据格式，根据需求方的数据结构，采用动态数据库建模技术写入到数据库中。入库后需要按指定的格式Soup，将数据发送给Web Service以同步给Microsoft Revision系统。

### 特点
1. 由于业务需要，字段和表的数量都十分庞大。每次数据传输都很可能需要新增若干张表（有可能几十张），且代码发布后不能再对数据库做任何操作，也就是说无法人为增加数据库表。因此在SQLAlchemy框架上，实现了一个数据结构动态建模的方式。
2. 数据量很大，单脚本的执行时间略长。在数据处理瓶颈处，使用有序多线程的方式来提高效率。
3. 数据操作敏感性很高，人工排查难度大。在开发时使用了测试驱动开发的方法，提高了软件的质量，大量节约了调试和修改的时间成本。
4. 由于数据来源存在时区，针对时区转换进行了额外的处理。
5. 同步到Revision系统的Web Service采用了Microsoft Windows ntlm认证，需要做额外的工作进行适配。
6. 需要开放一个restful API，供其他语言进行手动调用。

### 技术栈
Python 3.7
SQLAlchemy
Flask
Flask_SQLAlchemy
pytest
xmltodict
requests
requests_ntlm
pyodbc
pycrptodome
Microsoft SQLServer
