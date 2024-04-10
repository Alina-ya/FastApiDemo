# coding=utf-8
# Copyright (c) 2024,Bongmi
# All rights reserved
# @Author  : xiongjiao@bongmi.com
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
class SqlDB:
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456xj@127.0.0.1:3306/FastApiData"
        # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

        engine = create_engine(
            SQLALCHEMY_DATABASE_URL, echo=True
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # 创建基本映射类
        self.Base = declarative_base()
    # def __del__(self):
    #     self.db.close()
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db = SqlDB()

