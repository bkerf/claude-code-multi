# Windows 安装指南

## 环境要求

- Python 3.10+
- Node.js 18+ (用于 Claude Code)
- Windows 10/11

---

## 安装步骤

### 1. 克隆项目

```powershell
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
```

### 2. 安装 Python 包

```powershell
pip install -e .
```

这会创建全局命令 `ccm` 和 `ccc`。

### 3. 创建配置文件

```powershell
# 复制配置模板
cp ccm_services.template ~/.ccm_services.toml

# 编辑配置文件
ccm config
```

### 4. 填写 API Key

在打开的编辑器中，找到你要使用的服务，填写 `api_key` 字段：

```toml
[service.minimax-cn]
type = "minimax"
base_url = "https://api.minimaxi.com/anthropic"
api_key = "your-minimax-api-key"  # 填写你的 API Key
model = "MiniMax-M2.5-highspeed"
default_sonnet = "MiniMax-M2.5-highspeed"
default_opus = "MiniMax-M2.5-highspeed"
default_haiku = "MiniMax-M2.5-highspeed"
subagent_model = "MiniMax-M2.5-highspeed"
```

**所有字段必填，不可省略！**

---

## 使用方法

### 列出所有服务

```powershell
ccm list
```

### 查看当前配置

```powershell
ccm status
```

### 切换服务（当前 shell）

```powershell
ccm minimax-cn        # MiniMax 中国
ccm glm-cn            # GLM 中国
ccm kimi-cn           # Kimi 中国
ccm ali-qwen-cn       # 阿里云 Qwen 中国
ccm deepseek          # DeepSeek
```

执行后会输出 PowerShell 环境变量设置命令：

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.minimaxi.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = "your-key"
$env:ANTHROPIC_MODEL = "MiniMax-M2.5-highspeed"
# ...
```

### 切换并启动 Claude Code

```powershell
ccc minimax-cn        # 切换到 MiniMax 并启动
ccc glm-cn            # 切换到 GLM 并启动
ccc ali-qwen-cn       # 切换到阿里云 Qwen 并启动
```

**工作原理：**
- `ccc` 会在新的 Windows Terminal 窗口（或 PowerShell 窗口）中启动 Claude Code
- 自动设置所有必需的环境变量
- 自动过滤包含特殊字符的环境变量名，避免 PowerShell 语法错误
- 窗口标题显示 "Claude Code"

---

## 支持的服务

配置文件包含 20 个预定义服务：

| 服务名 | 提供商 | 区域 |
|--------|--------|------|
| `kimi-cn` | Kimi (月之暗面) | China |
| `glm-cn` | GLM (智谱) | China |
| `minimax-cn` | MiniMax | China |
| `ali-qwen-cn` | 阿里云 Qwen | China |
| `ali-kimi-cn` | 阿里云 Kimi | China |
| `ali-glm-cn` | 阿里云 GLM | China |
| `ali-minimax-cn` | 阿里云 MiniMax | China |
| `deepseek` | DeepSeek | Global |
| `seed` | Seed/Doubao (字节) | - |
| `stepfun` | StepFun (阶跃) | - |
| `claude` | Claude (官方) | - |

完整列表见 [docs/README_INDEX.md](README_INDEX.md)

---

## 常见问题

### Q: 配置文件不存在

```
❌ 配置文件不存在: ~/.ccm_services.toml
💡 复制 ccm_services.template 到 ~/.ccm_services.toml 并填写 API Key
```

**解决方法：**
```powershell
cp ccm_services.template ~/.ccm_services.toml
ccm config
```

### Q: 服务未配置 API Key

```
❌ Service 'kimi-cn' 未配置 api_key
💡 编辑 ~/.ccm_services.toml 并设置 api_key
```

**解决方法：**
打开 `~/.ccm_services.toml`，找到对应服务，填写 `api_key` 字段。

### Q: Auth conflict 告警

```
⚠️ Auth conflict: Both a token (ANTHROPIC_AUTH_TOKEN) and an API key (ANTHROPIC_API_KEY) are set.
```

**解决方法：**
```powershell
$env:ANTHROPIC_API_KEY = $null
```

### Q: ccc 启动后看不到窗口

**解决方法：**
1. 检查是否安装了 Claude Code：
   ```powershell
   npm install -g @anthropic-ai/claude-code
   ```

2. 检查 Python 版本：
   ```powershell
   python --version  # 应该 >= 3.10
   ```

3. 重新安装：
   ```powershell
   pip install -e .
   ```

### Q: 如何查看当前配置

```powershell
ccm status
```

### Q: 如何切回官方 Claude

```powershell
ccm claude
# 或
ccc claude
```

---

## 自定义服务

在 `~/.ccm_services.toml` 中添加自己的中转服务：

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
```powershell
ccm my-service
```

---

## 核心规范

详见 [CORE_RULES.md](CORE_RULES.md)

**最核心约束：永远禁止向后兼容！**
