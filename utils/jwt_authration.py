# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import sys
from datetime import timedelta, datetime
from os import path
from typing import Union
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from model.response_model.tokenData import TokenData

sys.path.append("..")
#将当前文件所在目录的上上级目录添加到系统的搜索路径中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#解
from config.config import SECRET_KEY,ALGORITHM

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    根据用户信息生成token
    """
    #将传入的`data`字典进行浅拷贝，赋值给`to_encode`变量。这样做是为了不修改原始的`data`字典
    to_encode = data.copy()
    #判断是否传入了过期时间间隔
    if expires_delta:
        #过期时间：当前时间+过期时间间隔
        expire = datetime.utcnow() + expires_delta
    else:
        #过期时间：当前时间+15分钟
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #print("encoded_jwt",encoded_jwt)
    #jwt_token = encoded_jwt.replace('.','')
    return encoded_jwt

def user_authorization(token: str = Depends(OAuth2PasswordBearer(tokenUrl='/user/login'))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    result = str(token).split(":")
    token = result[-1]
    print("token", token)
    print("token_type", type(token))
    try:
        # print("jinrutry")
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("sub")
        print("id", id)
        username: str = payload.get("username")
        print("username", username)
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id, username=username)
    except JWTError:
        raise credentials_exception
    return token_data













# #还原JWT的原始格式
# def Restore_jwt(token:str):
#     token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiI2MDY2MjMxOTMiLCJuYW1lIjoienlsbHN1ZGh1ICIsImV4cCI6MTcwODQxODM2OH0E7ApGimtf4txCK5a0PlB8OH5N8xuijzRA39WToEHCZk'
#     #在JWT的HS256加密算法中点号（.）是用来分割JWT的三个部分：头部（Header）、载荷（Payload）和签名（Signature）
#     header_base64 = token.split(".", 1)
#     header_base64, payload_base64, signature = token.split('.')
#
#     print("header_base64",header_base64)
#
#     # Base64解码头部和载荷
#     header = base64.urlsafe_b64decode(header_base64 + "==")
#     payload = base64.urlsafe_b64decode(payload_base64 + "==")
#     # 还原为原始的JSON字符串
#     header_str = header.decode("utf-8")
#     payload_str = payload.decode("utf-8")
#     # 重新添加点号
#     jwt = header_str + "." + payload_str
#     print(jwt)
#     return jwt

