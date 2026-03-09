# GLM Provider 需求文档

## 1. 功能需求

### 1.1 Provider 基本信息

| 属性 | 值 |
|------|-----|
| Provider ID | `glm` |
| 显示名称 | GLM (Zhipu AI) |
| 描述 | 智谱 AI 的 GLM 系列模型 |
| 命令别名 | `glm`, `glm5`, `glm4`, `glm4.6`, `glm4.7` |

### 1.2 区域支持

| 区域 | 端点 | 说明 |
|------|------|------|
| `global` | `https://api.z.ai/api/anthropic` | 国际版 API |
| `china` | `https://open.bigmodel.cn/api/anthropic` | 国内版 API |

**默认区域**: `global`

### 1.3 模型配置

| 环境变量 | 默认值 | 说明 |
|----------|-------|------|
| `GLM_MODEL` | `glm-5` | 模型 ID |
| `GLM_API_KEY` | - | API 密钥 (必需) |

---

## 2. CLI 命令规范

### 2.1 基本切换命令

```bash
# 切换到 GLM (默认 global 区域)
eval "$(ccm glm)"

# 指定区域
eval "$(ccm glm global)"
eval "$(ccm glm china)"
```

### 2.2 别名支持

```bash
# 以下命令等效
eval "$(ccm glm)"
eval "$(ccm glm5)"
```

### 2.3 输出格式

**bash/zsh 输出**:
```bash
export ANTHROPIC_BASE_URL='https://api.z.ai/api/anthropic'
export ANTHROPIC_AUTH_TOKEN='<api_key>'
export ANTHROPIC_MODEL='glm-5'
export ANTHROPIC_DEFAULT_SONNET_MODEL='glm-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='glm-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='glm-5'
export CLAUDE_CODE_SUBAGENT_MODEL='glm-5'
```

**fish 输出**:
```fish
set -gx ANTHROPIC_BASE_URL 'https://api.z.ai/api/anthropic'
set -gx ANTHROPIC_AUTH_TOKEN '<api_key>'
# ... 其他变量
```

---

## 3. 配置管理

### 3.1 配置优先级

1. 环境变量 `GLM_API_KEY` / `GLM_MODEL`
2. `~/.ccm_config` 配置文件
3. 内置默认值 (`glm-5`)

### 3.2 配置文件示例

```bash
# ~/.ccm_config
GLM_API_KEY=your-glm-api-key
GLM_MODEL=glm-5
```

### 3.3 API Key 占位符检测

以下值被视为占位符 (未配置):
- 包含 `your` + `api` + `key` 的值
- 示例: `your-glm-api-key`, `sk-your-glm-api-key`

---

## 4. 错误处理

### 4.1 未配置 API Key

**场景**: 用户执行 `ccm glm` 但未设置 `GLM_API_KEY`

**输出**:
```
❌ Please configure GLM_API_KEY
💡 Set environment variable or add to ~/.ccm_config
```

**退出码**: 1

### 4.2 无效区域

**场景**: 用户指定无效区域 `ccm glm invalid`

**输出**:
```
❌ Invalid region: invalid
💡 Usage: ccm glm [global|china]
```

**退出码**: 1

---

## 5. 状态显示

### 5.1 `ccm status` 命令输出

```
🔧 API Keys Status
   GLM_API_KEY: [Set]
```

或

```
   GLM_API_KEY: [Not Set]
```

### 5.2 `ccm list` 命令输出

```
| Provider | Description     | Region | Variants |
|---------|-----------------|--------|----------|
| glm     | GLM (Zhipu AI)  | Yes    | -        |
```

---

## 6. 代码实现要求

### 6.1 文件位置

`src/ccm/providers/glm.py`

### 6.2 类结构

```python
class GLMProvider(BaseProvider):
    """GLM (Zhipu AI) provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="glm",
        description="GLM (Zhipu AI)",
        aliases=["glm", "glm5", "glm4", "glm4.6", "glm4.7"],
        supports_region=True,
        supports_variant=False,
    )

    BASE_URLS: ClassVar[dict[Region, str]] = {
        Region.GLOBAL: "https://api.z.ai/api/anthropic",
        Region.CHINA: "https://open.bigmodel.cn/api/anthropic",
    }
```

### 6.3 方法要求

| 方法 | 说明 |
|------|------|
| `get_info()` | 返回 ProviderInfo |
| `get_config(api_key, variant, region, model_override)` | 返回 ProviderConfig |
| `format_exports(config, shell)` | 格式化导出语句 |

---

## 7. 测试覆盖

### 7.1 单元测试

| 测试用例 | 验证内容 |
|----------|----------|
| `test_get_glm` | Provider 注册正确 |
| `test_glm_global_config` | 国际端点配置正确 |
| `test_glm_china_config` | 国内端点配置正确 |

### 7.2 集成测试

```bash
# 手动测试步骤
1. 配置 GLM_API_KEY
2. 执行 eval "$(ccm glm)"
3. 验证环境变量设置正确
4. 执行 eval "$(ccm glm china)"
5. 验证端点切换到国内
```

---

## 8. 兼容性说明

### 8.1 与 Bash 版本兼容

Python 版本应与原 Bash 版本行为一致:

**Bash 版本端点** (ccm.sh):
```bash
# global
base_url="https://api.z.ai/api/anthropic"
# china
base_url="https://open.bigmodel.cn/api/anthropic"
```

### 8.2 迁移说明

用户无需修改现有配置:
- `~/.ccm_config` 格式保持不变
- 环境变量名保持不变
- CLI 命令语法保持不变

---

## 9. 验收标准

- [ ] `ccm glm` 输出正确的 export 语句
- [ ] `ccm glm china` 切换到国内端点
- [ ] `ccm status` 正确显示 API Key 状态
- [ ] `ccm list` 正确显示 GLM provider 信息
- [ ] 未配置 API Key 时显示友好错误信息
- [ ] 单元测试全部通过
