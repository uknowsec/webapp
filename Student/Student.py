# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.request import quote
import re
from threading import Thread
from . import sqlconfig
import time

def findvalues(tpage):
    this_html = BeautifulSoup(tpage.text, "lxml")
    val = this_html.find('input')['value']
    return val

class student:
    def __init__(self,number,passwd):
        self.number = number
        self.passwd = passwd
        self.name = ''
        self.info = {}
        self.grade = []


    def getgrade(self):
        s = requests.Session()
        # 默认不填学期 学年
        xueqi = ''
        xuenian = ''
        baseUrl = 'http://218.94.104.201:85'
        url = baseUrl + '/default6.aspx'
        headers = {
            'Referer': baseUrl + '/xs_main.aspx?xh=' + self.number,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/46.0.2490.86 Safari/537.36',
        }
        page = s.get(url)
        values = findvalues(page)
        datas = {
            '__VIEWSTATE': values,
            'txtYhm': self.number,
            'txtMm': self.passwd,
            'rblJs': '学生',
            'btnDl': '登录'
        }
        # 提交表单 登陆
        r = s.post(url, data=datas)

        # 形成http://ip/xscj.aspx?xh=usernum&xm=username&gnmkdm=N121605

        cd = BeautifulSoup(r.text, 'html.parser')
        try:
            name = cd.find('span', id='xhxm').get_text()
        except Exception as e:
            return
        username = name[:-2]
        self.name = quote(self.name, encoding='gb2312')
        find_url = baseUrl + '/xscj.aspx?xh=' + self.number + '&xm=' + self.name + '&gnmkdm=N121605'

        # 两次get 避免move object
        grade1 = s.get(find_url, headers=headers)

        headers2 = {
            'Referer': find_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 '
                          'Safari/537.36',
        }
        # 查询成绩表单数据
        page = s.get(find_url, headers=headers2)
        find_values = findvalues(page)
        finddatas = {
            '__VIEWSTATE': find_values,
            'ddlXN': xuenian,
            'ddlXQ': xueqi,
            'txtQSCJ': '0',
            'txtZZCJ': '100',
            'Button2': '在校学习成绩查询'
        }
        # 提交查询的信息
        grade = s.post(find_url, data=finddatas, headers=headers2)
        grade.encoding='gb2312'
        gradehtml = BeautifulSoup(grade.text, "html.parser")
        st_infos = gradehtml.find('table', id='Table1').find_all('span', {'id': re.compile('Label*')})
        #获取学生信息
        for line in st_infos:
            if line.get_text() !='在校学习成绩' and line.get_text()!= '':
                st_info = line.get_text().split("：")
                if len(st_info) == 2:
                    self.info[st_info[0]]=st_info[1]
                else :
                    self.info['专业'] = st_info[0]


        #获取所有成绩
        st_grades = gradehtml.find('table',class_='datelist').find_all('tr')[1:]
        for line in st_grades:
            st_grade = []
            for grade_info in line.find_all('td'):
                st_gradelist = grade_info.get_text()
                # 空格 &nasp; -> \xa0
                if st_gradelist == '\xa0':
                    st_gradelist = ' '
                st_grade.append(st_gradelist)
            self.grade.append(st_grade)

        #for line in self.grade:
        #    print(line)
        #print(self.info)
        #更新数据库
        new=Thread(target=sqlconfig.inserStudent ,args=(self.info,self.passwd,self.grade))
        new.start()

