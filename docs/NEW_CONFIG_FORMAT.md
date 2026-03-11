# 新配置格式设计文档

## 配置文件路径

```
~/.ccm_services.toml
```

## 设计原则

1. **所有参数必填** - 不省略任何字段，避免混乱
2. **统一变量名** - 所有服务使用相同的字段名
3. **完整端点信息** - 每个服务必须明确指定 base_url
4. **敏感信息不入库** - api_key 仅存在于用户配置文件，不提交到代码仓库

## 配置格式

```toml
# CCM Services Configuration
# 所有字段均为必填，不可省略

language = "zh"

# ============================================================================
# Kimi (月之暗面) - 直连
# ============================================================================

[service.kimi]
type = "kimi"
base_url = "https://api.moonshot.ai/anthropic"
api_key = ""
model = "kimi-k2.5"
default_sonnet = "kimi-k2.5"
default_opus = "kimi-k2.5"
default_haiku = "kimi-k2.5"
subagent_model = "kimi-k2.5"

[service.kimi-cn]
type = "kimi"
base_url = "https://api.moonshot.cn/anthropic"
api_key = ""
model = "kimi-k2.5"
default_sonnet = "kimi-k2.5"
default_opus = "kimi-k2.5"
default_haiku = "kimi-k2.5"
subagent_model = "kimi-k2.5"

# ============================================================================
# GLM (智谱) - 直连
# ============================================================================

[service.glm]
type = "glm"
base_url = "https://api.z.ai/api/anthropic"
api_key = ""
model = "glm-5"
default_sonnet = "glm-5"
default_opus = "glm-5"
default_haiku = "glm-5"
subagent_model = "glm-5"

[service.glm-cn]
type = "glm"
base_url = "https://open.bigmodel.cn/api/anthropic"
api_key = ""
model = "glm-5"
default_sonnet = "glm-5"
default_opus = "glm-5"
default_haiku = "glm-5"
subagent_model = "glm-5"

# ============================================================================
# DeepSeek - 直连
# ============================================================================

[service.deepseek]
type = "deepseek"
base_url = "https://api.deepseek.com/anthropic"
api_key = ""
model = "deepseek-chat"
default_sonnet = "deepseek/deepseek-v3.2"
default_opus = "deepseek/deepseek-v3.2"
default_haiku = "deepseek/deepseek-v3.2"
subagent_model = "deepseek-chat"

# ============================================================================
# MiniMax - 直连
# ============================================================================

[service.minimax]
type = "minimax"
base_url = "https://api.minimax.io/anthropic"
api_key = ""
model = "MiniMax-M2.5"
default_sonnet = "MiniMax-M2.5"
default_opus = "MiniMax-M2.5"
default_haiku = "MiniMax-M2.5"
subagent_model = "MiniMax-M2.5"

[service.minimax-cn]
type = "minimax"
base_url = "https://api.minimaxi.com/anthropic"
api_key = ""
model = "MiniMax-M2.5"
default_sonnet = "MiniMax-M2.5"
default_opus = "MiniMax-M2.5"
default_haiku = "MiniMax-M2.5"
subagent_model = "MiniMax-M2.5"

# ============================================================================
# Alibaba Cloud Coding Plan (阿里云)
# ============================================================================

[service.ali-qwen]
type = "ali"
base_url = "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "qwen3.5-plus"
default_sonnet = "qwen3.5-plus"
default_opus = "qwen3.5-plus"
default_haiku = "qwen3.5-plus"
subagent_model = "qwen3.5-plus"

[service.ali-qwen-cn]
type = "ali"
base_url = "https://coding.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "qwen3.5-plus"
default_sonnet = "qwen3.5-plus"
default_opus = "qwen3.5-plus"
default_haiku = "qwen3.5-plus"
subagent_model = "qwen3.5-plus"

[service.ali-kimi]
type = "ali"
base_url = "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "kimi-k2.5"
default_sonnet = "kimi-k2.5"
default_opus = "kimi-k2.5"
default_haiku = "kimi-k2.5"
subagent_model = "kimi-k2.5"

[service.ali-kimi-cn]
type = "ali"
base_url = "https://coding.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "kimi-k2.5"
default_sonnet = "kimi-k2.5"
default_opus = "kimi-k2.5"
default_haiku = "kimi-k2.5"
subagent_model = "kimi-k2.5"

[service.ali-glm]
type = "ali"
base_url = "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "glm-5"
default_sonnet = "glm-5"
default_opus = "glm-5"
default_haiku = "glm-5"
subagent_model = "glm-5"

[service.ali-glm-cn]
type = "ali"
base_url = "https://coding.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "glm-5"
default_sonnet = "glm-5"
default_opus = "glm-5"
default_haiku = "glm-5"
subagent_model = "glm-5"

[service.ali-minimax]
type = "ali"
base_url = "https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "MiniMax-M2.5"
default_sonnet = "MiniMax-M2.5"
default_opus = "MiniMax-M2.5"
default_haiku = "MiniMax-M2.5"
subagent_model = "MiniMax-M2.5"

[service.ali-minimax-cn]
type = "ali"
base_url = "https://coding.dashscope.aliyuncs.com/apps/anthropic"
api_key = ""
model = "MiniMax-M2.5"
default_sonnet = "MiniMax-M2.5"
default_opus = "MiniMax-M2.5"
default_haiku = "MiniMax-M2.5"
subagent_model = "MiniMax-M2.5"

# ============================================================================
# Seed/Doubao (字节跳动)
# ============================================================================

[service.seed]
type = "seed"
base_url = "https://ark.cn-beijing.volces.com/api/coding"
api_key = ""
model = "ark-code-latest"
default_sonnet = "ark-code-latest"
default_opus = "ark-code-latest"
default_haiku = "ark-code-latest"
subagent_model = "ark-code-latest"

# ============================================================================
# StepFun (阶跃)
# ============================================================================

[service.stepfun]
type = "stepfun"
base_url = "https://api.stepfun.ai/v1/anthropic"
api_key = ""
model = "step-3.5-flash"
default_sonnet = "step-3.5-flash"
default_opus = "step-3.5-flash"
default_haiku = "step-3.5-flash"
subagent_model = "step-3.5-flash"

# ============================================================================
# Claude (官方)
# ============================================================================

[service.claude]
type = "claude"
base_url = "https://api.anthropic.com/"
api_key = ""
model = "claude-sonnet-4-5-20250929"
default_sonnet = "claude-sonnet-4-5-20250929"
default_opus = "claude-opus-4-6"
default_haiku = "claude-haiku-4-5-20251001"
subagent_model = "claude-sonnet-4-5-20250929"

# ============================================================================
# OpenRouter (多提供商网关)
# ============================================================================

[service.openrouter]
type = "openrouter"
base_url = "https://openrouter.ai/api"
api_key = ""
model = "anthropic/claude-sonnet-4.5"
default_sonnet = "anthropic/claude-sonnet-4.5"
default_opus = "anthropic/claude-opus-4.6"
default_haiku = "anthropic/claude-haiku-4-5"
subagent_model = "anthropic/claude-sonnet-4.5"

# ============================================================================
# 自定义中转服务示例
# ============================================================================

[service.my-proxy]
type = "claude"
base_url = "https://your-proxy.example.com"
api_key = ""
model = "claude-sonnet-4-5-20250929"
default_sonnet = "claude-sonnet-4-5-20250929"
default_opus = "claude-opus-4-6"
default_haiku = "claude-haiku-4-5-20251001"
subagent_model = "claude-sonnet-4-5-20250929"
```

## 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `type` | ✅ | 服务类型 |
| `base_url` | ✅ | API 端点 URL |
| `api_key` | ✅ | API 密钥（Claude Pro 可留空） |
| `model` | ✅ | 主模型 ID |
| `default_sonnet` | ✅ | Sonnet 模型 ID |
| `default_opus` | ✅ | Opus 模型 ID |
| `default_haiku` | ✅ | Haiku 模型 ID |
| `subagent_model` | ✅ | 子代理模型 ID |

## 服务列表 (20个)

| 服务名 | 类型 | 说明 | base_url |
|--------|------|------|----------|
| `kimi` | kimi | Kimi 国际 | api.moonshot.ai |
| `kimi-cn` | kimi | Kimi 中国 | api.moonshot.cn |
| `glm` | glm | GLM 国际 | api.z.ai |
| `glm-cn` | glm | GLM 中国 | open.bigmodel.cn |
| `deepseek` | deepseek | DeepSeek | api.deepseek.com |
| `minimax` | minimax | MiniMax 国际 | api.minimax.io |
| `minimax-cn` | minimax | MiniMax 中国 | api.minimaxi.com |
| `ali-qwen` | ali | 阿里云 Qwen | coding-intl.dashscope |
| `ali-qwen-cn` | ali | 阿里云 Qwen 中国 | coding.dashscope |
| `ali-kimi` | ali | 阿里云 Kimi | coding-intl.dashscope |
| `ali-kimi-cn` | ali | 阿里云 Kimi 中国 | coding.dashscope |
| `ali-glm` | ali | 阿里云 GLM | coding-intl.dashscope |
| `ali-glm-cn` | ali | 阿里云 GLM 中国 | coding.dashscope |
| `ali-minimax` | ali | 阿里云 MiniMax | coding-intl.dashscope |
| `ali-minimax-cn` | ali | 阿里云 MiniMax 中国 | coding.dashscope |
| `seed` | seed | 字节豆包 | ark.cn-beijing.volces.com |
| `stepfun` | stepfun | 阶跃 | api.stepfun.ai |
| `claude` | claude | Claude 官方 | api.anthropic.com |
| `openrouter` | openrouter | OpenRouter | openrouter.ai |

## 命令映射 (旧 → 新)

| 旧命令 | 新命令 | 说明 |
|--------|--------|------|
| `ccc kimi` | `ccc kimi` | 不变 |
| `ccc kimi china` | `ccc kimi-cn` | 合并为一个命令 |
| `ccc glm china` | `ccc glm-cn` | 合并为一个命令 |
| `ccc ali qwen` | `ccc ali-qwen` | 连字符连接 |
| `ccc ali qwen china` | `ccc ali-qwen-cn` | 连字符连接 |
| `ccc ali kimi` | `ccc ali-kimi` | 连字符连接 |
| `ccc seed doubao` | `ccc seed` | 移除 variant |

## 使用方式

```bash
# 切换服务（输出环境变量）
ccm kimi
ccm ali-qwen
ccm 2233

# 列出所有服务
ccm list

# 启动 Claude Code
ccc kimi
ccc ali-qwen-cn
ccc 2233
```

## 与旧配置的区别

| 项目 | 旧配置 (`~/.ccm_config`) | 新配置 (`~/.ccm_services.toml`) |
|------|--------------------------|----------------------------|
| 格式 | KEY=VALUE (bash 风格) | TOML |
| 服务定义 | 硬编码在代码中 | 完全动态配置 |
| URL | 硬编码在 provider 类中 | 每个服务独立配置 |
| Model | 可选覆盖 | 必填，完整配置 |
| 自定义服务 | 不支持 | 完全支持 |
| 迁移 | - | 测试通过后删除旧配置 |

## 迁移计划

1. **阶段 1**: 实现新配置读取（不影响旧配置）
2. **阶段 2**: 新增 `ccm init` 生成示例配置
3. **阶段 3**: 测试所有内置服务
4. **阶段 4**: 测试自定义服务
5. **阶段 5**: 文档更新
6. **阶段 6**: 删除旧配置支持

## 规则

- **api_key 不入库**: 配置模板中 `api_key = ""` 保持为空，实际密钥仅存在于用户本地 `~/.ccm_services.toml`
