# README 索引

> 快速跳转到详细文档

---

## 配置

| 主题 | 文档 |
|------|------|
| 配置格式说明 | [docs/NEW_CONFIG_FORMAT.md](NEW_CONFIG_FORMAT.md) |
| 核心规范 | [docs/CORE_RULES.md](CORE_RULES.md) |
| Windows 安装 | [docs/WINDOWS_INSTALL.md](WINDOWS_INSTALL.md) |

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

在配置文件中添加自己的中转服务：

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

---

## 环境变量

所有服务统一使用以下环境变量：

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_BASE_URL` | API 端点 |
| `ANTHROPIC_AUTH_TOKEN` | API 密钥（唯一认证变量） |
| `ANTHROPIC_MODEL` | 主模型 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 模型 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 模型 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 模型 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 子代理模型 |
| `CLAUDE_CODE_EFFORT_LEVEL` | 努力级别 |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 禁用非必要流量 |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 实验性代理团队 |

> ⚠️ **重要：** 使用 `ANTHROPIC_AUTH_TOKEN`，不要使用 `ANTHROPIC_API_KEY`（已废弃）

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

```
❌ 配置文件不存在: ~/.ccm_services.toml
💡 复制 ccm_services.template 到 ~/.ccm_services.toml 并填写 API Key
```

**解决方法：**
```bash
cp ccm_services.template ~/.ccm_services.toml
ccm config  # 编辑配置
```

### 服务未配置 API Key

```
❌ Service 'kimi' 未配置 api_key
💡 编辑 ~/.ccm_services.toml 并设置 api_key
```

---

## 开发指南

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
