<p align="center">
  <img src="logo.jpg" alt="TraceHunter-CLI Logo" width="120" height="120">
</p>

<h1 align="center">TraceHunter-CLI</h1>

<p align="center">
  <strong>Lightweight Terminal Username Digital Footprint Tracking Engine</strong><br>
  轻量级终端用户名数字足迹智能追踪引擎
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Dependencies-0-success.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Sites-275+-orange.svg" alt="275+ Sites">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Cross Platform">
  <img src="https://img.shields.io/badge/Release-v1.0.0-brightgreen.svg" alt="Release">
</p>

<p align="center">
  <a href="#-project-introduction">Introduction</a> |
  <a href="#-core-features">Features</a> |
  <a href="#-quick-start">Quick Start</a> |
  <a href="#-usage-guide">Usage Guide</a> |
  <a href="#-design-philosophy">Design</a> |
  <a href="#--contributing">Contributing</a> |
  <a href="#--license">License</a>
</p>

---

## [中文] 项目介绍

TraceHunter-CLI 是一款轻量级终端用户名数字足迹追踪工具，仅使用 Python 标准库实现，**零外部依赖**。输入一个用户名，即可在 **275+ 个精选网站**上搜索该用户名的账户，自动评估信息泄露风险等级，生成多格式报告。

### 为什么选择 TraceHunter-CLI？

| 特性 | TraceHunter-CLI | 其他工具 |
|------|----------------|---------|
| 外部依赖 | **0** | 30+ |
| 安装方式 | pip / 单文件 | Docker / 编译 |
| 站点覆盖 | 275+ 精选 | 3000+ 但臃肿 |
| 风险评分 | **内置** | 无 |
| 报告格式 | 终端/JSON/HTML | 多但复杂 |
| 启动速度 | **秒级** | 分钟级 |

## ✨ 核心特性

- **零依赖** - 纯 Python 3.8+ 标准库，无需安装任何第三方包
- **275+ 精选站点** - 覆盖社交、技术、媒体、游戏、金融、教育等 9 大类别
- **多线程搜索** - 可配置并发数（默认 20 线程），快速扫描
- **风险评分系统** - 自动评估每个发现账户的信息泄露风险（0-100 分）
- **多格式报告** - 终端彩色输出、JSON、HTML 三种格式
- **分类过滤** - 按类别筛选目标站点，精准搜索
- **代理支持** - 支持 HTTP/SOCKS5 代理
- **跨平台** - Windows、Linux、macOS 全平台兼容
- **中国站点支持** - 内置微博、B站、知乎、掘金、CSDN 等国内平台

## 🚀 快速开始

### 安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/gitstq/TraceHunter-CLI.git

# 或克隆后本地安装
git clone https://github.com/gitstq/TraceHunter-CLI.git
cd TraceHunter-CLI
pip install .
```

### 基本使用

```bash
# 搜索用户名
tracehunter -u johndoe

# 搜索特定类别
tracehunter -u johndoe --categories social,tech

# 排除某些类别
tracehunter -u johndoe --exclude-categories gaming

# 导出 HTML 报告
tracehunter -u johndoe --output-html report.html

# 导出 JSON 报告
tracehunter -u johndoe --output-json result.json

# 使用代理
tracehunter -u johndoe --proxy socks5://127.0.0.1:1080

# 调整并发数和超时
tracehunter -u johndoe --workers 50 --timeout 15

# 查看所有可用站点
tracehunter --list-sites

# 查看版本
tracehunter --version
```

## 📖 详细使用指南

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--username` | `-u` | 目标用户名 | 必填 |
| `--proxy` | `-p` | 代理 URL (http/socks5) | 无 |
| `--timeout` | `-t` | 请求超时（秒） | 10 |
| `--workers` | `-w` | 最大并发线程数 | 20 |
| `--categories` | `-c` | 包含的站点类别（逗号分隔） | 全部 |
| `--exclude-categories` | `-e` | 排除的站点类别（逗号分隔） | 无 |
| `--output-json` | | 导出 JSON 文件路径 | 无 |
| `--output-html` | | 导出 HTML 文件路径 | 无 |
| `--list-sites` | | 列出所有站点并退出 | - |
| `--version` | | 显示版本号 | - |

### 站点类别

| 类别 | 说明 | 示例站点 |
|------|------|---------|
| `social` | 社交媒体 | Twitter, Instagram, Facebook, 微博 |
| `tech` | 技术开发 | GitHub, GitLab, StackOverflow, 掘金 |
| `media` | 内容媒体 | YouTube, Spotify, Medium, B站 |
| `gaming` | 游戏娱乐 | Steam, Twitch, Roblox, Discord |
| `finance` | 金融商业 | Buy Me a Coffee, Ko-fi, Gumroad |
| `education` | 教育研究 | LeetCode, Kaggle, Coursera |
| `forum` | 论坛社区 | Reddit, Quora, Product Hunt, 知乎 |
| `shopping` | 购物市场 | Amazon, eBay, Etsy |
| `other` | 其他平台 | Goodreads, Strava, TripAdvisor |

### 风险评分说明

| 分数范围 | 风险等级 | 说明 |
|---------|---------|------|
| 80-100 | CRITICAL | 极高风险，暴露大量敏感个人信息 |
| 60-79 | HIGH | 高风险，存在显著信息泄露 |
| 40-59 | MEDIUM | 中等风险，有一定信息暴露 |
| 20-39 | LOW | 低风险，信息暴露有限 |
| 0-19 | MINIMAL | 最低风险，几乎无信息暴露 |

### 输出示例

```
  ╔══════════════════════════════════════════════════════╗
  ║     TraceHunter-CLI v1.0.0                        ║
  ║     Lightweight Username Digital Footprint Tracker ║
  ╚══════════════════════════════════════════════════════╝

  [*] Searching for username: johndoe
  [*] Scanning sites...

  ═══════════════════════════════════════════════════════════════
    DIGITAL FOOTPRINT ASSESSMENT
  ═══════════════════════════════════════════════════════════════
    Username:    johndoe
    Overall Risk: HIGH (72/100)
    Accounts:    15 found
    High Risk:   4
  ═══════════════════════════════════════════════════════════════
```

## 💡 设计思路与迭代规划

### 设计理念

1. **极简主义** - 零外部依赖，一个 pip install 即可使用
2. **精选优于海量** - 275 个精选高价值站点，胜过 3000 个低质量签名
3. **安全意识** - 内置风险评分，帮助用户了解自己的数字足迹
4. **速度优先** - 多线程 + 智能调度，默认 30 秒内完成扫描

### 迭代规划

- [x] v1.0.0 - 核心搜索功能 + 风险评分 + 多格式报告
- [ ] v1.1.0 - 递归关联搜索（从已发现账户提取新用户名）
- [ ] v1.2.0 - 搜索历史对比（多次扫描差异分析）
- [ ] v1.3.0 - Web UI 界面
- [ ] v2.0.0 - AI 分析模式（LLM 集成，生成调查摘要）

## 📦 打包与部署指南

### 作为 Python 包使用

```python
from tracehunter_cli.engine import TraceHunter
from tracehunter_cli.risk_scorer import RiskScorer

# 创建搜索实例
hunter = TraceHunter(
    username="target_user",
    timeout=10,
    max_workers=20,
    categories=["social", "tech"],
)

# 执行搜索
results = hunter.search()

# 风险评分
scorer = RiskScorer()
scored = scorer.score_all(results)

# 获取统计
stats = hunter.get_stats()
print(f"Found: {stats['found']}/{stats['total']}")
```

### 开发模式安装

```bash
git clone https://github.com/gitstq/TraceHunter-CLI.git
cd TraceHunter-CLI
pip install -e .
```

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 添加新站点

编辑 `tracehunter_cli/sites_db.py`，在 `SITES` 列表中添加新条目：

```python
{
    "name": "sitename",
    "category": "social",
    "url": "https://example.com/{username}",
    "presence_strs": ["account exists indicator"],
    "absence_strs": ["account not found indicator"],
    "method": "html",
    "tags": ["tag1", "tag2"],
}
```

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<p align="center">
  <strong>[English]</strong> | <a href="README.zh-TW.md">繁體中文</a> | <a href="README.ja.md">日本語</a>
</p>

---

## [English] Project Introduction

TraceHunter-CLI is a lightweight terminal tool for tracking username digital footprints across the internet. Built entirely with Python standard library, it has **zero external dependencies**. Simply provide a username, and it searches across **275+ curated websites** to find associated accounts, automatically assesses information exposure risk, and generates multi-format reports.

### Why TraceHunter-CLI?

| Feature | TraceHunter-CLI | Other Tools |
|---------|----------------|-------------|
| Dependencies | **0** | 30+ |
| Installation | pip / single file | Docker / compile |
| Site Coverage | 275+ curated | 3000+ but bloated |
| Risk Scoring | **Built-in** | None |
| Report Formats | Terminal/JSON/HTML | Many but complex |
| Startup Speed | **Seconds** | Minutes |

## ✨ Core Features

- **Zero Dependencies** - Pure Python 3.8+ standard library, no third-party packages needed
- **275+ Curated Sites** - Covering 9 categories: social, tech, media, gaming, finance, education, forums, shopping, and more
- **Multi-threaded Search** - Configurable concurrency (default 20 threads) for fast scanning
- **Risk Scoring System** - Automatically assesses information exposure risk for each discovered account (0-100 score)
- **Multi-format Reports** - Colored terminal, JSON, and HTML output formats
- **Category Filtering** - Filter target sites by category for precise searching
- **Proxy Support** - HTTP/SOCKS5 proxy support
- **Cross-platform** - Compatible with Windows, Linux, and macOS
- **Chinese Site Support** - Built-in Weibo, Bilibili, Zhihu, Juejin, CSDN, and more

## 🚀 Quick Start

### Installation

```bash
# Install from GitHub
pip install git+https://github.com/gitstq/TraceHunter-CLI.git

# Or clone and install locally
git clone https://github.com/gitstq/TraceHunter-CLI.git
cd TraceHunter-CLI
pip install .
```

### Basic Usage

```bash
# Search for a username
tracehunter -u johndoe

# Search specific categories
tracehunter -u johndoe --categories social,tech

# Export HTML report
tracehunter -u johndoe --output-html report.html

# Export JSON report
tracehunter -u johndoe --output-json result.json

# Use proxy
tracehunter -u johndoe --proxy socks5://127.0.0.1:1080

# List all available sites
tracehunter --list-sites
```

## 📖 Detailed Usage Guide

### CLI Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--username` | `-u` | Target username | Required |
| `--proxy` | `-p` | Proxy URL (http/socks5) | None |
| `--timeout` | `-t` | Request timeout (seconds) | 10 |
| `--workers` | `-w` | Max concurrent threads | 20 |
| `--categories` | `-c` | Site categories to include (comma-separated) | All |
| `--exclude-categories` | `-e` | Site categories to exclude (comma-separated) | None |
| `--output-json` | | Export JSON file path | None |
| `--output-html` | | Export HTML file path | None |
| `--list-sites` | | List all sites and exit | - |
| `--version` | | Show version | - |

### Risk Score Guide

| Score Range | Risk Level | Description |
|-------------|-----------|-------------|
| 80-100 | CRITICAL | Very high risk, extensive sensitive personal information exposed |
| 60-79 | HIGH | High risk, significant information leakage |
| 40-59 | MEDIUM | Moderate risk, some information exposure |
| 20-39 | LOW | Low risk, limited information exposure |
| 0-19 | MINIMAL | Minimal risk, almost no information exposure |

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Minimalism** - Zero dependencies, one pip install to get started
2. **Curated over Quantity** - 275 high-value curated sites over 3000 low-quality signatures
3. **Security Awareness** - Built-in risk scoring to help users understand their digital footprint
4. **Speed First** - Multi-threaded + intelligent scheduling, completes in under 30 seconds

### Roadmap

- [x] v1.0.0 - Core search + risk scoring + multi-format reports
- [ ] v1.1.0 - Recursive search (extract new usernames from discovered accounts)
- [ ] v1.2.0 - Search history comparison (diff analysis across scans)
- [ ] v1.3.0 - Web UI interface
- [ ] v2.0.0 - AI analysis mode (LLM integration for investigation summaries)

## 📦 Packaging & Deployment

### Use as Python Library

```python
from tracehunter_cli.engine import TraceHunter
from tracehunter_cli.risk_scorer import RiskScorer

hunter = TraceHunter(
    username="target_user",
    timeout=10,
    max_workers=20,
    categories=["social", "tech"],
)

results = hunter.search()
scorer = RiskScorer()
scored = scorer.score_all(results)
stats = hunter.get_stats()
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with Python | Zero Dependencies | MIT License
</p>
