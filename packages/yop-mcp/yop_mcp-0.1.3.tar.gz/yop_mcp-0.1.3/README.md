# YOP MCP Server

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Build Status](https://github.com/yop-platform/yop-mcp/workflows/Python%20package/badge.svg)](https://github.com/yop-platform/yop-mcp/actions)
[![Code Quality](https://github.com/yop-platform/yop-mcp/workflows/CodeQL/badge.svg)](https://github.com/yop-platform/yop-mcp/actions)
[![MCP](https://img.shields.io/badge/MCP-Server-orange.svg)](https://modelcontextprotocol.io/)

> 🚀 快速对接易宝支付开放平台(YOP)的 MCP Server

## 📖 简介

**yop-mcp** 是一个专为易宝支付开放平台(YOP)设计的 MCP (Model Context Protocol) Server，提供了一套完整的工具函数，帮助开发者通过AI助手（如Claude、Cursor等）更便捷地获取YOP平台的相关信息、生成密钥对、下载证书等操作。

### ✨ 核心特性

- 🔧 **10个专业工具函数** - 覆盖平台概览、产品详情、API文档、SDK指南等
- 🔐 **密钥管理** - 支持RSA/SM2算法的密钥对生成和证书下载
- 📚 **智能文档获取** - 自动获取最新的API文档和产品信息
- 🛡️ **安全可靠** - 内置容错机制和安全验证
- 🚀 **即插即用** - 与主流AI开发工具无缝集成

## 🛠️ 功能特点

该 MCP Server 提供以下工具函数：

### 📋 平台信息获取

1. **yeepay_yop_overview()** - 获取易宝支付开放平台(YOP)的平台规范、产品概览、接入流程和对接工具信息
2. **yeepay_yop_product_overview()** - 获取易宝支付开放平台(YOP)的所有产品的概览信息
3. **yeepay_yop_product_detail_and_associated_apis(product_code)** - 获取指定产品的介绍、使用说明和相关 API 接口列表
4. **yeepay_yop_api_detail(api_uri)** - 获取指定 API 接口的详细定义，包括基本信息、请求参数、响应参数、示例代码等

### 📚 文档和SDK指南

1. **yeepay_yop_java_sdk_user_guide()** - 获取易宝支付开放平台(YOP)的 yop-java-sdk 使用说明
2. **yeepay_yop_sdk_and_tools_guide()** - 获取易宝支付开放平台(YOP)提供的各种SDK和工具的使用说明
3. **yeepay_yop_link_detail(url)** - 获取易宝支付开放平台(YOP)的各个子页面或外部链接的详细内容

### 🔐 密钥和证书管理

1. **yeepay_yop_gen_key_pair(algorithm, format, storage_type)** - 生成非对称加密的密钥对
2. **yeepay_yop_download_cert(algorithm, serial_no, auth_code, private_key, public_key, pwd)** - 下载CFCA证书
3. **yeepay_yop_parse_certificates(algorithm, pfxCert, pubCert, pwd)** - 解析证书文件获取公钥或私钥字符串

## 📋 环境要求

- **Python**: 3.10 或更高版本
- **包管理器**: uv（推荐）或 pip
- **操作系统**: Windows / macOS / Linux

## 🚀 快速开始

### 方式一：直接使用 uvx（推荐）

**1. 安装 uv**

**Windows:**

```bash
pip install uv
```

**Linux/Mac:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. 直接运行**

```bash
uvx yop-mcp
```

这将自动从 PyPI 下载并运行最新版本的 yop-mcp。

### 方式二：从源码安装

**1. 获取代码**

```bash
git clone http://gitlab.yeepay.com/yop/yop-mcp.git
cd yop-mcp
```

**2. 安装依赖**

```bash
uv sync  # 这将创建虚拟环境并安装所需的包
```

**3. 运行服务器**

```bash
uv run yop_mcp/main.py
```

服务器启动后，您将看到类似以下的输出：

```text
MCP Server started on stdio transport
```

## 🔧 在 AI 工具中配置

### 方式一：使用 uvx（推荐）

#### Cursor 配置

```json
{
  "mcpServers": {
    "yop-mcp": {
      "command": "uvx",
      "args": ["yop-mcp"],
      "timeout": 600,
      "autoApprove": [
        "yeepay_yop_overview",
        "yeepay_yop_product_overview",
        "yeepay_yop_product_detail_and_associated_apis",
        "yeepay_yop_api_detail",
        "yeepay_yop_java_sdk_user_guide",
        "yeepay_yop_sdk_and_tools_guide",
        "yeepay_yop_link_detail",
        "yeepay_yop_gen_key_pair",
        "yeepay_yop_download_cert",
        "yeepay_yop_parse_certificates"
      ]
    }
  }
}
```

#### Claude Desktop 配置

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "yop-mcp": {
      "command": "uvx",
      "args": ["yop-mcp"]
    }
  }
}
```

### 方式二：从源码运行

如果您选择从源码安装，请使用以下配置：

#### Cursor 配置

请记得将路径 `/Users/your-username/path/to/yop-mcp` 更改为您系统上实际克隆仓库的路径。

```json
{
  "mcpServers": {
    "yop-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/your-username/path/to/yop-mcp",
        "run",
        "yop_mcp/main.py"
      ],
      "timeout": 600,
      "autoApprove": [
        "yeepay_yop_overview",
        "yeepay_yop_product_overview",
        "yeepay_yop_product_detail_and_associated_apis",
        "yeepay_yop_api_detail",
        "yeepay_yop_java_sdk_user_guide",
        "yeepay_yop_sdk_and_tools_guide",
        "yeepay_yop_link_detail",
        "yeepay_yop_gen_key_pair",
        "yeepay_yop_download_cert",
        "yeepay_yop_parse_certificates"
      ]
    }
  }
}
```

#### Claude Desktop 配置

```json
{
  "mcpServers": {
    "yop-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/yop-mcp", "run", "yop_mcp/main.py"]
    }
  }
}
```

## 📚 API 文档

### 1. yeepay_yop_overview()

获取易宝支付开放平台(YOP)的概览信息，包括平台规范、产品概览、接入流程和对接工具等信息。

**示例调用：**

```python
yeepay_yop_overview()
```

**返回：** YOP 平台概览信息（markdown 格式）

### 2. yeepay_yop_product_overview()

获取易宝支付开放平台(YOP)的所有产品的概览信息。

**示例调用：**

```python
yeepay_yop_product_overview()
```

**返回：** YOP 平台所有产品的概览信息（markdown 格式）

### 3. yeepay_yop_product_detail_and_associated_apis(product_code)

获取指定产品的介绍、使用说明和相关 API 接口列表。

**参数：**

- `product_code`（字符串）- 产品编码，产品的唯一标识

**示例调用：**

```python
yeepay_yop_product_detail_and_associated_apis("user-scan")
```

**返回：** 指定产品的介绍、使用说明和相关 API 接口列表（markdown 格式）

### 4. yeepay_yop_api_detail(api_uri)

获取指定 API 接口的详细定义，包含基本信息、请求参数、请求示例、响应参数、响应示例、错误码、回调、示例代码等信息。

**参数：**
- `api_uri`（字符串）- API 的 URI 路径，支持以下格式：
  - `/rest/v1.0/aggpay/pre-pay`
  - `https://open.yeepay.com/docs-v3/api/post_rest_v1.0_aggpay_pre-pay.md`
  - `https://open.yeepay.com/docs-v2/apis/user-scan/post__rest__v1.0__aggpay__pre-pay/index.html`

**示例调用：**
```
yeepay_yop_api_detail("/rest/v1.0/aggpay/pre-pay")
```

**返回：** API 接口的详细定义信息（markdown 格式）

### 5. yeepay_yop_java_sdk_user_guide()

获取易宝支付开放平台(YOP)的 yop-java-sdk 使用说明。

**示例调用：**
```
yeepay_yop_java_sdk_user_guide()
```

**返回：** yop-java-sdk 使用说明（markdown 格式）

### 6. yeepay_yop_sdk_and_tools_guide()

获取易宝支付开放平台(YOP)提供的各种SDK和工具的使用说明，以及对接最佳实践等。

**示例调用：**
```
yeepay_yop_sdk_and_tools_guide()
```

**返回：** SDK和工具的使用说明（markdown 格式）

### 7. yeepay_yop_link_detail(url)

获取易宝支付开放平台(YOP)的各个子页面或外部链接的详细内容。

**参数：**
- `url`（字符串）- 易宝支付开放平台(YOP)的子页面的URL地址

**示例调用：**
```
yeepay_yop_link_detail("https://open.yeepay.com/docs-v3/platform/201.md")
```

**返回：** 子页面的详细内容（markdown 格式）

### 8. yeepay_yop_gen_key_pair(algorithm, format, storage_type)

根据密钥算法生成非对称加密的密钥对（公钥和私钥），并保存到本地路径。

**参数：**
- `algorithm`（字符串）- 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
- `format`（字符串）- 密钥格式，可选值为 "pkcs8"或"pkcs1"，默认为 "pkcs8"
- `storage_type`（字符串）- 密钥存储类型，"file"或"string"，默认为 "file"

**示例调用：**
```
yeepay_yop_gen_key_pair(algorithm="SM2", format="pkcs8", storage_type="file")
```

**返回：** 生成的密钥对信息

### 9. yeepay_yop_download_cert(algorithm, serial_no, auth_code, private_key, public_key, pwd)

根据密钥算法、CFCA证书的序列号、授权码、非对称密钥对（公钥和私钥）、密码，下载该证书，并保存到本地路径。

**参数：**
- `algorithm`（字符串）- 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
- `serial_no`（字符串）- cfca证书序列号
- `auth_code`（字符串）- cfca证书授权码
- `private_key`（字符串）- Base64 编码后的私钥字符串
- `public_key`（字符串）- Base64 编码后的公钥字符串
- `pwd`（字符串）- 密码，长度：12~16位

**返回：**
```json
{
    "message": "响应信息",
    "pfxCert": "私钥证书路径(.pfx)",
    "pubCert": "公钥证书路径(.cer)"
}
```

### 10. yeepay_yop_parse_certificates(algorithm, pfxCert, pubCert, pwd)

根据证书文件解析出Base64编码后的公钥或私钥字符串。

**参数：**
- `algorithm`（字符串）- 密钥算法，可选值为 "RSA" 或 "SM2"，默认为 "RSA"
- `pfxCert`（字符串）- 私钥证书（.pfx）文件路径
- `pubCert`（字符串）- 公钥证书（.cer）文件路径
- `pwd`（字符串）- PFX证书的密码，默认为None

**返回：**
```json
{
    "message": "响应信息",
    "privateKey": "Base64编码后的私钥字符串",
    "publicKey": "Base64编码后的公钥字符串"
}
```

## ❓ 常见问题

### 如何查找产品编码？

可以通过调用 `yeepay_yop_product_overview()` 获取产品概览，从中找到需要的产品编码。

### 如何获取完整的 API 列表？

先通过 `yeepay_yop_product_overview()` 获取产品编码，然后调用 `yeepay_yop_product_detail_and_associated_apis(product_code)` 获取特定产品的 API 列表。

### 接口返回错误怎么办？

系统已内置容错机制，如果特定接口请求失败，会尝试备用地址获取信息。

### 如何在不同的AI工具中使用？

本项目支持所有兼容MCP协议的AI工具，包括但不限于：
- Claude Desktop
- Cursor
- 其他支持MCP的AI开发工具

## ⚠️ 注意事项

- 所有接口返回的数据均为 markdown 格式，方便直接展示
- 确保网络连接正常，能够访问易宝支付开放平台
- 密钥和证书操作涉及敏感信息，请妥善保管
- 建议在测试环境中先验证功能后再在生产环境使用

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 开发指南

1. 确保您的代码符合项目的编码规范
2. 添加适当的测试用例
3. 更新相关文档
4. 确保所有测试通过

## 📄 许可证

本项目采用 [Apache License 2.0](LICENSE) 许可证。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

## 📞 支持

如果您在使用过程中遇到问题，可以通过以下方式获取帮助：

- 提交 [Issue](http://gitlab.yeepay.com/yop/yop-mcp/-/issues)
- 查看 [易宝支付开放平台文档](https://open.yeepay.com/)
- 联系技术支持

## 🔗 相关链接

- [易宝支付开放平台](https://open.yeepay.com/)
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)
- [Cursor](https://cursor.sh/)

---

*Made with ❤️ by YOP Team*
