#!/bin/bash

# 上传代码到GitHub的脚本

# 使用说明:
# 1. 确保已安装Git: https://git-scm.com/downloads
# 2. 确保已在GitHub上创建仓库
# 3. 将此脚本保存为upload_to_github.sh
# 4. 运行 chmod +x upload_to_github.sh 赋予执行权限
# 5. 运行 ./upload_to_github.sh <your-github-repo-url>

# 检查参数
if [ $# -ne 1 ]; then
    echo "用法: $0 <your-github-repo-url>"
    echo "例如: $0 https://github.com/your-username/your-repo-name.git"
    exit 1
fi

REPO_URL=$1

# 检查是否已初始化Git仓库
if [ ! -d .git ]; then
    echo "初始化Git仓库..."
    git init
    if [ $? -ne 0 ]; then
        echo "Git初始化失败"
        exit 1
    fi
fi

# 添加所有文件到暂存区
echo "添加文件到暂存区..."
git add .
if [ $? -ne 0 ]; then
    echo "添加文件失败"
    exit 1
fi

# 提交更改
echo "提交更改..."
git commit -m "Initial commit"
if [ $? -ne 0 ]; then
    echo "提交失败"
    exit 1
fi

# 添加远程仓库
echo "添加远程仓库..."
git remote add origin $REPO_URL
if [ $? -ne 0 ]; then
    echo "添加远程仓库失败，尝试更新现有远程仓库..."
    git remote set-url origin $REPO_URL
    if [ $? -ne 0 ]; then
        echo "更新远程仓库失败"
        exit 1
    fi
fi

# 推送代码到GitHub
echo "推送代码到GitHub..."
git push -u origin main
if [ $? -ne 0 ]; then
    echo "推送失败，尝试强制推送..."
    git push -u origin main --force
    if [ $? -ne 0 ]; then
        echo "强制推送也失败"
        exit 1
    fi
fi

echo "代码上传成功！"
echo "仓库地址: $REPO_URL"