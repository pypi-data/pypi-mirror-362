# 敏智 Python SDK

[![PyPI version](https://badge.fury.io/py/minzhi-sdk.svg)](https://badge.fury.io/py/minzhi-sdk)
[![Python version](https://img.shields.io/pypi/pyversions/minzhi-sdk.svg)](https://pypi.org/project/minzhi-sdk/)

敏智 Python SDK 是一个功能强大的 Python 库，提供了自动化执行 (AE) 和 CMDB 客户端功能。该 SDK 旨在简化与敏智平台的集成，让开发者能够轻松地进行数据查询、操作和管理。

## 📋 目录

- [特性](#特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [详细用法](#详细用法)
  - [AEClient 自动化执行客户端](#aeclient-自动化执行客户端)
  - [CmdbClient CMDB客户端](#cmdbclient-cmdb客户端)
  - [Authorization 授权模块](#authorization-授权模块)
- [API 参考](#api-参考)
- [开发和发布](#开发和发布)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## ✨ 特性

- **🚀 自动化执行 (AE) 客户端**: 提供数据查询、增删改查等完整的数据库操作功能
- **🗃️ CMDB 客户端**: 支持配置管理数据库的数据获取和导入
- **🔐 授权管理**: 内置 RSA 加密和 token 管理
- **📊 数据处理**: 内置结果处理类，支持数据验证、转换和导出
- **🛡️ 异常处理**: 完善的错误处理和日志记录
- **📈 多种输出格式**: 支持 JSON、DataFrame 等多种数据格式

## 📦 安装

### 从 PyPI 安装（推荐）

```bash
pip install minzhi-sdk
```

### 从测试 PyPI 安装

```bash
pip install --index-url https://test.pypi.org/simple/ minzhi-sdk
```

### 依赖项

该 SDK 需要 Python 3.8+ 版本，并依赖以下包：

- `loguru`: 日志记录
- `pycryptodome`: RSA 加密
- `requests`: HTTP 请求

## 🚀 快速开始

### 基本使用示例

```python
from minzhi import AEClient, CmdbClient, Authorization

# 1. 使用 AEClient 进行数据操作
ae_client = AEClient(
    businessId="your_business_id",
    table_name="your_table_name"
)

# 分页查询数据
result = ae_client.selectPage(current=1, pageSize=10)
if result.is_success():
    data = result.get_data()
    print(f"查询到 {result.count()} 条记录")

# 2. 使用 CmdbClient 获取配置数据
cmdb_client = CmdbClient(
    view_id="your_view_id",
    CMDB_SERVER="https://your-cmdb-server.com",
    APPID="your_app_id",
    APPSECRET="your_app_secret"
)

# 获取所有数据
all_data = cmdb_client.get_all_data()
print(f"获取到 {len(all_data)} 条 CMDB 记录")

# 3. 使用 Authorization 进行身份验证
auth = Authorization(
    SERVER="https://your-server.com",
    USER="your_username",
    PASSWORD="your_password"
)
```

## 📖 详细用法

### AEClient 自动化执行客户端

AEClient 提供了完整的数据库操作功能，支持查询、插入、更新和删除操作。

#### 基本配置

```python
from minzhi import AEClient

client = AEClient(
    businessId="your_business_id",
    table_name="your_table_name"
)
```

#### 查询操作

```python
# 分页查询
result = client.selectPage(current=1, pageSize=20)

# 查询所有记录
result = client.selectAll(
    fields=["id", "name", "status"],
    query={"status": "active"}
)

# 检查查询结果
if result.is_success():
    data = result.get_data()
    print(f"查询成功，共 {result.count()} 条记录")
    
    # 转换为 DataFrame (需要安装 pandas)
    df = result.to_dataframe()
    
    # 转换为 JSON
    json_str = result.to_json()
else:
    print(f"查询失败: {result.get_error_message()}")
```

#### 插入操作

```python
# 插入单条记录
data = {"name": "张三", "age": 25, "department": "技术部"}
result = client.insertOne(data)

# 批量插入
data_list = [
    {"name": "李四", "age": 28, "department": "产品部"},
    {"name": "王五", "age": 30, "department": "运营部"}
]
result = client.insertMany(data_list)

# 插入或更新（如果记录存在则更新，不存在则插入）
result = client.insertOrUpdate(data)
```

#### 更新操作

```python
# 批量更新
update_data = {
    "where": {"department": "技术部"},
    "data": {"status": "active"}
}
result = client.updateMany(update_data)
```

#### 删除操作

```python
# 根据 ID 删除
result = client.deleteByIds(["id1", "id2", "id3"])

# 根据条件删除
result = client.delete(
    fields=["id"],
    query={"status": "inactive"}
)
```

#### 枚举值查询

```python
# 获取枚举值
result = client.getEnum("status_enum")
if result.is_success():
    enum_data = result.get_data()
    # 返回格式: {"标签": "值", ...}
    print(enum_data)
```

### CmdbClient CMDB客户端

CmdbClient 用于与配置管理数据库进行交互。

#### 基本配置

```python
from minzhi import CmdbClient

client = CmdbClient(
    view_id="your_view_id",
    CMDB_SERVER="https://your-cmdb-server.com",
    APPID="your_app_id",
    APPSECRET="your_app_secret"
)
```

#### 数据获取

```python
# 获取所有数据
all_data = client.get_all_data()

# 带查询条件的数据获取
query_conditions = [
    {"field": "status", "operator": "eq", "value": "active"}
]
filtered_data = client.get_all_data(
    startPage=1,
    pageSize=500,
    queryKey=query_conditions
)
```

#### 数据导入

```python
# 准备要导入的数据
import_data = [
    {"name": "服务器A", "ip": "192.168.1.100", "status": "运行中"},
    {"name": "服务器B", "ip": "192.168.1.101", "status": "维护中"}
]

# 导入数据
result = client.import_data(import_data)
if result.get("success"):
    print("数据导入成功")
else:
    print(f"数据导入失败: {result.get('message')}")
```

### Authorization 授权模块

Authorization 模块处理身份验证和 token 管理。

#### 基本使用

```python
from minzhi import Authorization

auth = Authorization(
    SERVER="https://your-server.com",
    USER="your_username",
    PASSWORD="your_password"
)

# 获取 token
token = auth.get_token()

# 获取带 Cookie 的请求头
headers = auth.HEADERS
```

#### 在其他请求中使用

```python
import requests

# 使用授权信息发送请求
response = requests.get(
    "https://your-server.com/api/data",
    headers=auth.HEADERS
)
```

## 📚 API 参考

### Result 类

查询操作返回的 `Result` 对象提供以下方法：

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `is_success()` | 检查请求是否成功 | `bool` |
| `ensure_success()` | 确保成功，失败时抛出异常 | `Result` |
| `get_data()` | 获取处理后的数据 | `dict` |
| `to_json()` | 转换为 JSON 字符串 | `str` |
| `count()` | 获取记录数量 | `int` |
| `is_empty()` | 检查结果是否为空 | `bool` |
| `get_error_message()` | 获取错误信息 | `str` |
| `to_dataframe()` | 转换为 pandas DataFrame | `DataFrame` |

### AEClient 方法

| 方法 | 说明 | 参数 |
|------|------|------|
| `selectPage(current, pageSize)` | 分页查询 | `current`: 页码, `pageSize`: 每页条数 |
| `selectAll(fields, query)` | 查询所有记录 | `fields`: 字段列表, `query`: 查询条件 |
| `deleteByIds(ids)` | 按 ID 删除 | `ids`: ID 列表 |
| `delete(fields, query)` | 按条件删除 | `fields`: 字段列表, `query`: 删除条件 |
| `updateMany(data)` | 批量更新 | `data`: 更新数据列表 |
| `insertMany(data)` | 批量插入 | `data`: 记录列表 |
| `insertOrUpdate(data)` | 插入或更新 | `data`: 记录数据 |
| `insertOne(data)` | 插入单条记录 | `data`: 记录数据 |
| `getEnum(enum_name)` | 获取枚举值 | `enum_name`: 枚举名称 |

## 🔧 开发和发布

### 开发环境设置

1. 克隆项目
```bash
git clone <repository-url>
cd minzhi_sdk
```

2. 安装开发依赖
```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 构建和发布

项目使用 `uv` 作为包管理器和构建工具。

#### 构建包

```bash
uv build
```

#### 发布到测试环境

```bash
# 设置测试环境的 API Token
export UV_PUBLISH_PASSWORD_TESTPYPI="your_test_pypi_token"

# 发布到测试 PyPI
./publish.sh test
```

#### 发布到生产环境

```bash
# 设置生产环境的 API Token
export UV_PUBLISH_PASSWORD="your_pypi_token"

# 发布到生产 PyPI
./publish.sh prod
```

### 版本管理

在 `pyproject.toml` 中更新版本号：

```toml
[project]
version = "0.1.13"
```

### 发布流程

1. 更新版本号
2. 构建包：`uv build`
3. 测试发布：`./publish.sh test`
4. 验证测试包
5. 生产发布：`./publish.sh prod`

## 🤝 贡献指南

我们欢迎所有形式的贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 使用 Python 3.8+ 语法
- 遵循 PEP 8 代码风格
- 添加必要的文档字符串
- 编写单元测试

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果您遇到问题或有疑问，请：

1. 查看 [Issues](https://github.com/your-repo/minzhi-sdk/issues) 页面
2. 创建新的 Issue 描述您的问题
3. 联系维护团队

## 📊 更新日志

### v0.1.14 (当前版本)
- 完善 AEClient 数据操作功能
- 优化 CmdbClient 数据获取性能
- 改进 Result 类的数据处理能力
- 增强错误处理和日志记录

---

**敏智 Python SDK** - 让数据操作更简单 🚀
