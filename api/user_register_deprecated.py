# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import sys
from datetime import datetime
from os import path

from fastapi import HTTPException


sys.path.append("..")
#将当前文件所在目录的上上级目录添加到系统的搜索路径中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#解决：  from model.users import User ModuleNotFoundError: No module named 'model'的问题
#将当前文件所在目录的上级目录添加到系统的搜索路径中
from model.response_model.user_app_info import UserInfo
from model.request_model.users import UserBase
from utils.hash_tool import safe_password
from utils.mysql_tool_deprecated import db
#from utils.database import db

from config.config import app


# app = FastAPI()

"""
设计用户注册接口：
    1、host:127.0.0.1
    2、port：8001
    3、参数：username,password,email其余选填
    4、响应结果：响应成功，数据库新增一条数据，返回用户信息；响应失败，提示注册失败
"""
@app.post('/user/register',response_model=UserInfo)
async def user_register(user:UserBase):
    now = datetime.now()
    timestamp = int(now.timestamp())
    #注册时邮箱不允许重复，所以注册时先查询邮箱是否已经注册
    if user.email:
        sql_confirm = "select email from users where email = '{}'".format(user.email)
        print(sql_confirm)
        result_email = db.select_data(sql_confirm)
        print("查询到email：{}".format(result_email))
        if result_email :
            #数据库内已经有邮箱，说明此邮箱已经注册,直接抛出接口异常
           raise HTTPException(status_code=4003,detail='This email is already exist')
        else:
            # 该邮箱为注册过，直接给用户密码加密，插入数据库中
            password = safe_password(user.password, user.username)
            #print(password)
            sql_insert = ("insert into users(password,gender,username,email,createTime)"
                          "values('{}','{}','{}','{}','{}')").format(password,user.gender,user.username,user.email,timestamp)
            print(sql_insert)
            db.execute_data(sql_insert)
    elif user.gender!='0' or user.gender!='1':
        raise HTTPException(status_code=4002,detail='Incorrect format')
    return user
