# webapp

本项目基于 request+flask 爬取教务网成绩及时更新反馈

用户通过登录网站查看个人成绩

## 前提条件 以ubuntu为例：

* python3
  * ``` sudo apt-get install python3 ```
  * ``` sudo apt-get install python3-pip ```
  * ``` 可用虚拟环境 ```

* mysql
  * ``` sudo apt-get install mysql-server ```
  * 设置mysql字符集utf8 在 /etc/mysql/下
  
* uwsgi
  * ``` pip3 install uwsgi ```

* supervisor
  * ``` sudo apt-get install supervisor ```
  
* nginx
  * ``` sudo apt-get install nginx ```
  

## 运行配置：
* 在Student/sqlconfig.py下 配置数据库账号密码

* mysql 创建数据库 ```create database score```

* 安装必要的python库
```
   pip install -r requirment.txt
```

```python
   #创建数据库
   python sqlconfig.py
```

* 配置uwsgi
在项目文件下创建 config.ini
```
  [uwsgi]

  # uwsgi 启动时所使用的地址与端口
  socket = 127.0.0.1:8002

  # 指向网站目录
  chdir = /home/www/ 

  # python 启动程序文件
  wsgi-file = app.py 

  # python 程序内用以启动的 application 变量名
  callable = app 

  # 处理器数
  processes = 4

  # 线程数
  threads = 2

  #状态检测地址
  stats = 127.0.0.1:9191
   
```
* 配置supervisor
在下/etc/supervisor/conf.d/创建app.conf
```
[program:sanjiangweb]
# 启动命令入口
command=/home/ubuntu/.local/bin/uwsgi /home/www/config.ini

# 命令程序所在目录
directory=/home/ubuntu/.local
#运行命令的用户名
user=ubuntu
		
autostart=true
autorestart=true
#日志地址
stdout_logfile=/home/webapp/uwsgi_supervisor.log	
```
* 配置nginx 
修改/etc/nginx/sites-enabled/default
```
server {
	listen 80;
	listen [::]:80;

	location / {
		include      uwsgi_params;
		uwsgi_pass   127.0.0.1:8002;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
		uwsgi_param UWSGI_CHDIR  /home/webapp/sanjiangweb; # 指向网站根目录
		uwsgi_param UWSGI_SCRIPT app:app; # 指定启动程序
	}
}

```

##运行服务
* ``` sudo service mysql restart ```
* ``` sudo service supervisor restart ```
* ``` sudo service nginx restart ```
* 可选

    按时更新数据成绩
  * ``` nohup python3 runserver.py & ```

