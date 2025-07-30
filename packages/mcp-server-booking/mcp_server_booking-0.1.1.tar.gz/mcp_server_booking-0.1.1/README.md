# CUHKSZ Booking MCP

一个基于 Model Context Protocol (MCP) 的香港中文大学（深圳）场馆预订系统接口服务，提供场地信息查询、可用性检查和在线预订等功能。

## ✨ 功能特性

- **实时场地查询**: 获取指定场地的基本信息和当日已有的预订情况。
- **可用时段检查**: 查询特定时间段内所有可用的具体场地。
- **在线预订**: 通过提供场地ID、时间、联系方式等信息完成场馆预订。
- **智能会话管理**: 自动处理登录状态，会话超时（15分钟）后自动重新登录。
- **高效查询缓存**: 对查询类接口提供缓存（5-10分钟），避免重复请求，提升响应速度。
- **容器化部署**: 提供 Docker 和 Docker Compose 配置，实现一键部署和环境隔离。

## 📋 目录

- [项目架构](#-项目架构)
- [实现方式与核心逻辑](#-实现方式与核心逻辑)
- [部署指南](#-部署指南)
- [测试说明](#-测试说明)
- [API 接口](#-api-接口)
- [故障排除](#-故障排除)
- [许可证与免责声明](#-许可证与免责声明)

## 🏗️ 项目架构

### 整体架构图

```
BOOKING-MCP/
├── src/mcp_server_booking/      # 核心源代码目录
│   ├── __init__.py              # 包初始化文件
│   ├── __main__.py              # 服务启动入口点
│   ├── booking.py               # MCP 服务器主逻辑，工具定义
│   ├── booking_system.py        # 场馆预订系统交互核心模块
│   ├── requirements.txt         # Python 依赖包列表
│   └── Dockerfile               # Docker 容器构建文件
├── test/
│   ├── test.py                  # 完整功能测试脚本
│   └── requirements.txt         # 测试脚本依赖
├── docker-compose.yml           # Docker Compose 配置
├── .env.example                 # 环境变量配置文件示例
└── README.md                    # 项目文档
```

### 核心模块说明

#### 1. `booking.py` - MCP 服务器层
- **职责**: 定义 MCP 工具接口，处理异步请求，管理缓存和登录会话。
- **核心功能**:
  - **会话管理**: 15分钟无操作自动重新登录，确保会话有效。
  - **结果缓存**: 对查询类工具提供缓存，减少重复请求，提高响应速度。
  - **异步执行**: 将同步的爬虫和请求操作包装在异步工具中，避免阻塞服务。
  - **工具定义**: 定义了5个与预订系统交互的 MCP 工具。

#### 2. `booking_system.py` - Booking 交互层
- **职责**: 直接与 CUHKSZ 场馆预订系统网站进行交互，负责登录认证、数据抓取和表单提交。
- **核心功能**:
  - **ADFS 登录**: 处理 ADFS (Active Directory Federation Services) 的认证流程。
  - **数据解析**: 使用 `lxml` 和 `json` 解析场地信息、预订状态等数据。
  - **预订操作**: 模拟浏览器行为，提交预订表单以完成场馆预订。

#### 3. `__main__.py` - 服务入口与凭证管理
- **职责**: 处理服务启动、参数配置和凭证管理。它会验证启动时是否提供了必要的 Booking 用户名和密码，并支持从命令行参数或 `.env` 文件中读取这些凭证。
- **传输协议**: Server-Sent Events (SSE)。
- **默认端口**: 3001。

### 技术栈

- **后端框架**: FastMCP (基于 FastAPI)
- **HTTP 客户端**: requests
- **HTML/JSON 解析**: lxml, json
- **SSL 处理**: pyOpenSSL
- **容器化**: Docker, Docker Compose
- **传输协议**: Server-Sent Events (SSE)

## 🔧 实现方式与核心逻辑

### 1. 登录认证流程

```python
# booking_system.py
def login(self) -> bool:
    # 直接向 ADFS 端点发送包含用户名和密码的 POST 请求
    url = "https://sts.cuhk.edu.cn/adfs/oauth2/authorize"
    params = {
        "response_type": "code",
        "client_id": "caf5aded-3f28-4b64-b836-4451312e1ea3",
        "redirect_uri": "https://booking.cuhk.edu.cn/sso/code",
    }
    data = {
        "UserName": "cuhksz\\" + self.username,
        "Password": self.password,
        "AuthMethod": "FormsAuthentication"
    }
    r = self.session.post(url, params=params, data=data, allow_redirects=True)
    
    # 通过检查重定向后的 URL 是否包含 booking.cuhk.edu.cn 来验证登录
    if not ("booking.cuhk.edu.cn" in r.url):
        raise ValidationError("Username or password incorrect!")
    
    return True
```

### 2. 缓存与会话管理

```python
# booking.py
_booking_instance: Optional[BookingSystem] = None
_last_login_time: float = 0
_global_cache: Dict[str, Dict] = {}
LOGIN_TIMEOUT = 15 * 60  # 15分钟

def _get_booking_instance() -> BookingSystem:
    # 检查会话是否超时或实例是否存在
    if (_booking_instance is None or 
        time.time() - _last_login_time > LOGIN_TIMEOUT):
        # 超时或首次调用，重新创建实例并登录
        _booking_instance = BookingSystem(username, password)
        _last_login_time = time.time()
    return _booking_instance

def _get_cached_or_fetch(cache_key: str, fetch_func, ttl: int):
    # 检查缓存是否存在且未过期
    if (cache_key in _global_cache and ...):
        return _global_cache[cache_key]['data']
    
    # 缓存未命中，调用 fetch_func 获取新数据并存入缓存
    data = fetch_func()
    _global_cache[cache_key] = {'data': data, 'timestamp': time.time()}
    return data
```

### 3. 数据抓取与预订逻辑

- **数据抓取**: 通过向预订系统的 API (`/eventsV1`) 发送 GET 请求，获取包含场地预订情况的 JSON 数据。
- **场地解析**: 通过请求场地主页并使用 XPath 解析 HTML，获取所有可用的场地及其 ID。
- **预订提交**: 模拟浏览器行为，先通过 GET 请求获取预订表单的动态参数，然后将所有信息（包括用户输入）打包成 POST 请求发送到 `/saveData` 接口，完成预订。

## 🚀 部署指南

### 环境要求

- Docker 和 Docker Compose
- 有效的 CUHKSZ 学号和密码

### 1. 克隆项目

```bash
git clone https://github.com/your-repo/awesome-cuhksz-mcp.git
cd BOOKING-MCP
```

### 2. 创建环境变量文件

复制示例文件并填入您的凭证。

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
# .env
BOOKING_USERNAME=你的学号
BOOKING_PASSWORD=你的密码
MCP_SERVER_PORT=3001
```

> **凭证提供方式**
>
> 服务启动时必须提供 Booking 用户名和密码。支持以下两种方式，**命令行参数的优先级更高**：
>
> 1.  **命令行参数 (推荐用于调试)**:
>     直接在启动命令中通过 `--username` 和 `--password` 参数提供。
> 2.  **.env 文件 (推荐用于 Docker 部署)**:
>     在 `.env` 文件中设置 `BOOKING_USERNAME` 和 `BOOKING_PASSWORD`。`docker-compose` 会自动加载此文件。

**⚠️ 安全提醒**: 请确保 `.env` 文件不会被提交到版本控制系统。

### 3. 构建和启动服务

使用 Docker Compose 一键构建并启动服务。

```bash
# 构建并以守护进程模式启动容器
docker-compose up --build -d

# 查看实时日志
docker-compose logs -f booking-mcp

# 停止服务
docker-compose down
```

### 4. 验证部署

服务启动后，你应该能看到类似以下的日志输出：
```
booking-mcp-server | INFO:     Started server process [1]
booking-mcp-server | INFO:     Waiting for application startup.
booking-mcp-server | INFO:     Application startup complete.
booking-mcp-server | INFO:     Uvicorn running on http://0.0.0.0:3001 (Press CTRL+C to quit)
```
服务将在 `http://localhost:3001` 上提供 MCP 接口。

## 🧪 测试说明

项目提供了完整的自动化测试脚本，可以测试所有 MCP 工具的功能。

### 1. 运行测试

```bash
# 确保服务已在 Docker 中运行
docker-compose up -d

# 安装测试脚本的依赖
pip install -r test/requirements.txt

# 运行测试
python test/test.py
```

### 2. 测试模式

脚本提供三种测试模式：
- **模式 1: 安全测试**: 调用所有查询类工具，不执行真实的预订操作。
- **模式 2: 快速预订测试**: 使用默认参数（后天上午10-11点）尝试进行预订。
- **模式 3: 自定义预订测试**: 允许用户自定义日期和时间进行预订测试。

### 3. 测试输出示例

```
🚀 开始全面测试，正在连接到: http://localhost:3001/sse
✅ 连接成功！发现 5 个可用工具。将依次调用...

--- 正在调用工具: booking_get_field_info ---
   参数: {'field': 'badminton', ...}

✅ booking_get_field_info 调用成功！结果预览:
---
场地信息:
场地名称: badminton
场地ID: 1097
...
---

🏁 所有工具调用完毕，全面测试结束！
```

## 📡 API 接口

### 可用工具列表

| 工具名称 | 描述 | 主要参数 | 缓存时间 |
|---------|------|----------|----------|
| `booking_get_field_info` | 获取场地信息和当天所有预订 | `field`, `start_time`, `end_time` | 10分钟 |
| `booking_get_available_places` | 查询指定时间段的可用场地 | `field`, `check_start_time`, ... | 5分钟 |
| `booking_book` | 预订一个场地 | `field_id`, `place_id`, `start_time`, ... | 不缓存 |
| `booking_clear_cache` | 清除所有工具的缓存 | 无 | - |
| `booking_force_relogin` | 强制系统重新登录 | 无 | - |

### 响应格式
所有工具都返回格式化的字符串。如果发生错误，错误信息也会包含在返回的字符串中。

## 🔧 故障排除

### 常见问题

#### 1. 登录失败或测试返回 "environment variables must be set"
- **原因**: Docker 容器没有正确加载到环境变量。
- **解决方案**:
  1. 确认 `BOOKING-MCP` 根目录下存在 `.env` 文件。
  2. 确认 `.env` 文件中 `BOOKING_USERNAME` 和 `BOOKING_PASSWORD` 已被正确填写。
  3. 重启容器：`docker-compose down && docker-compose up --build -d`。

#### 2. 测试脚本连接失败
- **原因**: 无法从本地连接到 Docker 容器中的服务。
- **解决方案**:
  1. 确认 Docker 服务正在运行: `docker-compose ps`。
  2. 确认端口 `3001` 没有被其他程序占用。
  3. 查看容器日志寻找错误信息: `docker-compose logs booking-mcp`。

#### 3. 启动时报错 "Error: BOOKING_USERNAME and BOOKING_PASSWORD must be provided"

**症状**: 服务无法启动，并显示凭证缺失的错误。
**解决方案**:
- 确保项目根目录中存在 `.env` 文件，并且其中包含了 `BOOKING_USERNAME` 和 `BOOKING_PASSWORD`。对于 Docker 部署，这是推荐的方式。
- 对于本地开发或调试，也可以在运行 `mcp-server-booking` 命令时，使用 `--username` 和 `--password` 参数提供凭证。

## 📄 许可证与免责声明

- **许可证**: 本项目采用 MIT 许可证。
- **免责声明**: 本项目仅供学习和技术研究使用。所有操作均为用户真实意图的体现，请遵守学校的相关规定。 