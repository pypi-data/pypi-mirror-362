# DataEyes MCP Service

[![PyPI version](https://img.shields.io/pypi/v/dataeyes-mcp-server.svg)](https://pypi.org/project/dataeyes-mcp-server/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[中文版说明](README_zh.md)

This project provides an MCP (Machine-Comprehensible Protocol) service powered by [DataEyes Intelligence](https://shuyanai.com). It exposes a series of tools (e.g., web content reading) to enhance the capabilities of AI Agents.

## 🤔 What is MCP?

MCP (Machine-Comprehensible Protocol) is a protocol designed for communication between AI Agents and tools. It standardizes how an agent discovers the capabilities of a tool and how it invokes them, enabling seamless integration between different AI systems and services.

## ✨ Features

- **Standardized Protocol**: Fully compatible with the MCP standard for easy integration.
- **Hosted & Self-Hosted Options**: Provides a stable, high-performance hosted SSE service and a self-hosted CLI for flexibility.
- **Extensible Toolset**: Offers an expanding suite of tools.

## 🛠️ Available Tools

This service provides a set of tools that can be invoked through the MCP protocol.

### 📖 reader

The `reader` tool can access a web page URL and return the main content in a clean, LLM-friendly Markdown format.

**Parameters:**

- `url` (string, required): The URL of the web page to read.
- `timeout` (integer, optional, default: 30): The page load timeout in seconds (range: 1-60).

## 🚀 Getting Started

### 1. Obtain Your API KEY

An API KEY is required to use the DataEyes services.

**Official Website**: [https://shuyanai.com](https://shuyanai.com)

Please register and log in to obtain your exclusive API KEY.

### 2. Choose Your Usage Method

#### Option A: Hosted SSE Service (Recommended)

This is the easiest way to get started. Just point your AI Agent to our hosted SSE (Server-Sent Events) endpoint.

**Endpoint URL**:
```
https://mcp.shuyanai.com/sse?key=YOUR_API_KEY
```
Remember to replace `YOUR_API_KEY` with the key you obtained.

#### Option B: Self-Hosting via CLI

If you prefer to run the server locally, you can install it as a command-line tool.

**a. Installation**

We recommend using `uv` to install and run the tool in an isolated environment.

```bash
# First, install uv if you don't have it
pip install uv

# Run the server using uvx
uvx dataeyes-mcp-server
```

**b. Environment Variable**

For self-hosting, the server reads the API KEY from the `DATAEYES_API_KEY` environment variable.

- **For macOS/Linux:**
  ```bash
  export DATAEYES_API_KEY='your_api_key'
  ```
- **For Windows:**
  ```powershell
  setx DATAEYES_API_KEY "your_api_key"
  ```
> Note: You may need to restart your terminal for the changes to take effect.

Once the environment variable is set, you can run `uvx dataeyes-mcp-server` to start the service, which will communicate via stdio.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
