# -*- coding:utf-8 -*-
import pymysql
import sys

HOST_IP = 'localhost'
SQL_USERNAME = 'root'
SQL_PASSWORD = 'jiangyang'
SQL_USEDATABASE = 'socre'


def createtables():
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS Students")
        sql = """CREATE TABLE Students(
                STUNum VARCHAR(20) NOT NULL PRIMARY KEY,
                STUpass VARCHAR(22),
                STUName VARCHAR(10),
                STUCollege VARCHAR(20),
                STUClass VARCHAR(20),
                STUSpecialty VARCHAR(20))ENGINE=InnoDB DEFAULT CHARSET=utf8"""
        cursor.execute(sql)
        cursor.execute("DROP TABLE IF EXISTS grade")
        sql = """CREATE TABLE grade(
                ST_id int(5) auto_increment PRIMARY KEY,
                STNum VARCHAR(20),
                STName VARCHAR(20),
                CId VARCHAR(20),
                CName VARCHAR(40),
                CType VARCHAR(10),
                CGrade VARCHAR(6),
                CFGrade VARCHAR(6),
                Ctypes VARCHAR(10),
                CRGrade VARCHAR(6),
                CCGrade VARCHAR(6),
                CCredit VARCHAR(6),
                CFlag VARCHAR(6)
                )ENGINE=InnoDB DEFAULT CHARSET=utf8"""
        cursor.execute(sql)
    except Exception  as e:
        pass
    finally:
        cursor.close()
        db.close()

def inserStudent(info,passwd,grade):
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql="select count(*) from Students where STUNum=%s"
        cursor.execute(sql, info['学号'])
        result=cursor.fetchone()
        if result[0] < 1:
            sql="insert into Students value(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(info['学号'], passwd, info['姓名'], info['学院'], info['行政班'], info['专业']))
        else:
            print("账号已存在")

        for i in grade:
            sql = "select count(*) from grade where STNum=%s and CId=%s"
            cursor.execute(sql, (info['学号'], i[0]))
            result = cursor.fetchone()
            if result[0] < 1:
                sql="""insert into grade (STNum, STName, CId, CName, CType,
                CGrade, CFGrade, Ctypes, CRGrade, CCGrade, CCredit,CFlag)
                value
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(sql, (info['学号'], info['姓名'], i[0], i[1], i[2], i[3],
                                     i[4], i[5], i[6], i[7], i[8], i[9]))
        db.commit()
    except Exception  as e:
        pass
    finally:
        cursor.close()
        db.close()


def selectuser(uid):
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "select count(*) from Students where STUNum=%s"
        cursor.execute(sql, uid)
        result = cursor.fetchone()
        if result[0] < 1:
            return False
        else:
            return True
    except:
        pass


def selectgrade(uid):
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "select * from grade where STNum=%s"
        cursor.execute(sql, uid)
        result = cursor.fetchall()
        return result
    except Exception as e:
        pass


def alluser():
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "select * from Students"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        pass


if __name__ == '__main__':
    selectgrade('12014054055')
