# CLAUDE.md

> Claude Code 模型切换 CLI。本文档只包含项目特有约束，通用规范见全局 `~/.claude/CLAUDE.md`。

## 项目定位

Bash CLI 通过环境变量切换 Claude Code 的 AI 提供商。

## 命令

```bash
ccm <provider> [region]    # 当前 shell 切换
ccc <provider> [region]    # 切换 + 启动 Claude Code
```

## Provider

| 命令 | 提供商 | 说明 |
|------|--------|------|
| `ali[:qwen\|kimi\|glm\|minimax]` | 阿里云 Coding Plan | 4 模型 |
| `kimi [china\|global]` | Kimi (月之暗面) | 直连 |
| `glm [china\|global]` | GLM (智谱) | 直连 |
| `minimax [china\|global]` | MiniMax | 直连 |
| `deepseek` | DeepSeek | - |
| `seed [variant]` | 豆包/ARK | doubao/glm/kimi |
| `claude` | Claude (官方) | - |
| `open <provider>` | OpenRouter | - |

## 核心文件

```
claude-code-switch/
├── ccm.sh          # 核心: emit_env_exports(), resolve_model_variant()
├── ccc             # 启动器: 解析参数, eval exports, exec claude
├── install.sh      # 安装 + shell 函数
├── lang/*.json     # 国际化
└── docs/
    └── ali/        # 阿里云 Coding Plan 功能文档
```

## 关键模式

| 模式 | 说明 |
|------|------|
| 配置优先级 | `环境变量` > `~/.ccm_config` > `内置默认` |
| 导出模式 | `emit_env_exports()` 输出 export 语句，调用方 eval 执行 |
| 区域 | `china` (默认) \| `global` |

## 开发约束

### 禁止向后兼容

- ❌ 删除的功能不再保留别名
- ❌ 旧命令直接报错，不静默 fallback
- ✅ 用户看到错误后更新使用方式

### 新增 Provider

1. 在 `emit_env_exports()` 添加 case
2. 在 `resolve_model_variant()` 添加映射（如有变体）
3. 更新 `ccc` 的 usage 和 `is_known_model()`
4. 在配置模板添加默认值

## 文档索引

```
docs/
└── plans/                      # 3 Provider 并行开发
    ├── ali/                    # 阿里云 Coding Plan
    │   └── <feature>/         # 按功能分子目录
    │       ├── PLAN.md
    │       └── REQUIREMENTS.md
    ├── glm/                    # GLM (智谱)
    │   └── <feature>/
    └── minimax/                # MiniMax
        └── <feature>/
```

| 路径 | 说明 |
|------|------|
| `docs/plans/ali/model-switch/` | 阿里云多模型切换 |
| `docs/plans/glm/` | GLM 功能（待开发） |
| `docs/plans/minimax/` | MiniMax 功能（待开发） |
| `CHANGELOG.md` | 版本历史 |
| `TROUBLESHOOTING.md` | 故障排查 |
