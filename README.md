# Claude Code Multi (ccm)

[English](README.md) | [中文](README_CN.md)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**统一动态配置系统 - 一个配置文件，管理所有 AI 提供商**

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
# 创建配置文件
cp ccm_services.template ~/.ccm_services.toml

# 编辑配置，填写 API Key
ccm config
```

---

## 使用

```bash
# 列出所有服务
ccm list

# 查看当前配置
ccm status

# 切换服务（当前 shell）
ccm kimi-cn

# 切换服务并启动 Claude Code
ccc kimi-cn
```

**支持 20+ 服务**: Kimi、GLM、MiniMax、DeepSeek、阿里云、Seed、StepFun、Claude、OpenRouter 等

详见 [docs/README_INDEX.md](docs/README_INDEX.md)

---

## License

MIT License - see [LICENSE](LICENSE)
