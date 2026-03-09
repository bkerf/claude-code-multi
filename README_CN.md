# Claude Code Multi (ccm)

[English](README.md) | [中文](README_CN.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/bkerf/claude-code-multi.svg)](https://github.com/bkerf/claude-code-multi/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/bkerf/claude-code-multi.svg)](https://github.com/bkerf/claude-code-multi/issues)

在多个终端会话中并行运行不同的 AI 模型，实现多模型协同工作。


## 快速开始

```bash
# 1. 安装
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
./install.sh

# 2. 重载 shell
source ~/.zshrc  # 或 ~/.bashrc

# 3. 配置 API Key
ccm config

# 4. 切换并使用
ccm glm              # 切换到 GLM
ccc glm global       # 切换 + 启动 Claude Code

# 高级：用户级设置（最高优先级，覆盖所有其他配置）
ccm user glm global      # 设置 GLM 为所有项目的默认
ccm user reset           # 恢复环境变量控制

# 高级：项目级覆盖
ccm project glm china    # 仅当前项目使用 GLM

# 高级：多个 Claude Pro 账号
ccm account save work    # 保存当前账号
ccm account switch work  # 切换到已保存账号
```

---

## 安装

### Mac & Linux

```bash
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
./install.sh
source ~/.zshrc  # 或 ~/.bashrc
```

### Windows

详见 [Windows 安装指南](docs/WINDOWS_INSTALL.md)

快速开始：
```powershell
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
pip install -e .
```

### 安装模式

| 模式 | 命令 | 使用场景 |
|------|------|----------|
| **用户**（默认） | `./install.sh` | 个人使用，全局可用 |
| **系统** | `./install.sh --system` | 共享机器，所有用户 |
| **项目** | `./install.sh --project` | 项目专用，隔离环境 |

### 安装选项
```bash
./install.sh --no-rc           # 跳过 shell rc 注入
./install.sh --cleanup-legacy  # 清理旧版本
./install.sh --help            # 显示所有选项
```

### 卸载
```bash
./uninstall.sh
```

---

## 首次配置

> ⚠️ **重要：删除 settings.json 中的 env 字段**
>
> 如果你的 `~/.claude/settings.json` 文件中存在 `env` 字段，**必须删除它**，否则 ccm 设置的环境变量不会生效。
>
> **检查方法：**
> ```bash
> cat ~/.claude/settings.json
> ```
>
> 如果输出包含 `"env": {...}` 部分，需要手动删除或运行：
> ```bash
> ccm user reset
> ```

### 1. 配置 API Key
```bash
ccm config
```

这会在编辑器中打开 `~/.ccm_config`。添加你的 API Key：

```bash
# 每个需要使用的 provider 都需要配置
DEEPSEEK_API_KEY=sk-...
KIMI_API_KEY=...
GLM_API_KEY=...
QWEN_API_KEY=...
MINIMAX_API_KEY=...
ARK_API_KEY=...           # 豆包/Seed
OPENROUTER_API_KEY=...    # OpenRouter
CLAUDE_API_KEY=...        # 可选，Claude API（非订阅用户）
```

### 2. 验证配置
```bash
ccm status    # 查看当前配置
```

---

## 基本用法

### 切换 Provider（当前 shell）
```bash
ccm glm global        # GLM 全球（默认）
ccm glm china         # GLM 国内
ccm deepseek          # DeepSeek
ccm kimi global       # Kimi 全球
ccm kimi china        # Kimi 国内
ccm ali china         # 阿里云 Coding Plan
ccm minimax           # MiniMax
ccm seed              # 豆包/Seed
ccm claude            # Claude 官方
```

### 阿里云 Coding Plan (2.4.0)
阿里云 Coding Plan 提供 4 种模型：
```bash
# 语法：ccm ali <变体> [区域]
ccm ali qwen china        # qwen3.5-plus（多模态）
ccm ali kimi global       # kimi-k2.5（多模态）
ccm ali glm china         # glm-5
ccm ali minimax china     # MiniMax-M2.5

# 冒号语法简写
ccm ali:qwen              # qwen3.5-plus，国内
ccm ali:kimi:global       # kimi-k2.5，全球
```

### 切换 + 启动 Claude Code
```bash
ccc glm global        # 切换到 GLM 全球，然后启动
ccc glm china         # 切换到 GLM 国内，然后启动
ccc open glm          # 通过 OpenRouter

# 阿里云 Coding Plan
ccc ali               # 默认：qwen3.5-plus，国内
ccc ali:qwen:global   # qwen3.5-plus，全球
ccc ali:kimi          # kimi-k2.5，国内
```

### 查看状态
```bash
ccm status             # 显示当前模型和 API Key 状态
ccm account current    # 显示当前 Claude Pro 账号
```

### 获取帮助
```bash
ccm help               # 显示所有命令
ccc                    # 显示 ccc 用法（无参数）
```

---

## 多模型协同

ccm 的核心目的是让**不同终端使用不同模型**，让专业模型协同工作：

```bash
# 终端 1: DeepSeek 负责编码
ccm deepseek
claude

# 终端 2: GLM 负责文档
ccm glm china
claude

# 终端 3: MiniMax 负责分析
ccm minimax
claude
```

每个终端会话保持独立的模型选择。这可以实现：
- **并行工作流**：专业模型各司其职
- **模型对比**：同一任务对比不同模型
- **任务委派**：分配给最合适的模型

---

## Provider 参考

### 直连 Provider（需要 API Key）

| Provider | 命令 | 区域 | Base URL |
|----------|------|------|----------|
| 阿里云 | `ccm ali [变体] [global\|china]` | global | `coding-intl.dashscope.aliyuncs.com/apps/anthropic` |
| | | china（默认） | `coding.dashscope.aliyuncs.com/apps/anthropic` |
| GLM | `ccm glm [global\|china]` | global（默认） | `api.z.ai/api/anthropic` |
| | | china | `open.bigmodel.cn/api/anthropic` |
| DeepSeek | `ccm deepseek` | - | `api.deepseek.com/anthropic` |
| Kimi | `ccm kimi [global\|china]` | global（默认） | `api.moonshot.ai/anthropic` |
| | | china | `api.moonshot.cn/anthropic` |
| MiniMax | `ccm minimax [global\|china]` | global（默认） | `api.minimax.io/anthropic` |
| | | china | `api.minimaxi.com/anthropic` |
| 豆包/Seed | `ccm seed [变体]` | - | `ark.cn-beijing.volces.com/api/coding` |
| Claude | `ccm claude` | - | `api.anthropic.com` |

> **阿里云 Coding Plan**: [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com/)
>
> **GLM Coding Plan**: [bigmodel.cn/glm-coding](https://www.bigmodel.cn/glm-coding?ic=5XMIOZPPXB)
>
> **豆包 Coding Plan**: [volcengine.com](https://volcengine.com/L/rLv5d5OWXgg/)（邀请码：`ZP5PZMEY`）

### Seed 变体
```bash
ccm seed              # ark-code-latest（默认）
ccm seed doubao       # doubao-seed-code
ccm seed glm          # glm-5
ccm seed deepseek     # deepseek-v3.2
ccm seed kimi         # kimi-k2.5
```

### 阿里云 Coding Plan 模型

| 变体 | 模型 ID | 描述 |
|------|---------|------|
| `qwen` | qwen3.5-plus | 多模态（图像理解） |
| `kimi` | kimi-k2.5 | 多模态（图像理解） |
| `glm` | glm-5 | 通用 |
| `minimax` | MiniMax-M2.5 | 通用 |

### OpenRouter
```bash
ccm open              # 显示帮助
ccm open claude       # Claude via OpenRouter
ccm open glm          # GLM via OpenRouter
ccm open kimi         # Kimi via OpenRouter
ccm open deepseek     # DeepSeek via OpenRouter
ccm open qwen         # Qwen via OpenRouter
ccm open minimax      # MiniMax via OpenRouter
ccm open stepfun      # StepFun via OpenRouter
ccm open sf-free      # StepFun 免费版
```

**可用 provider：**`claude`、`glm`、`kimi`、`deepseek`、`qwen`、`minimax`、`stepfun`

**免费版：**`stepfun-free` 或 `sf-free` 使用 StepFun 免费模型

---

## 高级功能

### Claude Pro 账号管理
在多个 Claude Pro 订阅之间切换：

```bash
# 保存当前登录账号
ccm account save work

# 切换到已保存账号
ccm account switch work

# 列出所有已保存账号
ccm account list

# 显示当前账号
ccm account current

# 删除已保存账号
ccm account delete work
```

### 用户级设置（最高优先级）
直接写入 `~/.claude/settings.json`。这会覆盖包括环境变量在内的所有配置，适用于有其他工具（如 Quotio）也修改此文件的场景。

```bash
# 设置用户级 provider
ccm user glm global      # 所有项目使用 GLM 全球
ccm user glm china       # 所有项目使用 GLM 国内
ccm user deepseek        # 所有项目使用 DeepSeek
ccm user claude          # 所有项目使用 Claude 官方

# 重置为环境变量控制
ccm user reset           # 移除 ccm 设置，使用环境变量
```

**使用场景：**
- 有 Quotio 或其他代理修改 `~/.claude/settings.json`
- 需要持久化默认设置，不受 shell 重启影响
- 环境变量被其他程序覆盖

### 项目级覆盖
为特定项目覆盖设置（保持全局设置不变）：

```bash
# 在项目目录中
ccm project glm global    # 仅此项目使用 GLM
ccm project glm china     # 仅此项目使用 GLM 国内
ccm project reset         # 移除项目覆盖
```

这会在当前项目创建/删除 `.claude/settings.local.json`。

### 带账号启动
```bash
ccc work                  # 切换到 'work' 账号，然后启动
ccc claude:personal       # 切换到 'personal' 账号 + 使用 Claude
```

---

## 配置

### 优先级（从高到低）
1. `~/.claude/settings.json`（env 部分）- 用户级设置
2. `.claude/settings.local.json` - 项目级设置
3. `~/.ccm_config` 文件 - **每次 ccm 命令都会重新加载**
4. 环境变量（仅当配置值为占位符时使用）

### 配置文件位置
```
~/.ccm_config
```

### 快速设置
```bash
# 复制示例配置并编辑
cp ccm_config.example ~/.ccm_config
ccm config  # 在编辑器中打开
```

### 多变体 Provider

部分 provider 支持**统一 API Key**访问多种模型：

| Provider | API Key | 变体（CLI） | 示例 |
|----------|---------|-------------|------|
| **阿里云** | `QWEN_API_KEY` | `qwen`、`kimi`、`glm`、`minimax` | `ccm ali kimi china` |
| **豆包/Seed** | `ARK_API_KEY` | `doubao`、`glm`、`deepseek`、`kimi` | `ccm seed glm` |
| **OpenRouter** | `OPENROUTER_API_KEY` | `claude`、`kimi`、`glm`、`deepseek`... | `ccm open claude` |

**关键点：**变体通过 CLI 指定，不在配置文件中。一个 API Key 覆盖所有变体。

```bash
# 阿里云：一个 Key，4 种模型
QWEN_API_KEY=sk-xxx     # 适用于 qwen、kimi、glm、minimax

# 通过 CLI 切换模型：
ccm ali qwen            # → qwen3.5-plus
ccm ali kimi global     # → kimi-k2.5（全球区域）
ccm ali glm china       # → glm-5（国内区域）
```

### 完整配置示例

详见 [ccm_config.example](ccm_config.example)。

```bash
# ~/.ccm_config - API Keys
DEEPSEEK_API_KEY=sk-xxx
KIMI_API_KEY=sk-xxx
GLM_API_KEY=sk-xxx
QWEN_API_KEY=sk-xxx     # ali 变体统一 key
MINIMAX_API_KEY=sk-xxx
ARK_API_KEY=sk-xxx      # seed 变体统一 key
OPENROUTER_API_KEY=sk-or-xxx

# 模型 ID 覆盖（可选）
DEEPSEEK_MODEL=deepseek-chat
KIMI_MODEL=kimi-k2.5
KIMI_CN_MODEL=kimi-k2.5
QWEN_MODEL=qwen3-max-2026-01-23
GLM_MODEL=glm-5
MINIMAX_MODEL=MiniMax-M2.5
SEED_MODEL=ark-code-latest
CLAUDE_MODEL=claude-sonnet-4-5-20250929
OPUS_MODEL=claude-opus-4-6
HAIKU_MODEL=claude-haiku-4-5-20251001
```

---

## 无 RC 注入模式

如果你使用 `--no-rc` 安装或想从克隆的仓库使用：

```bash
# 切换模型（将环境变量应用到当前 shell）
eval "$(ccm glm global)"
eval "$(./ccm.sh glm china)"

# 或直接使用包装脚本
./ccm glm global         # 只打印 export 语句
./ccc glm china          # 切换 + 启动
```

---

## 注意事项

- **每个 provider 导出 7 个环境变量**：`ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_MODEL`、`ANTHROPIC_DEFAULT_OPUS_MODEL`、`ANTHROPIC_DEFAULT_SONNET_MODEL`、`ANTHROPIC_DEFAULT_HAIKU_MODEL`、`CLAUDE_CODE_SUBAGENT_MODEL`
- **Claude 官方**：默认使用 Claude Code 订阅，或使用 `CLAUDE_API_KEY`（如果设置）
- **OpenRouter**：需要显式 `ccm open <provider>` 命令
- **项目覆盖**：仅通过 `.claude/settings.local.json` 影响当前项目

---

## 贡献

欢迎贡献！以下是参与方式：

### 报告问题
发现 Bug 或有功能建议？[提交 Issue](https://github.com/bkerf/claude-code-multi/issues)。

### 提交代码
1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/your-feature`）
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

### 开发
```bash
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
./ccm.sh help    # 本地测试（无需安装）
```

---

## 更新日志

### v2.4.0 (2025-02)
- **`ccm user` 命令** - 直接写入 `~/.claude/settings.json`（最高优先级）
- **配置文件实时重载** - 编辑 `~/.ccm_config` 后立即生效
- **增强 `ccm status`** - 检测并警告用户级设置覆盖
- 模型更新：Kimi → `kimi-k2.5`、MiniMax → `MiniMax-M2.5`、GLM → `glm-5`
- 新增 Coding Plan 链接：GLM、豆包

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)。

---

## 致谢

本工具源于在使用 Claude Code 时便捷切换 AI Provider 的需求。感谢所有贡献者和开源社区。