# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
from typing import Union

from pydantic import BaseModel

#请求体，当你需要将数据从客户端（例如浏览器）发送给 API 时，你将其作为「请求体」发送。

class UserBase(BaseModel):
    # # 当一个模型属性具有默认值时，它不是必需的，否则它是一个必需属性将默认值设为None可使其成为可选属性
    # #birthYear和gender都是可选属性，上传数据时不填写也合法
    email: str
    username: str
    gender:Union[int, None] = None

class UserCreate(UserBase):
    """
    请求模型验证：
    email:
    password:
    """
    password: str

class UserLogin(BaseModel):
    """
    登录验证模型
    """
    email: str
    password: str

class UserInfoUpdate(BaseModel):
    """
    更新用户信息模型
    """
    birthYear: int
    username: str

class UserInDB(UserBase):
    username:str
    email: str
    password: str