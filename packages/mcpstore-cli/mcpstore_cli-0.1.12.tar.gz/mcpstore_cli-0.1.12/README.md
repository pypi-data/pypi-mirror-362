# 🚀 mcpstore-cli

**English | [中文说明](#中文说明)**

---

## Overview

`mcpstore-cli` is a powerful Python CLI tool for managing and proxying Model Context Protocol (MCP) servers. It provides a unified registry, installation, configuration, and proxy solution for AI agent developers. Supports MCP servers from PyPI, NPM, GitHub, Docker, and more.

- 🔍 **Registry Search**: Discover MCP servers from multiple sources
- 📦 **One-Click Install**: Install and configure servers for various clients
- 🛠️ **Proxy Mode**: Run as a transparent MCP proxy
- 🌐 **Multi-Source**: Supports PyPI, NPM, GitHub, Docker
- 🎨 **Rich CLI**: Beautiful, interactive command line interface

---

## Quick Start

### Installation

```bash
pip install mcpstore-cli
```

Or use [uv](https://github.com/astral-sh/uv):

```bash
uv pip install mcpstore-cli
```

### Basic Usage

#### Search for MCP servers
```bash
mcpstore-cli search weather
```

#### Show server info
```bash
mcpstore-cli info @turkyden/weather
```

#### Install server to client
```bash
mcpstore-cli install @turkyden/weather --client cursor --key <your-api-key>
```

#### List installed servers
```bash
mcpstore-cli list --client cursor
```

#### Run as MCP proxy
```bash
mcpstore-cli run @turkyden/weather --key <your-api-key>
```

---

## Configuration

- **Config file**: `~/.mcpstore/config.toml`
- **Environment variables**: `MCPSTORE_REGISTRY_URL`, `MCPSTORE_API_KEY`, etc.
- **Clients supported**: Cursor, Claude Desktop, VS Code, Custom

Example config:
```toml
[registry]
url = "https://registry.mcpstore.dev"
api_key = "your-api-key"

[proxy]
host = "127.0.0.1"
port = 8080
```

---

## Architecture

- **Proxy Mode**: Acts as a transparent proxy between MCP client and server
- **Registry**: Aggregates servers from PyPI, NPM, GitHub, Docker
- **CLI**: Rich, interactive, multi-language

---

## FAQ

**Q: How to publish my own MCP server?**
A: Publish to PyPI/NPM/GitHub/Docker, then register via `mcpstore-cli`.

**Q: How to use with Cursor/Claude/VSCode?**
A: Use `install` command to configure the client automatically.

**Q: How to update?**
A: `pip install --upgrade mcpstore-cli` or `uv pip install --upgrade mcpstore-cli`

---

# 中文说明

## 简介

`mcpstore-cli` 是一款面向 AI 智能体开发者的 Python 命令行工具，支持 MCP 服务器的注册、发现、安装、配置和代理。支持 PyPI、NPM、GitHub、Docker 多源服务器。

- 🔍 **注册表搜索**：多源发现 MCP 服务器
- 📦 **一键安装**：自动安装配置到各类客户端
- 🛠️ **代理模式**：透明代理 MCP 通信
- 🌐 **多源支持**：PyPI/NPM/GitHub/Docker
- 🎨 **美观 CLI**：交互式命令行体验

---

## 快速开始

### 安装

```bash
pip install mcpstore-cli
```

或使用 uv：

```bash
uv pip install mcpstore-cli
```

### 基本用法

#### 搜索服务器
```bash
mcpstore-cli search weather
```

#### 查看服务器信息
```bash
mcpstore-cli info @turkyden/weather
```

#### 安装服务器到客户端
```bash
mcpstore-cli install @turkyden/weather --client cursor --key <你的API密钥>
```

#### 列出已安装服务器
```bash
mcpstore-cli list --client cursor
```

#### 代理运行服务器
```bash
mcpstore-cli run @turkyden/weather --key <你的API密钥>
```

---

## 配置

- **配置文件**：`~/.mcpstore/config.toml`
- **环境变量**：`MCPSTORE_REGISTRY_URL`、`MCPSTORE_API_KEY` 等
- **支持客户端**：Cursor、Claude Desktop、VS Code、自定义

配置示例：
```toml
[registry]
url = "https://registry.mcpstore.dev"
api_key = "your-api-key"

[proxy]
host = "127.0.0.1"
port = 8080
```

---

## 架构说明

- **代理模式**：作为 MCP 客户端与服务器之间的透明代理
- **注册表聚合**：支持 PyPI/NPM/GitHub/Docker 多源
- **命令行交互**：支持中英文

---

## 常见问题

**Q: 如何发布自己的 MCP 服务器？**
A: 发布到 PyPI/NPM/GitHub/Docker 后，用 mcpstore-cli 注册。

**Q: 如何与 Cursor/Claude/VSCode 配合？**
A: 用 `install` 命令自动配置。

**Q: 如何升级？**
A: `pip install --upgrade mcpstore-cli` 或 `uv pip install --upgrade mcpstore-cli`

---

## 贡献与支持

- GitHub: https://github.com/xray918/mcpstore-cli
- Issues: https://github.com/xray918/mcpstore-cli/issues

---

> mcpstore-cli © 2024 xray918. MIT License. 