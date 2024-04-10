# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import sys
from os import path
from sqlalchemy import Boolean, Column, Integer, String
sys.path.append("..")
#将当前文件所在目录的上上级目录添加到系统的搜索路径中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#解决：  from model.users import User ModuleNotFoundError: No module named 'model'的问题
#将当前文件所在目录的上级目录添加到系统的搜索路径中
from model.response_model.user_app_info import UserInfo
from utils.database import db


#通过数据库配置文件中的基类来创建数据库模型类
class User(db.Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    phoneNo = Column(Integer,index=True,default=None)
    password = Column(String(32), unique=True)
    gender = Column(Integer,index=True,default=None)
    username =  Column(String,index=True)
    country = Column(String,index=True,default=None)
    email = Column(String(32),unique=True)
    birthYear =  Column(String,index=True,default=0)
    createTime = Column(Integer,index=True)