# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import hashlib
import hmac

from config.config import Password_Key


#给用户密码加密
#生成一个 HMAC-SHA-1 摘要，用于对消息进行认证和保护。使用密钥可以增加摘要的安全性
# def safe_password(message,key):
#     #将字符串转化为字节流
#     message = bytes(message,'utf-8')
#     key = bytes(key,'utf-8')
#     #使用`hmac.new`函数创建一个`hmac`对象，该对象使用SHA-1算法对`key`和`message`进行哈希运算
#     #hmac.new(key,message,hashlib.sha1).digest() 的意义是使用密钥（key）对消息（message）进行哈希计算，并返回计算结果的摘要（digest）
#     digester  = hmac.new(key,message,hashlib.md5)
#     hash_password = digester.digest()
#     return hash_password



#给用户密码加密
def safe_password(message, str):
    str = message + str+ Password_Key # 把用户名也作为str加密的一部分
    #将字符串转化成字节
    str_bytes = bytes(str,'utf-8')
    # 创建md5对象
    md5 = hashlib.md5()
    #创建一个md5对象，并使用update()方法将字节类型的字符串传递给md5对象进行加密
    md5.update(str_bytes)
    # 返回密文
    return md5.hexdigest()
