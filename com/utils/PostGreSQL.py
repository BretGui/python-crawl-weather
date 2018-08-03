# -*- coding: utf-8 -*-

import psycopg2

dataBaseName = "weather"
userName = "postgres"
password = "Gaiaxis2011"
host = "47.97.173.229"
port = "5432"

class PostGreSQL:
    #初始化
    def __init__(self):
        self.dataBaseName = dataBaseName
        self.userName = userName
        self.password = password
        self.host = host
        self.port = port

        self._conn = self.GetConnect()
        if self._conn:
            self._cur = self._conn.cursor()

    #获取数据库连接对象
    def GetConnect(self):
        conn = False
        try:
            conn = psycopg2.connect(
                database=self.dataBaseName,
                user=self.userName,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except Exception as err:
            print("连接数据库失败，%s" % err)
        else:
            return conn

    #执行查询sql
    def ExecQuery(self,sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

    #执行增删改sql
    def ExceNonQuery(self,sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as err:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % err)
        else:
            return flag

    def GetConnectInfo(self):
        print("连接信息：")
        print("服务器:%s , 用户名:%s , 数据库:%s " % (self.host, self.userName, self.dataBaseName))