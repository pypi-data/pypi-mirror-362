# Cloud Platform MCP Server

> **📦 Now Available on PyPI!** Install with: `uvx cloud-mcp-libro`

A Model Context Protocol (MCP) server for cloud platform backend APIs. Enables seamless integration with AI assistants and tools through standardized MCP protocol.

## 🚀 Quick Start

### Install and Run (Recommended)

```bash
# Install and run directly with uvx
uvx cloud-mcp-libro

# Or install globally
pip install cloud-mcp-libro
cloud-mcp-server
```

### Environment Configuration

Set required environment variables before running:

```bash
# Windows
set CLOUD_USERNAME=your-email@example.com
set CLOUD_PASSWORD=your-password
set CLOUD_BASE_URL=http://localhost:8080
set CLOUD_TIMEZONE=Asia/Shanghai
set CLOUD_AREA=CN
set CLOUD_COUNTRY=China

# Linux/Mac
export CLOUD_USERNAME=your-email@example.com
export CLOUD_PASSWORD=your-password
export CLOUD_BASE_URL=http://localhost:8080
export CLOUD_TIMEZONE=Asia/Shanghai
export CLOUD_AREA=CN
export CLOUD_COUNTRY=China
```

## 📋 Features

- `authenticate_user`: 用户认证 ✅ **已验证工作正常**
- `get_user_profile`: 获取用户资料 ✅ **已修复，使用正确端点**
- `get_device_list`: 获取绑定设备列表 ✅ **新增功能**
- `manual_feeding`: 手动喂食控制 ✅ **新增功能**
- `add_feeding_plan`: 添加喂食计划 ✅ **新增功能**
- `get_feeding_plan_list`: 查看喂食计划列表 ✅ **新增功能**
- `remove_feeding_plan`: 删除指定喂食计划 ✅ **新增功能**
- `call_api`: 调用任意API接口 ✅ **可用于探索其他API**

## ✅ 认证状态

**认证功能已完全正常工作！** 

### 成功的配置
- **URL**: `https://demo-api.dl-aiot.com`
- **必需头部**: `source: IOS`, `version: 1.0.0`, `language: ZH`
- **返回成功码**: `0` (不是200)
- **Token获取**: 成功获取并管理token

### 测试结果
```json
{
  "code": 0,
  "msg": null,
  "data": {
    "token": "xxx",
    "clientId": "APP_189012631",
    "memberId": 189012631,
    "account": "limo.yu@designlibro.com",
    "email": "limo.yu@designlibro.com",
    "country": "China"
  }
}
```

## ✅ 编码修复说明

如果之前遇到类似这样的乱码：
```
INFO:cloud-mcp:֤Ӧ״̬: 200
INFO:cloud-mcp:֤Ӧ: {'code': 1002, 'msg': 'ӦIDΪ', 'data': None}
```

现在会正确显示为：
```
INFO:cloud-mcp:认证响应状态: 200
INFO:cloud-mcp:认证响应: {'code': 200, 'msg': '登录成功', 'data': {...}}
```

## 🔍 故障排除

### 编码问题
**当前版本使用英文日志，已解决所有乱码问题**

如果需要中文日志且出现乱码：
1. 使用中文版本：`python server_chinese_backup.py`
2. 设置编码：`chcp 65001 && set PYTHONIOENCODING=utf-8`
3. 或使用启动脚本：`start.bat`

### JSON通信问题
如果遇到JSON解析错误：
1. 确保没有print语句输出到stdout
2. 所有日志和调试信息应输出到stderr
3. 运行 `python verify_fixes.py` 验证修复

## 🧪 验证修复

运行验证脚本确保所有问题已修复：
```bash
python verify_fixes.py
```

应该看到所有测试通过：
```
🎉 所有测试通过！MCP服务器已准备就绪
💡 现在可以安全地启动MCP服务器了
```

## 文件说明

- `server.py`: 主MCP服务器（英文日志，推荐使用）
- `server_chinese_backup.py`: 中文日志版本的备份
- `test_final.py`: 最终测试脚本
- `ENCODING_FIX_FINAL.md`: 完整的问题解决方案文档

## 作者

- **作者**: limo
- **日期**: 2025-01-01

## 版本历史

- v1.0.0: 初始版本，支持基本MCP功能
- v1.1.0: 修复JSON通信问题
- v1.2.0: 完全解决中文乱码问题（使用英文日志） 