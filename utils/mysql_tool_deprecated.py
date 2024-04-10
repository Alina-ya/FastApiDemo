# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
import pymysql
from config.config import mysql_host,mysql_port,mysql_username,mysql_password,mysql_db

class MysqlDb:
    def __init__(self):
        #建立数据库连接
        self.conn = pymysql.connect(host=mysql_host,
                             port=mysql_port,
                             user=mysql_username,
                             password=mysql_password,
                             database=mysql_db,
                             autocommit=True)
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 对象资源被释放时触发，在对象即将被删除时的最后操作
    def __del__(self):
        # 关闭游标
        self.cursor.close()
        #关闭数据库连接
        self.conn.close()

    #查询数据
    def select_data(self,sql):
        """查询"""
        #查询数据之前，检查数据库连接是否断了，如果断了自动重新连接
        self.conn.ping(reconnect=True)
        #使用 execute() 执行sql
        self.cursor.execute(sql)
        #使用fetchall()获取查询结果
        data = self.cursor.fetchall()
        return data

    def execute_data(self,sql):
        """插入/更新/删除"""
        try:
            #检查连接是否断开，如果断开了就重新连接
            self.conn.ping(reconnect=True)
            #使用execute执行sql
            self.cursor.execute(sql)
            #提交事务
            self.conn.commit()
        except Exception as e :
            print("操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()

    # def collate_data(self,key,db):
    #     """查询数据，校验指定字段是否已经存在"""
    #     self.conn.ping(reconnect=True)
    #     sql = 'select ' + key + 'from ' + db +'where ' +

#创建一个sql对象
db = MysqlDb()

