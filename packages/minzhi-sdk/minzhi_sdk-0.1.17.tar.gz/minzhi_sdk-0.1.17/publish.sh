#!/bin/bash

# 发布脚本
# 用法: ./publish.sh [test|prod]

ENV=${1:-test}

echo "正在构建包..."
uv build

if [ "$ENV" = "test" ]; then
    echo "发布到测试 PyPI..."
    echo "使用测试 API Token（长度: ${#UV_PUBLISH_PASSWORD_TESTPYPI} 字符）"
    # 保存 token 值，然后清除环境变量避免冲突
    TEST_TOKEN="$UV_PUBLISH_PASSWORD_TESTPYPI"
    unset UV_PUBLISH_USERNAME UV_PUBLISH_PASSWORD
    uv publish --token "$TEST_TOKEN" --index testpypi --keyring-provider disabled
    echo "✅ 发布到测试 PyPI 成功！"
    echo "查看链接: https://test.pypi.org/project/minzhi-sdk/"
    echo "安装测试包: pip install --index-url https://test.pypi.org/simple/ minzhi-sdk"
elif [ "$ENV" = "prod" ]; then
    echo "发布到生产 PyPI..."
    # 保存 token 值，然后清除环境变量避免冲突
    PROD_TOKEN="$UV_PUBLISH_PASSWORD"
    echo "使用 API Token（长度: ${#PROD_TOKEN} 字符）"
    echo "Token前缀: ${PROD_TOKEN:0:10}..."
    unset UV_PUBLISH_USERNAME UV_PUBLISH_PASSWORD
    uv publish --token "$PROD_TOKEN" --keyring-provider disabled
    echo "✅ 发布到生产 PyPI 成功！"
    echo "查看链接: https://pypi.org/project/minzhi-sdk/"
    echo "安装包: pip install minzhi-sdk"
else
    echo "错误: 请指定环境 'test' 或 'prod'"
    echo "用法: ./publish.sh [test|prod]"
    exit 1
fi 