# 将代码上传到GitHub指南

## 前提条件
1. 已安装Git：[https://git-scm.com/downloads](https://git-scm.com/downloads)
2. 已注册GitHub账号：[https://github.com/](https://github.com/)
3. 在GitHub上创建了新仓库

## 获取GitHub仓库URL
1. 登录GitHub并进入你的仓库
2. 点击绿色的"Code"按钮
3. 复制HTTPS或SSH URL（推荐使用HTTPS URL）

## 配置Git用户名和邮箱
在终端中运行以下命令，设置你的Git用户名和邮箱：
```bash
git config --global user.name "Your GitHub Username"
git config --global user.email "your-email@example.com"
```

## 使用上传脚本
1. 打开终端，进入项目根目录：
```bash
cd /Users/Celia/Downloads/new
```

2. 为脚本添加执行权限：
```bash
chmod +x upload_to_github.sh
```

3. 运行脚本，传入你的GitHub仓库URL：
```bash
./upload_to_github.sh https://github.com/your-username/your-repo-name.git
```

## 手动上传步骤（不使用脚本）
如果你 prefer 手动执行命令，可以按照以下步骤操作：

1. 初始化Git仓库：
```bash
git init
```

2. 添加所有文件到暂存区：
```bash
git add .
```

3. 提交更改：
```bash
git commit -m "Initial commit"
```

4. 添加远程仓库：
```bash
git remote add origin https://github.com/your-username/your-repo-name.git
```

5. 推送代码到GitHub：
```bash
git push -u origin main
```

## 常见问题
1. **推送失败提示权限不足**：
   - 确保你有权限访问该仓库
   - 检查你的GitHub账号是否已登录
   - 可以尝试使用SSH URL并配置SSH密钥

2. **仓库已存在错误**：
   - 确保你使用的是正确的仓库URL
   - 如果远程仓库已存在，可以使用 `git remote set-url origin <new-url>` 命令更新

3. **分支问题**：
   - 如果GitHub默认分支是`master`而不是`main`，请将命令中的`main`改为`master`

## 注意事项
- 首次推送可能需要输入GitHub用户名和密码（或个人访问令牌）
- 个人访问令牌可以在GitHub的"Settings > Developer settings > Personal access tokens"中生成
- 确保不要上传敏感信息（如API密钥、密码等）到GitHub
- 定期推送代码以备份你的工作

如果遇到其他问题，可以查看GitHub官方文档或搜索相关错误信息。