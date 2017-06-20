# -*- coding:utf-8 -*-
import pymysql


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
                ST_id INT(5) AUTO_INCREMENT PRIMARY KEY,
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
    except:
        pass
    finally:
        cursor.close()
        db.close()


def inserStudent(info, passwd, grade):
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "SELECT count(*) FROM Students WHERE STUNum = %s"
        cursor.execute(sql, info['学号'])
        result = cursor.fetchone()
        if result[0] < 1:
            sql = "INSERT INTO Students VALUE(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (info['学号'], passwd, info['姓名'], info['学院'], info['行政班'], info['专业']))
            db.commit()
        else:
            sql = "SELECT count(*) FROM Students WHERE STUNum = %s and STUPass = %s"
            cursor.execute(sql, (info['学号'], passwd))
            result = cursor.fetchone()
            if result[0] < 1:
                sql = "UPDATE Students set STUPass = %s WHERE STUNum = %s"
                cursor.execute(sql, (passwd, info['学号']))
        db.commit()
        for i in grade:
            sql = "select count(*) from grade where STNum=%s and CId=%s"
            cursor.execute(sql, (info['学号'], i[0]))
            result = cursor.fetchone()
            if result[0] < 1:
                sql = """INSERT INTO grade (STNum, STName, CId, CName, CType,
                CGrade, CFGrade, Ctypes, CRGrade, CCGrade, CCredit,CFlag)
                VALUE
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(sql, (info['学号'], info['姓名'], i[0], i[1], i[2], i[3],
                                     i[4], i[5], i[6], i[7], i[8], i[9]))
        db.commit()
    except:
        pass
    finally:
        cursor.close()
        db.close()


def selectuser(uid):
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "SELECT count(*) FROM Students WHERE STUNum = %s"
        cursor.execute(sql, uid)
        result = cursor.fetchone()
        if result[0] < 1:
            return False
        else:
            return True
    except:
        pass
    finally:
        db.commit()
        cursor.close()
        db.close()

def selectgrade(uid):
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "SELECT * FROM grade WHERE STNum = %s"
        cursor.execute(sql, uid)
        result = cursor.fetchall()
        return result
    except:
        pass
    finally:
        db.commit()
        cursor.close()
        db.close()

def alluser():
    db = pymysql.connect(HOST_IP, SQL_USERNAME, SQL_PASSWORD, SQL_USEDATABASE, charset="utf8")
    cursor = db.cursor()
    try:
        sql = "SELECT * FROM Students"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        pass
    finally:
        db.commit()
        cursor.close()
        db.close()

if __name__ == '__main__':
    createtables()
