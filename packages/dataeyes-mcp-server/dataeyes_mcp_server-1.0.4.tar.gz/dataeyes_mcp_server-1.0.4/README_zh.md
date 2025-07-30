# DataEyes MCP 服务

[![PyPI version](https://img.shields.io/pypi/v/dataeyes-mcp-server.svg)](https://pypi.org/project/dataeyes-mcp-server/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

本项目由[数眼智能](https://shuyanai.com)提供支持，是一个 MCP (Machine-Comprehensible Protocol) 服务。它提供了一系列工具（例如网页内容读取），以增强 AI Agent 的能力。

## 🤔 MCP 是什么？

MCP (Machine-Comprehensible Protocol) 是一种专为 AI Agent（智能体）与工具之间通信而设计的协议。它规范了智能体如何发现工具的能力以及如何调用它们，从而实现了不同 AI 系统与服务之间的无缝集成。

## ✨ 功能特性

- **标准化协议**: 完全兼容 MCP 标准，易于集成。
- **云端与自托管选项**: 提供稳定、高性能的云端 SSE 服务，以及灵活的自托管命令行工具。
- **可扩展的工具集**: 提供不断扩展的工具套件。

## 🛠️ 可用工具

本服务提供了一套可以通过 MCP 协议调用的工具。

### 📖 reader

`reader` 工具可以访问一个网页链接，并以干净、对大语言模型友好的 Markdown 格式返回其正文内容。

**参数:**

- `url` (字符串, 必需): 需要读取的网页链接。
- `timeout` (整数, 可选, 默认: 30): 页面加载超时时间，单位为秒 (范围: 1-60)。

## 🚀 快速开始

### 1. 获取您的 API KEY

使用数眼智能的服务需要一个 API KEY。

**官方网址**: [https://shuyanai.com](https://shuyanai.com)

请前往官网注册登录后，获取您的专属 API KEY。

### 2. 选择您的使用方式

#### A 方案: 使用云端 SSE 服务 (推荐)

这是最简单的入门方式。只需将您的 AI Agent 指向我们托管的 SSE (Server-Sent Events) 端点即可。

**端点 URL**:
```
https://mcp.shuyanai.com/sse?key=你的_API_KEY
```
请记得将 `你的_API_KEY` 替换为您获取的密钥。

#### B 方案: 通过命令行自托管

如果您希望在本地运行服务，可以将其作为命令行工具进行安装。

**a. 安装**

我们推荐使用 `uv` 在隔离环境中安装和运行本工具。

```bash
# 如果您还未安装 uv，请先执行此命令
pip install uv

# 使用 uvx 运行服务
uvx dataeyes-mcp-server
```

**b. 配置环境变量**

对于自托管方式，服务会从 `DATAEYES_API_KEY` 环境变量中读取 API KEY。

- **对于 macOS/Linux:**
  ```bash
  export DATAEYES_API_KEY='你的_api_key'
  ```
- **对于 Windows:**
  ```powershell
  setx DATAEYES_API_KEY "你的_api_key"
  ```
> 注意: 您可能需要重启终端才能让环境变量生效。

设置好环境变量后，运行 `uvx dataeyes-mcp-server` 即可启动服务，它将通过 stdio 进行通信。

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 发布。
