# -*- coding:utf-8 -*-
from Student.Student import student
from Student.sqlconfig import alluser
from threading import Thread
import time

if __name__ == '__main__':
    while True:
        users = alluser()
        for user in users:
            stu = student(user[0],user[1])
            Thread(target=stu.getgrade()).start()
        time.sleep(15)
