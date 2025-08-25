# 应用部署指南

## 项目概述
这是一个基于Flask的Web应用，提供了智能客服对话模块的管理界面，包括意图管理、实体管理、FAQ问答等功能。

## 依赖环境
- Python 3.8+ 
- 所需Python包已在requirements.txt中列出

## 本地开发运行
1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```
2. 运行应用:
   ```
   python app.py
   ```
3. 在浏览器中访问: `http://localhost:5000`

## 生产环境部署
### 方法1: 使用Gunicorn (推荐)
1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```
2. 运行启动脚本:
   ```
   ./start.sh
   ```
   这将使用Gunicorn启动应用，默认使用4个工作进程，绑定到所有网络接口的5000端口。

### 方法2: 直接运行Python (不推荐用于生产环境)
1. 设置环境变量以禁用调试模式:
   ```
   export DEBUG=False
   ```
2. 运行应用:
   ```
   python app.py
   ```

## 访问应用
- 本地访问: `http://localhost:5000`
- 网络访问: `http://<服务器IP地址>:5000`

## 注意事项
1. 确保服务器的防火墙已开放5000端口，以允许外部访问。
2. 对于生产环境，建议使用Nginx作为反向代理，并配置SSL证书以启用HTTPS。
3. 如果应用部署在云服务器上，可能需要配置安全组规则以允许外部访问。
4. 定期备份数据，特别是output.json文件，它包含了应用的核心数据。