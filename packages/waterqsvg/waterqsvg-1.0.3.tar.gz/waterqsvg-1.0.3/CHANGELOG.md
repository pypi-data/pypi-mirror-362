# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 🌊 WaterQSVG - Water Quality SVG Generator 专业水质数据可视化工具
- 🔗 OSS直连下载支持，直接从阿里云OSS下载ZIP数据包
- 📊 15+种水质指标自动识别和处理
- 🎨 多种颜色映射方案 (jet, viridis, water_quality, RdYlBu_r等)
- 🗺️ 高精度地理边界信息输出，适合地图叠加
- 🧮 Alpha Shape边界检测算法，精确插值边界
- 📱 跨平台兼容 (Windows/Linux/macOS)

### Features
- **智能指标识别**: 自动处理已知指标，未知指标保持原始名称
- **双重输入支持**: 支持直接URL和JSON配置文件两种输入方式
- **CLI工具**: 提供 `waterqsvg` 命令行工具
- **Python API**: 完整的编程接口支持
- **高质量SVG输出**: 透明背景矢量图，完美地图叠加
- **时间戳管理**: 自动创建时间戳文件夹管理输出
- **完整日志系统**: 详细的处理日志和错误报告

### Technical
- 标准Python包结构 (`src/waterqsvg/`)
- 使用 `setuptools-scm` 进行版本管理
- 支持现代Python 3.11+
- 完整的CI/CD流程 (GitHub Actions)

### Data Processing
- **数据格式支持**: INDEXS.CSV + POS.TXT格式
- **数据标准化**: 智能列名和指标名称映射
- **数据验证**: 完整的数据质量检查
- **插值算法**: 高分辨率网格插值 (400x400+)

### Supported Indicators
- 化学需氧量 (COD/CODCr)
- 高锰酸盐指数 (CODMn)
- 氨氮 (NH3-N)
- 总氮 (TN)
- 总磷 (TP)
- 溶解氧 (DO)
- pH值
- 浊度 (Turbidity)
- 叶绿素a (Chl-a)
- 蓝绿藻 (BGA)
- 电导率 (EC)
- 盐度 (Salinity)
- 总溶解固体 (TDS)
- 氧化还原电位 (ORP)
- 生化需氧量 (BOD)
- 总悬浮物 (TSS)

## [1.0.0] - 2024-07-09

### Added
- 初始版本发布
- 基础SVG热力图生成功能
- OSS数据下载和处理
- 水质指标标准化
- 地理边界信息输出

---

**Version Format**: `vX.Y.Z`
- `X`: 主版本号 (破坏性更改)
- `Y`: 次版本号 (新功能)
- `Z`: 修订版本号 (bug修复)