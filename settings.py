#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import config


class Base:
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 200
    SQLALCHEMY_POOL_RECYCLE = -1
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {"isolation_level": "AUTOCOMMIT"}
    # 数据库引擎
    DATABASE_ENGINE = "mysql+pymysql"
    # 数据库端口
    DATABASE_PORT = 3306
    # 连接字符串后缀
    DATABASE_SUFFIX = ""
    # 多库连接绑定
    SQLALCHEMY_BINDS = {}
    # 任务扫描时间冗余（分钟）
    TASK_SCAN_INTERVAL = 5
    # 是否开启日志（1=开启，0=不开启）
    LOG_ON = 1
    # 非CV任务是否开启多线程
    THREADING = 1


class Development(Base):
    ENV = "Development"
    DATABASE_ENGINE = "mysql+pymysql"
    DATABASE_PORT = 3306
    DATABASE_SUFFIX = "charset=utf8"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/dms_interface?charset=utf8"


# mac下的测试环境
class Test(Base):
    ENV = "Test"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:msSqlServer2020@127.0.0.1:1433/dms_interface?driver=ODBC+Driver+17+for+SQL+Server"
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://dms_user:dms_pwd@127.0.0.1:1433/dms_interface?driver=ODBC+Driver+17+for+SQL+Server"
    DATABASE_ENGINE = "mssql+pyodbc"
    DATABASE_PORT = 1433
    DATABASE_SUFFIX = "driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_ECHO = False
    TASK_SCAN_INTERVAL = 10


# windows下的测试环境
class TestWin(Base):
    ENV = "TestWin"
    DATABASE_ENGINE = "mssql+pyodbc"
    DATABASE_PORT = 1433
    DATABASE_SUFFIX = "driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://NavDBUser:Hytc_1qaz@WSX@62.234.26.35:1433/PH_DMSInterface?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_ECHO = False


# 生产环境
class Production(Base):
    ENV = "production"
    DATABASE_ENGINE = "mssql+pyodbc"
    DATABASE_PORT = 1433
    DATABASE_SUFFIX = "driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://NavDBUser:Hytc_1qaz@WSX@62.234.26.35:1433/PH_DMSInterface?driver=ODBC+Driver+17+for+SQL+Server"
    # 关闭sql回显
    SQLALCHEMY_ECHO = False
    # 任务扫描时间冗余（分钟）
    TASK_SCAN_INTERVAL = 10
    # 是否开启日志（1=开启，0=不开启）
    LOG_ON = 1
    # 非CV任务是否开启多线程
    THREADING = 1
