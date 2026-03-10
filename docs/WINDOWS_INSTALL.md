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

**工作原理：**
- `ccc` 会自动在新的 Windows Terminal 窗口（或 PowerShell 窗口）中启动 Claude Code
- 正常加载 PowerShell profile，保留你的自定义配置
- 自动设置所有必需的环境变量（API Key、Base URL、模型配置等）
- 自动过滤包含特殊字符的环境变量名，避免 PowerShell 语法错误
- 窗口标题显示 "Claude Code" 便于识别

**优势：**
- ✅ 保留 profile 配置（别名、函数、环境变量等）
- ✅ 环境变量自动配置，无需手动设置
- ✅ 独立窗口，不影响当前终端
- ✅ 支持 Windows Terminal 和传统 PowerShell

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

### Q: ccc 启动后看不到窗口或有语法错误

A: 已修复！当前版本自动过滤了包含特殊字符的环境变量名（如 `COMMONPROGRAMFILES(X86)`），避免 PowerShell 语法错误。

**修复内容：**
- ✅ 过滤环境变量名中的括号，避免 `Unexpected token '('` 错误
- ✅ 使用 Python subprocess 直接启动，避免 PowerShell 字符串转义问题
- ✅ 保留 profile 加载，不影响你的自定义配置

如果仍有问题，请检查：
1. 是否已重新安装：`pip install -e .`
2. Python 版本是否 >= 3.10
3. 是否安装了 Claude Code：`npm install -g @anthropic-ai/claude-code`

### Q: ccc 启动后焦点不在交互框

A: 这是 Windows 窗口管理的正常行为，手动点击 Claude Code 窗口即可获得焦点。

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

### Q: PowerShell profile 有错误怎么办（Terminal-Icons 等）

A: 如果看到 `Import-PowerShellDataFile` 或其他 profile 加载错误，这是**你的 PowerShell profile 本身的问题**，不是 `ccc` 脚本的问题。

**重要说明：**
- ❌ 这些错误来自 `$PROFILE` 文件加载的模块（如 Terminal-Icons）
- ✅ `ccc` 创建的临时脚本已修复，不会有语法错误
- ✅ Terminal-Icons 错误不影响 Claude Code 的正常运行

**修复方法：**

```powershell
# 方法 1: 更新 Terminal-Icons 模块（推荐）
Update-Module Terminal-Icons -Force

# 方法 2: 升级 PowerShell 到最新版本
# 访问 https://aka.ms/PSWindows 下载安装
# 新版本 PowerShell 包含 Import-PowerShellDataFile cmdlet

# 方法 3: 临时禁用 Terminal-Icons
# 编辑 $PROFILE 文件，注释掉这一行：
# Import-Module Terminal-Icons

# 方法 4: 检查 PowerShell 版本
$PSVersionTable.PSVersion
# 如果版本 < 5.1，建议升级
```

**验证修复：**
```powershell
# 重新打开 PowerShell，应该不再有错误
# 或者手动测试：
Import-PowerShellDataFile -Path "test.psd1"
```
