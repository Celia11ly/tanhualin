#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 使用Gunicorn启动应用
# -w 4: 4个工作进程
# -b 0.0.0.0:5000: 绑定到所有网络接口的5000端口
# --access-logfile: 访问日志文件
# --error-logfile: 错误日志文件
# app:app: 第一个app是模块名，第二个app是Flask实例名
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile access.log --error-logfile error.log app:app