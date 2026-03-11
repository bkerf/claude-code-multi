# Claude Code Multi (ccm)

[English](README.md) | [中文](README_CN.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**统一动态配置系统 - 一个配置文件，管理所有 AI 提供商**

## ⚠️ 重要变更 (v3.0.0)

**新配置系统已启用，不向后兼容旧版本！**

- ✅ 新配置文件：`~/.ccm_services.toml`
- ✅ 统一认证变量：`ANTHROPIC_AUTH_TOKEN`
- ✅ 动态服务命令：`ccm <service-name>`
- ❌ 废弃：`~/.ccm_config`、`ANTHROPIC_API_KEY`、`ccm kimi china`

**迁移：**
1. `cp ccm_services.template ~/.ccm_services.toml`
2. 填写 API Key
3. 使用新命令：`ccm kimi-cn` 而不是 `ccm kimi china`

---

## 安装

```bash
git clone https://github.com/bkerf/claude-code-multi.git
cd claude-code-multi
pip install -e .
```

**Windows**: 详见 [docs/WINDOWS_INSTALL.md](docs/WINDOWS_INSTALL.md)

---

## 配置

```bash
cp ccm_services.template ~/.ccm_services.toml
ccm config  # 编辑配置文件
```

---

## 使用

```bash
ccm list              # 列出所有服务
ccm status            # 查看当前配置
ccm kimi-cn           # 切换服务
ccc kimi-cn           # 切换并启动 Claude Code
```

**支持 20+ 服务**: Kimi、GLM、MiniMax、DeepSeek、阿里云、Seed、StepFun、Claude、OpenRouter 等。

详见 [docs/README_INDEX.md](docs/README_INDEX.md)

---

## License

MIT License - see [LICENSE](LICENSE)
