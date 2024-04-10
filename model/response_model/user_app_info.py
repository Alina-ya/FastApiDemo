# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
from typing import Union

from pydantic import BaseModel

from model.request_model.users import UserBase

class UserInfo(UserBase):
    """
    响应模型：
    id:
    email:
    is_active
    并且设置orm_mode与之兼容
    """
    id: int
    phoneNo: Union[int, None] = None
    country: Union[str, None] = None
    createTime: Union[int, None] = None
    birthYear: Union[int, None] = None

    class Config:
        from_attributes = True

