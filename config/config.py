# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
from fastapi import FastAPI

#mysql配置
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_username = 'root'
mysql_password = '123456xj'
mysql_db = 'FastApiData'

#密码加密key
Password_Key = 'fastapiDemo'

#接口鉴权密钥
SECRET_KEY = '42adfcd782c3c71af55870dae7231e1e5e24c80751a5cfe6e4bfastapiDemo'

#加密算法：HS256
ALGORITHM = 'HS256'
#Token过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 600

#redis配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWD = "123456xj"
app = FastAPI()
