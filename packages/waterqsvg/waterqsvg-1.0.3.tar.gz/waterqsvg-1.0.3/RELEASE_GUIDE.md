# WaterQSVG 发布指南

## 🚀 发布步骤

### 1. 准备发布

1. **确认功能完整性**
   ```bash
   # 测试所有功能
   uv run python interface.py --help
   uv run waterqsvg --help
   uv run python -c "import waterqsvg; print(waterqsvg.__version__)"
   ```

2. **更新版本文档**
   - 更新 `CHANGELOG.md`
   - 确认 `README.md` 内容准确
   - 检查 `pyproject.toml` 中的元数据

### 2. 创建发布标签

```bash
# 确保所有更改已提交
git add .
git commit -m "准备发布 v1.0.0"

# 推送到远程
git push origin main

# 创建并推送标签
git tag -a v1.0.0 -m "WaterQSVG v1.0.0 发布"
git push origin v1.0.0
```

### 3. 自动化发布

标签推送后，GitHub Actions 会自动：

1. **多平台测试** (`test.yml`)
   - 在多平台测试 (Ubuntu/Windows/macOS)
   - 测试 Python 3.11 和 3.12
   - 验证包构建和安装

2. **一键发布** (`release-and-publish.yml`)
   - 构建分发包
   - 验证包完整性
   - 发布到 PyPI
   - 创建 GitHub Release
   - 上传构建产物

3. **备用发布** (`release.yml`)
   - 备用的发布流程
   - 可用于调试或特殊情况

### 4. 手动发布 (如果需要)

如果自动发布失败，可以手动发布：

```bash
# 构建包
uv build

# 检查包
python -m pip install twine
python -m twine check dist/*

# 上传到 PyPI
python -m twine upload dist/*
```

### 5. 发布后验证

```bash
# 验证 PyPI 安装
pip install waterqsvg

# 测试功能
waterqsvg --help

# 验证版本
python -c "import waterqsvg; print(waterqsvg.__version__)"
```

## 🔧 GitHub Actions 配置

### 所需 Secrets

1. **PyPI API Token** (如果不使用可信发布)
   - 在 GitHub 仓库 Settings > Secrets 中添加 `PYPI_API_TOKEN`

2. **可信发布** (推荐)
   - 在 PyPI 项目设置中配置 GitHub Actions 可信发布
   - 无需手动管理 API Token

### 工作流说明

1. **test.yml** - 持续集成测试
   - 触发: push 到 main/dev 分支，PR 到 main 分支
   - 矩阵测试: 多平台 × 多 Python 版本

2. **release-and-publish.yml** - 一键发布 (主要)
   - 触发: 推送 `v*` 标签
   - 功能: 构建、测试、发布到 PyPI、创建 GitHub Release
   - 特点: 一步完成所有发布流程

3. **release.yml** - 备用发布
   - 触发: 推送 `v*` 标签
   - 功能: 构建、测试、发布到 PyPI、创建 GitHub Release
   - 用途: 作为备用或调试使用

## 📦 包发布检查清单

发布前请确认：

- [ ] 所有测试通过
- [ ] 功能完整且无 Bug
- [ ] 文档准确完整
- [ ] 版本号正确
- [ ] CHANGELOG.md 已更新
- [ ] GitHub Actions 配置正确
- [ ] PyPI 可信发布已配置
- [ ] 包元数据正确

## 🎯 发布后任务

- [ ] 验证 PyPI 安装
- [ ] 测试所有主要功能
- [ ] 更新相关文档
- [ ] 通知用户新版本发布
- [ ] 准备下一个版本的开发

## 📚 相关链接

- [PyPI 项目页面](https://pypi.org/project/waterqsvg/)
- [GitHub Releases](https://github.com/1034378361/waterqsvg/releases)
- [GitHub Actions](https://github.com/1034378361/waterqsvg/actions)
- [PyPI 可信发布文档](https://docs.pypi.org/trusted-publishers/)

---

**注意**: 确保在发布前进行充分测试，包括在不同环境中验证包的功能。