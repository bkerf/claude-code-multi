# CLAUDE.md

> Claude Code 模型切换 CLI (Python 版)。本文档只包含项目特有约束，通用规范见全局 `~/.claude/CLAUDE.md`。

**⚠️ 最核心约束：永远禁止向后兼容！** 详见 `docs/CORE_RULES.md` 和全局 CLAUDE.md。

# 禁止在项目库代码中出现任何api key
## 项目定位

Python CLI 通过环境变量切换 Claude Code 的 AI 提供商。

## 命令

```bash
ccm <provider> [region]    # 当前 shell 切换
ccc <provider> [region]    # 切换 + 启动 Claude Code
ccm status                 # 查看当前配置
ccm list                   # 列出所有 provider
```

## Provider

| 命令              | 提供商             | 说明                                                      | 区域 |
| ----------------- | ------------------ | --------------------------------------------------------- | ---- |
| `ali <variant>`   | 阿里云 Coding Plan | qwen/kimi/glm/minimax                                     | Yes  |
| `kimi`            | Kimi (月之暗面)    | 直连                                                      | Yes  |
| `glm`             | GLM (智谱)         | 直连                                                      | Yes  |
| `minimax`         | MiniMax            | 直连                                                      | Yes  |
| `deepseek`        | DeepSeek           | -                                                         | No   |
| `seed [variant]`  | 豆包/ARK           | doubao/glm/deepseek/kimi                                  | No   |
| `stepfun`         | StepFun (阶跃)     | -                                                         | No   |
| `claude`          | Claude (官方)      | -                                                         | No   |
| `open <provider>` | OpenRouter         | claude/kimi/deepseek/glm/ali/minimax/stepfun/stepfun-free | No   |

## 项目结构

```
claude-code-multi/
├── src/ccm/
│   ├── cli.py             # CLI 入口 (switch, status, list, set)
│   ├── launcher.py        # ccc 启动器
│   ├── config.py          # 配置管理
│   ├── providers/         # Provider 实现
│   │   ├── base.py        # BaseProvider, ProviderConfig, Region
│   │   ├── ali.py         # 阿里云 (variants: qwen/kimi/glm/minimax)
│   │   ├── kimi.py        # Kimi
│   │   ├── glm.py         # GLM
│   │   ├── minimax.py     # MiniMax
│   │   ├── deepseek.py    # DeepSeek
│   │   ├── seed.py        # 豆包/ARK
│   │   ├── stepfun.py     # StepFun
│   │   ├── claude.py      # 官方 Claude
│   │   └── openrouter.py  # OpenRouter
│   ├── settings/          # 配置存储
│   │   ├── user.py        # 用户级配置
│   │   └── project.py     # 项目级配置
│   └── accounts/          # 账号管理
│       ├── manager.py     # 账号管理器
│       └── keychain.py    # 系统 Keychain
├── tests/
│   └── test_providers.py  # Provider 测试
└── pyproject.toml         # 项目配置
```

## 关键模式

| 模式       | 说明                                                    |
| ---------- | ------------------------------------------------------- |
| 配置优先级 | `环境变量` > `项目配置` > `用户配置` > `内置默认`       |
| 导出模式   | `switch_provider()` 输出 export 语句，调用方 eval 执行  |
| 区域       | `china` (默认) \| `global`                              |
| 变体       | 部分 provider 支持模型变体 (ali: qwen/kimi/glm/minimax) |

## 开发约束

### 禁止向后兼容

- ❌ 删除的功能不再保留别名
- ❌ 旧命令直接报错，不静默 fallback
- ✅ 用户看到错误后更新使用方式

### 新增 Provider

1. 在 `src/ccm/providers/` 创建 `xxx.py`
2. 继承 `BaseProvider`，定义 `INFO` 和 `BASE_URLS`
3. 在 `src/ccm/providers/__init__.py` 注册
4. 在 `src/ccm/cli.py` 添加命令参数处理
5. 添加单元测试

## 文档索引

```
docs/
├── plans/                      # Provider 开发计划
│   ├── ali/                    # 阿里云 Coding Plan
│   ├── glm/                    # GLM (已完成)
│   └── minimax/                # MiniMax (已完成)
├── ali/                        # 阿里云功能文档
├── CHANGELOG.md                # 版本历史
└── TROUBLESHOOTING.md          # 故障排查
```
