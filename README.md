# Claude Code Multi (ccm)

[English](README.md) | [中文](README_CN.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**统一动态配置系统 - 一个配置文件，管理所有 AI 提供商**

## ⚠️ 重要变更 (v3.0.0)

**新配置系统已启用，不向后兼容旧版本！**

- ✅ 新配置文件：`~/.ccm_services.toml`
- ✅ 统一认证变量：`ANTHROPIC_AUTH_TOKEN`
- ✅ 动态服务命令：`ccm <service-name>`
- ❌ 废弃：`~/.ccm_config`（旧配置文件）
- ❌ 废弃：`ANTHROPIC_API_KEY`（错误的环境变量）
- ❌ 废弃：`ccm kimi china`（旧命令格式）

**迁移指南：**
1. 复制 `ccm_services.template` 到 `~/.ccm_services.toml`
2. 填写你的 API Key
3. 使用新命令：`ccm kimi-cn` 而不是 `ccm kimi china`

---

## Quick Start

```bash
# 1. 安装
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
pip install -e .

# 2. 配置
cp ccm_services.template ~/.ccm_services.toml
# 编辑 ~/.ccm_services.toml 填写 API Key

# 3. 使用
ccm list              # 列出所有服务
ccm kimi-cn           # 切换到 Kimi 中国
ccc ali-qwen-cn       # 切换并启动 Claude Code
```

---

## 安装

### 所有平台（推荐）

```bash
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
pip install -e .
```

### Windows

详见 [Windows 安装指南](docs/WINDOWS_INSTALL.md)

---

## 配置

### 1. 创建配置文件

```bash
cp ccm_services.template ~/.ccm_services.toml
```

### 2. 编辑配置文件

```bash
ccm config  # 自动打开编辑器
```

### 3. 填写 API Key

```toml
[service.kimi-cn]
type = "kimi"
base_url = "https://api.moonshot.cn/anthropic"
api_key = "your-kimi-api-key"  # 填写你的 API Key
model = "kimi-k2.5"
default_sonnet = "kimi-k2.5"
default_opus = "kimi-k2.5"
default_haiku = "kimi-k2.5"
subagent_model = "kimi-k2.5"
```

**所有字段必填，不可省略！**

---

## 基本使用

### 列出所有服务

```bash
ccm list
```

输出示例：
```
┌────────────────┬──────────┬─────────────────────────────┬─────────┐
│ Service        │ Type     │ Base URL                    │ API Key │
├────────────────┼──────────┼─────────────────────────────┼─────────┤
│ kimi-cn        │ kimi     │ api.moonshot.cn/anthropic   │ ✓       │
│ glm-cn         │ glm      │ open.bigmodel.cn/anthropic  │ ✓       │
│ minimax-cn     │ minimax  │ api.minimaxi.com/anthropic  │ ✓       │
└────────────────┴──────────┴─────────────────────────────┴─────────┘
```

### 切换服务

```bash
ccm kimi-cn           # 切换到 Kimi 中国
ccm glm-cn            # 切换到 GLM 中国
ccm ali-qwen-cn       # 切换到阿里云 Qwen 中国
ccm minimax-cn        # 切换到 MiniMax 中国
ccm deepseek          # 切换到 DeepSeek
```

### 切换并启动 Claude Code

```bash
ccc kimi-cn           # 切换到 Kimi 并启动
ccc ali-qwen-cn       # 切换到阿里云 Qwen 并启动
```

### 查看状态

```bash
ccm status            # 查看当前配置
```

---

## 支持的服务

配置文件包含 20 个预定义服务：

| 服务名 | 提供商 | 区域 |
|--------|--------|------|
| `kimi` | Kimi (月之暗面) | Global |
| `kimi-cn` | Kimi (月之暗面) | China |
| `glm` | GLM (智谱) | Global |
| `glm-cn` | GLM (智谱) | China |
| `deepseek` | DeepSeek | - |
| `minimax` | MiniMax | Global |
| `minimax-cn` | MiniMax | China |
| `ali-qwen` | 阿里云 Qwen | Global |
| `ali-qwen-cn` | 阿里云 Qwen | China |
| `ali-kimi` | 阿里云 Kimi | Global |
| `ali-kimi-cn` | 阿里云 Kimi | China |
| `ali-glm` | 阿里云 GLM | Global |
| `ali-glm-cn` | 阿里云 GLM | China |
| `ali-minimax` | 阿里云 MiniMax | Global |
| `ali-minimax-cn` | 阿里云 MiniMax | China |
| `seed` | Seed/Doubao (字节) | - |
| `stepfun` | StepFun (阶跃) | - |
| `claude` | Claude (官方) | - |
| `openrouter` | OpenRouter | - |

### 自定义服务

你可以在配置文件中添加自己的中转服务：

```toml
[service.my-service]
type = "claude"
base_url = "https://your-proxy.com"
api_key = "your-api-key"
model = "claude-sonnet-4-6"
default_sonnet = "claude-sonnet-4-6"
default_opus = "claude-opus-4-6"
default_haiku = "claude-haiku-4-5-20251001"
subagent_model = "claude-sonnet-4-6"
```

然后使用：
```bash
ccm my-service
```

---

## 环境变量

所有服务统一使用以下环境变量：

```bash
ANTHROPIC_BASE_URL                    # API 端点
ANTHROPIC_AUTH_TOKEN                  # API 密钥（唯一认证变量）
ANTHROPIC_MODEL                       # 主模型
ANTHROPIC_DEFAULT_SONNET_MODEL        # Sonnet 模型
ANTHROPIC_DEFAULT_OPUS_MODEL          # Opus 模型
ANTHROPIC_DEFAULT_HAIKU_MODEL         # Haiku 模型
CLAUDE_CODE_SUBAGENT_MODEL            # 子代理模型
CLAUDE_CODE_EFFORT_LEVEL              # 努力级别
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC  # 禁用非必要流量
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS  # 实验性代理团队
```

**⚠️ 重要：**
- ✅ 使用 `ANTHROPIC_AUTH_TOKEN`
- ❌ 不要使用 `ANTHROPIC_API_KEY`（已废弃）

---

## 核心规范

详见 [docs/CORE_RULES.md](docs/CORE_RULES.md)

**最核心约束：永远禁止向后兼容！**

1. ❌ 不保留废弃代码
2. ❌ 不兼容旧配置
3. ❌ 不兼容旧命令
4. ✅ 直接删除旧代码
5. ✅ 明确错误提示
6. ✅ 用户负责更新

---

## 故障排查

### Auth conflict 告警

如果看到以下告警：
```
⚠️ Auth conflict: Both a token (ANTHROPIC_AUTH_TOKEN) and an API key (ANTHROPIC_API_KEY) are set.
```

**解决方法：**
```bash
# PowerShell
$env:ANTHROPIC_API_KEY = $null

# Bash/Zsh
unset ANTHROPIC_API_KEY
```

### 配置文件不存在

```bash
❌ 配置文件不存在: ~/.ccm_services.toml
💡 复制 ccm_services.template 到 ~/.ccm_services.toml 并填写 API Key
```

**解决方法：**
```bash
cp ccm_services.template ~/.ccm_services.toml
ccm config  # 编辑配置
```

### 服务未配置 API Key

```bash
❌ Service 'kimi' 未配置 api_key
💡 编辑 ~/.ccm_services.toml 并设置 api_key
```

**解决方法：**
打开 `~/.ccm_services.toml`，找到对应服务，填写 `api_key` 字段。

---

## 开发

### 项目结构

```
claude-code-multi/
├── src/ccm/
│   ├── cli.py              # CLI 入口（动态命令注册）
│   ├── launcher.py         # ccc 启动器
│   ├── config/
│   │   ├── services.py     # 服务配置管理
│   │   └── __init__.py
│   └── providers/          # Provider 实现（已废弃，仅保留 base.py）
├── ccm_services.template   # 配置模板
├── docs/
│   ├── CORE_RULES.md       # 核心规范
│   └── WINDOWS_INSTALL.md  # Windows 安装指南
└── README.md
```

### 运行测试

```bash
pip install -e .
ccm list
ccm status
```

---

## 版本历史

### v3.0.0 (2025-03)
- ✅ **统一动态配置系统** - 一个 TOML 文件管理所有服务
- ✅ **动态命令注册** - 自动为每个服务创建命令
- ✅ **统一认证变量** - 所有服务使用 `ANTHROPIC_AUTH_TOKEN`
- ❌ **移除向后兼容** - 不支持旧配置文件和旧命令
- 📝 **核心规范文档** - `docs/CORE_RULES.md`

### v2.4.0 (2025-02)
- User-level settings
- Config file auto-reload
- Model updates

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Contributing

欢迎贡献！请遵循以下规范：

1. **禁止向后兼容** - 不保留废弃代码
2. **明确错误提示** - 告诉用户如何更新
3. **简洁代码** - 不添加不必要的抽象

详见 [docs/CORE_RULES.md](docs/CORE_RULES.md)
