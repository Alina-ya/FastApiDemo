# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import redis
from config.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWD,ACCESS_TOKEN_EXPIRE_MINUTES


class RedisDb():

    def __init__(self, host, port, passwd):
        # 建立数据库连接
        self.r = redis.Redis(
            host=host,
            port=port,
            password=passwd,
            decode_responses=True # get() 得到字符串类型的数据
        )

    def handle_redis_token(self, key, value=None):
        if value:  # 如果value非空，那么就设置key和value，EXPIRE_TIME为过期时间
            self.r.set(key, value, ex=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:  # 如果value为空，那么直接通过key从redis中取值
            redis_token = self.r.get(key)
            return redis_token

redis_db = RedisDb(REDIS_HOST, REDIS_PORT, REDIS_PASSWD)