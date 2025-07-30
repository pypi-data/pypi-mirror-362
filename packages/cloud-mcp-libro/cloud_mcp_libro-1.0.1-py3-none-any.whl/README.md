# Cloud Platform MCP Server

一个用于访问云平台后台接口的MCP（Model Context Protocol）服务器，已修复中文乱码问题。

## 🔧 修复的问题

✅ **中文乱码问题已解决**
- 使用英文日志消息，完全避免编码问题
- 正确设置UTF-8编码
- 确保在所有MCP客户端中正常显示

✅ **JSON通信问题已解决**
- 修复了MCP协议JSON解析错误
- 日志输出重定向到stderr，避免污染JSON通信
- 移除了可能干扰MCP协议的print语句

## ⚡ 快速开始

1. **配置环境**：
   ```bash
   # 复制配置文件
   copy .env.example .env
   # 编辑 .env 文件填写你的配置
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务器**：
   ```bash
   # Windows (推荐)
   start.bat
   
   # 或直接运行
   python server.py
   ```

## 🔧 配置

在 `.env` 文件中配置：

### 必需配置
```env
CLOUD_BASE_URL=http://your-server:8080
CLOUD_USERNAME=your-email@example.com  
CLOUD_PASSWORD=your-password
```

### 可选配置
```env
# 地区和时区
CLOUD_TIMEZONE=Asia/Shanghai
CLOUD_COUNTRY=China

# 应用标识信息（使用默认值即可）
CLOUD_APP_SN=eeec1ea2b23b11e1234
CLOUD_APP_ID=1
CLOUD_PHONE_BRAND=IOS
CLOUD_PHONE_SYSTEM=1
CLOUD_PHONE_SYSTEM_VERSION=1
```

## 🛠️ 可用功能

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