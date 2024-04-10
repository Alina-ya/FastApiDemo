# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com

"""
接口1:修改用户昵称，上传生日，需要鉴权
接口2:修改密码，需要鉴权
"""
import sys
from datetime import timedelta
from os import path

import uvicorn
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import update

sys.path.append("..")
#将当前文件所在目录的上上级目录添加到系统的搜索路径中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from config.config import app, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from model.request_model.users import UserCreate, UserInfoUpdate, UserBase, UserLogin, UserInDB
from utils.database import db
from model.database_model import db_model
from model.response_model.user_app_info import UserInfo
from common.crud import get_userInDB_id, get_userInDB_email
from model.response_model.tokenData import TokenData, Token
from utils.hash_tool import safe_password
from utils.jwt_authration import create_access_token, user_authorization
from utils.redis_tool import redis_db



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
        print("part2_type",type(part2))
        print("part2", part2)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(userdb.id),"name":userdb.password}, expires_delta=access_token_expires
        )
        token = '{}:{}:{}'.format(part1,part2,access_token)
        print('token', token)
        redis_db.handle_redis_token(userdb.id, token)
        return {"token": token,"token_type":"bearer"}



@app.get('/user/details',response_model=UserInfo)
def get_user_current(id:int,db:Session = Depends(db.get_db)):
# def get_user_current(id: int, db: Session = Depends(db.get_db),token: str = Depends(OAuth2PasswordBearer(tokenUrl='/user/login'))):
    credentials_exception = HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Could not validate credentials",
         headers={"WWW-Authenticate": "Bearer"},
    )
    redis_token = redis_db.handle_redis_token(id)  # 从redis中取token
    user = get_userInDB_id(db,user_authorization(redis_token).id)
    if user is None:
        raise credentials_exception
    print(user.email)
    return user


def update_userInDB(db:Session,username,birthYear,email):
    stm = update(db_model.User).where(db_model.User.email == email).values(username=username,birthYear=birthYear)
    try:
        db.execute(stm)
        db.commit()
        update_user = db.query(db_model.User).filter(db_model.User.email == email).first()
        return update_user
    except Exception as e:
        print("操作出现错误：{}".format(e))
        db.rollback()

@app.post('/user/update',response_model=UserInfo)
def user_update_info(user: UserInfoUpdate,email,db: Session = Depends(db.get_db)):
# def user_update_info(user: UserInfoUpdate, email, db: Session = Depends(db.get_db),token: str = Depends(OAuth2PasswordBearer(tokenUrl='/user/login'))):
    original_user = get_userInDB_email(db,email)
    redis_token = redis_db.handle_redis_token(original_user.id)
    if original_user.id == user_authorization(redis_token).id:
        NewUser = update_userInDB(db,user.username,user.birthYear,email)
        return NewUser

