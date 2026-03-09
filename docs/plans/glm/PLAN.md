# GLM Provider 实现计划

> **状态**: ✅ 已完成

## 概述

GLM (智谱 AI) 提供商支持双端点切换，- **China**: `https://open.bigmodel.cn/api/anthropic`
- **Global**: `https://api.z.ai/api/anthropic`

## 实现状态

✅ **已完成** - 在 Python 跨平台重构中实现

## 需求文档

详细需求请参考: [REQUIREMENTS.md](./REQUIREMENTS.md)

## Provider 信息

| 属性 | 值 |
|------|-----|
| 名称 | glm |
| 描述 | GLM (Zhipu AI) |
| 别名 | glm, glm5, glm4, glm4.6, glm4.7 |
| 区域支持 | Yes |
| 变体支持 | No |
| 默认区域 | global |

## 端点配置

### China (国内)

```bash
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_MODEL=glm-5
```

### Global (国际)

```bash
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
ANTHROPIC_MODEL=glm-5
```

## 使用方式

```bash
# 切换到 GLM 国际版 (默认)
eval "$(ccm glm)"

# 切换到 GLM 国内版
eval "$(ccm glm china)"

# 使用别名
eval "$(ccm glm5)"
```

## API Key 配置

**环境变量**: `GLM_API_KEY`

**配置文件** (`~/.ccm_config`):
```bash
GLM_API_KEY=your-glm-api-key
GLM_MODEL=glm-5
```

## 代码实现

**位置**: `src/ccm/providers/glm.py`

```python
class GLMProvider(BaseProvider):
    """GLM (Zhipu AI) provider."""

    INFO: ClassVar[ProviderInfo] = ProviderInfo(
        name="glm",
        description="GLM (Zhipu AI)",
        aliases=["glm", "glm5", "glm4", "glm4.6", "glm4.7"],
        supports_region=True,
    )

    BASE_URLS: ClassVar[dict[Region, str]] = {
        Region.GLOBAL: "https://api.z.ai/api/anthropic",
        Region.CHINA: "https://open.bigmodel.cn/api/anthropic",
    }
```

## 测试覆盖

- `test_get_glm`: 验证 provider 注册
- `test_glm_global_config`: 验证国际端点配置
- `test_glm_china_config`: 验证国内端点配置
