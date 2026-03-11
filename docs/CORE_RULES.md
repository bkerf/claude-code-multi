# CCM 核心规范

> **永远禁止向后兼容！**

## 环境变量规范

### 认证变量（必须）

**唯一正确的认证变量：**
```bash
ANTHROPIC_AUTH_TOKEN=<your-api-key>
```

**❌ 禁止使用的变量：**
- `ANTHROPIC_API_KEY` - 已废弃，永不使用
- 任何其他自定义认证变量

**规则：**
1. 所有 AI 提供商统一使用 `ANTHROPIC_AUTH_TOKEN`
2. 包括 MiniMax、Kimi、GLM、DeepSeek 等所有服务
3. 不存在任何例外情况

### 配置文件规范

**唯一配置文件：**
```
~/.ccm_services.toml
```

**❌ 禁止的配置文件：**
- `~/.ccm_config` - 已废弃
- `~/.ccm_services` - 错误的文件名（缺少 .toml 扩展名）

## 开发规范

### 禁止向后兼容

**严格禁止：**
1. ❌ 不保留废弃的配置文件格式
2. ❌ 不兼容旧的环境变量名
3. ❌ 不支持旧的命令参数
4. ❌ 不添加兼容层或回退逻辑

**正确做法：**
1. ✅ 直接删除旧代码
2. ✅ 更新文档说明新用法
3. ✅ 用户看到错误后自行更新

### 配置字段规范

**所有字段必填，不可省略：**

```toml
[service.example]
type = "provider-type"           # 必填：提供商类型
base_url = "https://..."         # 必填：API 端点
api_key = "sk-..."               # 必填：API 密钥（可为空字符串）
model = "model-id"               # 必填：主模型 ID
default_sonnet = "model-id"      # 必填：Sonnet 模型
default_opus = "model-id"        # 必填：Opus 模型
default_haiku = "model-id"       # 必填：Haiku 模型
subagent_model = "model-id"      # 必填：子代理模型
```

**禁止：**
- ❌ 使用默认值
- ❌ 省略任何字段
- ❌ 使用 null 或 undefined

## 命令规范

### 新命令格式

**正确：**
```bash
ccm <service-name>     # 直接使用服务名
ccc <service-name>     # 启动 Claude Code
```

**示例：**
```bash
ccm kimi-cn           # 切换到 Kimi 中国
ccm ali-qwen-cn       # 切换到阿里云 Qwen 中国
ccm minimax-cn        # 切换到 MiniMax 中国
```

### 废弃的命令格式

**❌ 禁止使用：**
```bash
ccm kimi china        # 旧格式，已废弃
ccm ali qwen china    # 旧格式，已废弃
```

**处理方式：**
- 直接报错，不提供兼容
- 提示用户使用新命令

## 错误处理规范

### 配置错误

**明确的错误信息：**
```
❌ Service 'xxx' 未配置 api_key
💡 编辑 ~/.ccm_services.toml 并设置 api_key
```

**禁止：**
- ❌ 模糊的错误提示
- ❌ 自动回退到默认值
- ❌ 静默失败

### 环境变量冲突

**检测冲突：**
- 如果同时设置了 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_API_KEY`
- 直接报错，要求用户清除错误的变量
- 不尝试自动选择

## 代码规范

### 删除旧代码

**立即删除：**
1. 旧的 provider 实现
2. 废弃的配置解析逻辑
3. 兼容性检查代码
4. 回退逻辑

**不保留：**
- ❌ 注释掉的旧代码
- ❌ 条件判断的兼容分支
- ❌ 废弃的函数/类

### 文档更新

**同步更新：**
1. README.md
2. CHANGELOG.md
3. 所有相关文档

**删除：**
- 旧版本的使用说明
- 迁移指南（不需要）
- 兼容性说明

## 版本策略

### 破坏性更新

**直接发布：**
- 不使用 major version bump
- 不提供迁移工具
- 不保留旧版本分支

**用户责任：**
- 用户自行更新配置
- 用户自行适应新命令
- 用户自行阅读文档

## 总结

**核心原则：**
1. 简单直接，不搞复杂
2. 有问题就报错，不猜测
3. 删除旧代码，不保留
4. 用户负责更新，不兼容

**禁止的思维：**
- "为了兼容旧用户..."
- "可能有人还在用..."
- "我们应该提供迁移..."
- "先保留一个版本..."

**正确的思维：**
- "直接删除旧代码"
- "用户看到错误会更新"
- "保持代码简洁"
- "不向后兼容"
