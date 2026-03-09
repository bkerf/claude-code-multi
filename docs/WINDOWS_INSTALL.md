# Windows 安装与运行指南

## 环境要求

- Python 3.10+
- Node.js 18+ (用于 Claude Code)
- Windows 10/11

## 安装步骤

### 1. 克隆项目

```powershell
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
```

### 2. 安装 Python 包

```powershell
pip install claude-code-multi
```

这会创建全局命令 `ccm` 和 `ccc`。

### 3. 配置 PowerShell 函数

```powershell
# 在 PowerShell 中运行安装脚本
.\install-ps.ps1
```

这会将 `ccm` 和 `ccc` 函数添加到 PowerShell 配置文件中。

### 4. 配置 API Key

编辑 `~/.ccm_config` 文件，添加你的 API Key：

```ini
# API Keys
GLM_API_KEY=your-glm-api-key
KIMI_API_KEY=your-kimi-api-key
MINIMAX_API_KEY=your-minimax-api-key
QWEN_API_KEY=your-qwen-api-key

# 可选：设置默认模型
MINIMAX_MODEL=MiniMax-M2.5-highspeed
GLM_MODEL=glm-5
```

## 使用方法

### ccm 命令（仅切换环境变量）

```powershell
# 切换到指定 provider
ccm minimax           # MiniMax (默认 china)
ccm minimax global    # MiniMax (global)
ccm glm              # GLM (默认 china)
ccm glm china        # GLM (china)
ccm kimi             # Kimi (默认 china)
ccm deepseek         # DeepSeek (默认 global)
ccm ali              # 阿里云 (默认 qwen)
ccm ali glm          # 阿里云 GLM 模型
ccm ali minimax       # 阿里云 MiniMax 模型
ccm ali kimi         # 阿里云 Kimi 模型
ccm ali qwen         # 阿里云 Qwen 模型

# 查看状态
ccm status
ccm list
```

执行后会输出环境变量设置命令，复制到当前终端执行：

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.minimaxi.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = "your-key"
# ...
```

### ccc 命令（切换 + 启动 Claude Code）

```powershell
# 切换并启动
ccc minimax           # MiniMax (默认 china)
ccc glm              # GLM (默认 china)
ccc ali glm          # 阿里云 GLM 模型
ccc ali minimax      # 阿里云 MiniMax 模型
ccc ali kimi         # 阿里云 Kimi 模型
```

ccc 会自动在新窗口启动 Claude Code。

## Provider 列表

| 命令 | 提供商 | 默认 Region | 支持变体 |
|------|--------|-------------|----------|
| `minimax` | MiniMax | china | - |
| `glm` | 智谱 GLM | china | - |
| `kimi` | 月之暗面 | china | - |
| `deepseek` | DeepSeek | global | - |
| `ali` | 阿里云 Coding Plan | china | qwen/glm/kimi/minimax |
| `seed` | 豆包/ARK | global | doubao/glm/deepseek/kimi |
| `stepfun` | 阶跃 | global | - |
| `claude` | 官方 Claude | global | - |

## 常见问题

### Q: ccc 启动后焦点不在交互框

A: 这是 PowerShell + subprocess 的已知问题，ccc 会在新窗口启动 Claude Code，手动点击交互框即可。

### Q: 认证错误 (invalid api key)

A:
1. 确认 ~/.ccm_config 中的 API Key 正确
2. 确认使用了正确的 region
3. 使用 `ccm status` 查看当前配置

### Q: 如何切回官方 Claude

A:
```powershell
ccm claude
# 或
ccc claude
```

### Q: 如何查看当前配置

A:
```powershell
ccm status
```
