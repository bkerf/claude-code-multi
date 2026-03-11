# Claude Code Multi (ccm)

[English](README.md) | [中文](README_CN.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**在多个终端窗口中同时运行不同的 AI 模型，让专业模型协同工作**

---

## 为什么需要 CCM？

Claude Code 很强大，但只能在一个窗口中使用一个模型。CCM 让你：

- 🚀 **并行工作流** - 在不同窗口使用不同模型，同时处理多个任务
- 🎯 **专业分工** - 让擅长编码的模型写代码，擅长文档的模型写文档
- 💰 **成本优化** - 简单任务用便宜的模型，复杂任务用强大的模型
- 🔄 **快速切换** - 一条命令切换 AI 提供商，无需重启

### 典型场景

```bash
# 窗口 1: DeepSeek 写代码（便宜且强大）
ccc deepseek

# 窗口 2: GLM 写文档（中文友好）
ccc glm-cn

# 窗口 3: Kimi 做分析（长上下文）
ccc kimi-cn

# 窗口 4: MiniMax 做测试（快速响应）
ccc minimax-cn
```

**每个窗口独立运行，互不干扰，专业模型协同工作！**

---

## 快速开始

```bash
# 1. 安装
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
pip install -e .

# 2. 配置
cp ccm_services.template ~/.ccm_services.toml
ccm config  # 填写 API Key

# 3. 启动多个窗口
ccc deepseek      # 窗口 1: DeepSeek 编码
ccc glm-cn        # 窗口 2: GLM 文档
ccc kimi-cn       # 窗口 3: Kimi 分析
```

---

## 核心功能

### 1. 多窗口并行

每个终端窗口可以使用不同的 AI 模型：

```bash
# 终端 1
ccc deepseek
> 用 DeepSeek 写核心算法

# 终端 2
ccc glm-cn
> 用 GLM 写中文文档

# 终端 3
ccc kimi-cn
> 用 Kimi 分析长文本
```

### 2. 一键切换

无需重启，一条命令切换模型：

```bash
ccm list          # 查看所有可用模型
ccm deepseek      # 切换到 DeepSeek
ccm glm-cn        # 切换到 GLM
```

### 3. 统一配置

一个配置文件管理所有 AI 提供商：

```toml
[service.deepseek]
api_key = "your-key"
model = "deepseek-chat"

[service.glm-cn]
api_key = "your-key"
model = "glm-5"
```

### 4. 支持 20+ 服务

- **国内**: Kimi、GLM、MiniMax、DeepSeek、阿里云、Seed、StepFun
- **国际**: Claude、OpenRouter
- **自定义**: 支持任何兼容 Anthropic API 的中转服务

---

## 安装

### 所有平台

```bash
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
pip install -e .
```

### Windows

详见 [docs/WINDOWS_INSTALL.md](docs/WINDOWS_INSTALL.md)

---

## 配置

```bash
# 1. 创建配置文件
cp ccm_services.template ~/.ccm_services.toml

# 2. 编辑配置
ccm config

# 3. 填写 API Key
# 在打开的编辑器中填写你要使用的服务的 api_key
```

---

## 使用

### 基本命令

```bash
ccm list          # 列出所有服务
ccm status        # 查看当前配置
ccm <service>     # 切换服务（当前 shell）
ccc <service>     # 切换服务并启动 Claude Code
```

### 多窗口工作流

**场景 1: 全栈开发**
```bash
# 窗口 1: 后端开发
ccc deepseek      # DeepSeek 写 Python/Go

# 窗口 2: 前端开发
ccc glm-cn        # GLM 写 Vue/React

# 窗口 3: 文档编写
ccc kimi-cn       # Kimi 写文档
```

**场景 2: 代码审查**
```bash
# 窗口 1: 写代码
ccc deepseek

# 窗口 2: 审查代码
ccc glm-cn        # 用不同模型审查，发现更多问题
```

**场景 3: 成本优化**
```bash
# 窗口 1: 简单任务
ccc minimax-cn    # 便宜的模型处理简单任务

# 窗口 2: 复杂任务
ccc deepseek      # 强大的模型处理复杂任务
```

---

## 支持的服务

| 服务 | 提供商 | 特点 | 推荐场景 |
|------|--------|------|----------|
| `deepseek` | DeepSeek | 便宜强大 | 编码、算法 |
| `glm-cn` | GLM (智谱) | 中文友好 | 文档、注释 |
| `kimi-cn` | Kimi (月之暗面) | 长上下文 | 分析、总结 |
| `minimax-cn` | MiniMax | 快速响应 | 测试、调试 |
| `ali-qwen-cn` | 阿里云 Qwen | 多模态 | 图片理解 |
| `ali-kimi-cn` | 阿里云 Kimi | 长上下文 | 代码审查 |
| `seed` | Seed/Doubao | 字节出品 | 通用任务 |
| `claude` | Claude 官方 | 最强大 | 复杂任务 |

完整列表（20+ 服务）见 [docs/README_INDEX.md](docs/README_INDEX.md)

---

## 自定义服务

支持任何兼容 Anthropic API 的中转服务：

```toml
[service.my-proxy]
type = "claude"
base_url = "https://your-proxy.com"
api_key = "your-api-key"
model = "claude-sonnet-4-6"
default_sonnet = "claude-sonnet-4-6"
default_opus = "claude-opus-4-6"
default_haiku = "claude-haiku-4-5-20251001"
subagent_model = "claude-sonnet-4-6"
```

---

## 贡献

欢迎贡献！我们需要：

- 🌍 **新的 AI 提供商支持** - 添加更多服务
- 📝 **文档改进** - 使用案例、最佳实践
- 🐛 **Bug 修复** - 发现问题请提 Issue
- ✨ **功能建议** - 告诉我们你的需求

### 开发规范

详见 [docs/CORE_RULES.md](docs/CORE_RULES.md)

**核心原则：永远禁止向后兼容！**

---

## 常见问题

### Q: 为什么需要多窗口？

A: 不同 AI 模型有不同优势：
- DeepSeek 编码强但中文弱
- GLM 中文强但编码弱
- Kimi 长上下文但速度慢
- MiniMax 速度快但能力弱

多窗口让你同时使用它们的优势！

### Q: 会不会很贵？

A: 反而更省钱！
- 简单任务用便宜模型（MiniMax、GLM）
- 复杂任务用强大模型（DeepSeek、Claude）
- 比全程用 Claude 便宜 10 倍以上

### Q: 如何选择模型？

A: 推荐组合：
- **编码**: DeepSeek（便宜强大）
- **文档**: GLM（中文友好）
- **分析**: Kimi（长上下文）
- **测试**: MiniMax（快速响应）

---

## 致谢

感谢所有贡献者和 AI 提供商！

特别感谢：
- [Claude Code](https://claude.ai/code) - 强大的 AI 编程工具
- [DeepSeek](https://www.deepseek.com/) - 便宜强大的编码模型
- [GLM](https://www.bigmodel.cn/) - 中文友好的通用模型
- [Kimi](https://www.moonshot.cn/) - 长上下文专家

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Star History

如果这个项目对你有帮助，请给个 ⭐️！

让更多人知道多窗口协同工作的强大！
