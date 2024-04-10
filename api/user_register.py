# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import sys
from datetime import datetime
from os import path

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
#将当前文件所在目录的上上级目录添加到系统的搜索路径中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#解决：  from model.users import User ModuleNotFoundError: No module named 'model'的问题
#将当前文件所在目录的上级目录添加到系统的搜索路径中
from model.request_model.users import UserCreate
from model.response_model import user_app_info
from utils.hash_tool import safe_password
from utils.database import db
from model.database_model import db_model
from config.config import app
from common.crud import create_user,get_userInDB_email


# app = FastAPI()

"""
设计用户注册接口：
    1、host:127.0.0.1
    2、port：8001
    3、参数：username,password,email其余选填
    4、响应结果：响应成功，数据库新增一条数据，返回用户信息；响应失败，提示注册失败
"""
@app.post('/user/register',response_model=user_app_info.UserInfo)
async def user_register(user_base: UserCreate,db: Session = Depends(db.get_db)):
    if get_userInDB_email(db,user_base.email):
        raise HTTPException(status_code=4003, detail='This email is already exist')
    else:
        now = datetime.now()
        timestamp = int(now.timestamp())
        password = safe_password(user_base.password, user_base.email)
        new_user =db_model.User(password=password,gender=user_base.gender,username=user_base.username,email=user_base.email,createTime=timestamp)
        try:
            db.add(new_user)
            db.commit()
        except Exception as e :
            print("操作出现错误：{}".format(e))
            db.rollback()
    return new_user
