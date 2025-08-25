# 部署指南：将Flask应用部署到免费平台

## 目录
- [Heroku部署](#heroku部署)
- [Render部署](#render部署)
- [其他免费平台选项](#其他免费平台选项)

## Heroku部署

### 前提条件
1. 注册一个Heroku账号：[https://www.heroku.com/](https://www.heroku.com/)
2. 安装Heroku CLI：[https://devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. 安装Git：[https://git-scm.com/downloads](https://git-scm.com/downloads)

### 部署步骤

#### 1. 准备本地代码
确保你的代码已经包含以下文件（我们已经帮你创建好了）：
- `app.py`：Flask应用主文件
- `requirements.txt`：项目依赖列表
- `Procfile`：Heroku启动命令
- `runtime.txt`：Python版本指定
- `output.json`：应用数据
- `templates/`：HTML模板文件夹

#### 2. 初始化Git仓库
```bash
# 在项目根目录执行
git init
git add .
git commit -m "Initial commit"
```

#### 3. 登录Heroku
```bash
heroku login
```
按照提示在浏览器中登录你的Heroku账号。

#### 4. 创建Heroku应用
```bash
heroku create your-app-name
```
将`your-app-name`替换为你想要的应用名称（必须唯一）。

#### 5. 部署代码
```bash
git push heroku main
```

#### 6. 查看应用
部署完成后，你可以通过以下命令打开应用：
```bash
heroku open
```

### 环境变量配置
如果需要配置环境变量（如DEBUG模式），可以使用以下命令：
```bash
heroku config:set DEBUG=false
```

### 查看应用日志
```bash
heroku logs --tail
```

## Render部署

### 前提条件
1. 注册一个Render账号：[https://render.com/](https://render.com/)
2. 安装Git：[https://git-scm.com/downloads](https://git-scm.com/downloads)
3. 将代码上传到GitHub或GitLab仓库

### 部署步骤

#### 1. 准备本地代码
确保你的代码已经包含以下文件（我们已经帮你创建好了）：
- `app.py`：Flask应用主文件
- `requirements.txt`：项目依赖列表
- `render.yaml`：Render部署配置文件
- `output.json`：应用数据
- `templates/`：HTML模板文件夹

#### 2. 上传代码到GitHub
```bash
# 在项目根目录执行
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main
```

#### 3. 登录Render并创建Web服务
1. 访问[Render控制台](https://dashboard.render.com/)
2. 点击"New +"按钮，选择"Web Service"
3. 选择你的GitHub仓库
4. Render会自动检测到`render.yaml`文件并使用其中的配置
5. 点击"Create Web Service"按钮

#### 4. 部署应用
Render会自动开始部署过程。你可以在控制台查看部署日志。

#### 5. 查看应用
部署完成后，你可以点击控制台中的应用链接访问你的应用。

### 环境变量配置
1. 在Render控制台中，选择你的应用
2. 点击"Environment"标签
3. 点击"Add Environment Variable"按钮添加或修改环境变量

### 查看应用日志
在Render控制台中，选择你的应用，然后点击"Logs"标签查看应用日志。

## 其他免费平台选项

### GitHub Pages（仅支持静态网站）
由于我们的应用是动态Flask应用，GitHub Pages并不直接支持。如果需要使用GitHub Pages，你需要将应用转换为静态网站，或者使用GitHub Actions配合其他服务进行部署。

### 其他平台
1. **PythonAnywhere**：[https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
2. **Glitch**：[https://glitch.com/](https://glitch.com/)

这些平台也提供免费的Python应用部署服务，具体步骤请参考各平台的官方文档。