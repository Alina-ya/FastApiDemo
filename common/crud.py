# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import sys
from datetime import datetime
from os import path

from sqlalchemy.orm import Session

from model.request_model.users import UserCreate
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


#新建一个用户

def create_user(user:UserCreate,db:Session):
    now = datetime.now()
    timestamp = int(now.timestamp())
    password = safe_password(user.password, user.username)
    new_user = db_model.User(password=password, gender=user.gender, username=user.username,
                             email=user.email, createTime=timestamp)
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        print("操作出现错误：{}".format(e))
        db.rollback()
    # elif user_base.gender!='0' or user_base.gender!='1':
    #     raise HTTPException(status_code=4002,detail='Incorrect format')
    return new_user

#查询数据库中的用户
def get_userInDB_email(db:Session,email:str):
    return db.query(db_model.User).filter(db_model.User.email == email).first()

def get_userInDB_id(db:Session,id:int):
    return db.query(db_model.User).filter(db_model.User.id == id).first()