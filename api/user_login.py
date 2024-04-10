# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import sys
from datetime import timedelta
from os import path
from fastapi import Depends
from sqlalchemy.orm import Session

sys.path.append("..")
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from model.response_model import user_app_info
from config.config import app, ACCESS_TOKEN_EXPIRE_MINUTES
from model.request_model.users import UserCreate, UserBase, UserInDB, UserLogin
from utils.database import db
from utils.hash_tool import safe_password
from common.crud import get_userInDB_email
from utils.jwt_authration import create_access_token
from model.response_model.tokenData import Token


#验证当前登录的密码哈希值等于数据库中存储的哈希值
def verify_password(Indb_password, hashed_password):
    print("查询到的密码为：",Indb_password)
    if Indb_password == hashed_password:
        return True
    else:
        return False

#用于hash用户的密码
def get_password_md5(user:UserLogin):
    hash_password = safe_password(user.password,user.email)
    print("输入的密码哈希值为：",hash_password)
    return hash_password

#从数据库中查询当前用户，并返回

def get_user(user:UserLogin , db: Session):
    #返回值是一个.db_model.User对象
    userIndb = get_userInDB_email(db,user.email)
    print('user_dict: ',userIndb)
    print("--------------------------------")
    return userIndb

#用于验证用户密码并返回用户
def authenticate_user_password(userdb:UserInDB,user:UserLogin):
    if not userdb:
        return False
    else:
        if verify_password(userdb.password,get_password_md5(user)):
            print("登录成功！")
            return True
        else:
            print("密码输入错误，请重新登录")
            return False


@app.post('/user/login',response_model=Token)
async def login(user: UserLogin,db: Session = Depends(db.get_db)):
    userdb = get_user(user,db)
    if authenticate_user_password(userdb, user):
        part1 = 'Lollypop-V1'
        part2 = userdb.id
        print("part2", part2)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": userdb.id,"name":userdb.username}, expires_delta=access_token_expires
        )
        token = '{}:{}:{}'.format(part1,part2,access_token)
        print('token', token)
        return {"token": token,"token_type":"bearer"}
