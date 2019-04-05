#入库指南

入库前请做好以下准备工作：

    - 安装好mysql
    - 脚本文件：Data.py
    - 安装好脚本文件依赖的库
    - 数据文件：filtered.csv

##数据库相关

    - 在/stupidSE/settings.py中配置好自己的mysql账号密码
    - 进入数据库建立一个名为ratemycourse的数据库(命令见MySQL.md)
    - 在terminal运行以下指令：
        - python manage.py makemigrations
        - python manage.py migrate
##脚本相关

    - 在terminal输入以下指令进入manage.py shell
        - python manage.py shell
    - 输入以下指令运行入库脚本
        - exec(open('Data.py', 'r', encoding='UTF-8').read())
        
    


