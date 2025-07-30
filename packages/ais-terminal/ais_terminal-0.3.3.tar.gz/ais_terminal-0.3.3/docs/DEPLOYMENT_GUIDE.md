# AIS 部署指南

本指南将帮助你将 AIS 项目部署到生产环境，包括 GitHub 仓库设置、PyPI 发布等。

## 📋 部署检查清单

### 1. GitHub 仓库设置

#### ✅ 基本设置
- [x] 仓库地址已更新：`https://github.com/kangvcar/ais`
- [x] 所有文件中的链接已更新
- [x] README.md 包含完整的安装和使用说明

#### 🔑 Secrets 配置
需要在 GitHub 仓库的 Settings > Secrets and variables > Actions 中添加：

```
PYPI_API_TOKEN=your_pypi_api_token_here
```

获取 PyPI API Token：
1. 访问 https://pypi.org/manage/account/token/
2. 创建新的 API token
3. 设置 scope 为整个账户或特定项目
4. 复制 token 到 GitHub Secrets

#### 📋 仓库描述
建议设置仓库描述：
```
AIS - 上下文感知的错误分析学习助手，通过深度Shell集成架构实现多维上下文感知和智能错误分析
```

### 2. 发布流程

#### 🏷️ 创建第一个发布版本
```bash
# 1. 确保所有更改已提交
git add .
git commit -m "准备发布 v0.1.0"

# 2. 创建标签
git tag -a v0.1.0 -m "首次发布 AIS v0.1.0"

# 3. 推送到 GitHub
git push origin main
git push origin v0.1.0
```

#### 🚀 自动发布到 PyPI
当你在 GitHub 上创建 Release 时，GitHub Actions 会自动：
1. 运行测试套件
2. 构建 Python 包
3. 发布到 PyPI

手动创建 Release：
1. 访问 https://github.com/kangvcar/ais/releases
2. 点击 "Create a new release"
3. 选择标签 `v0.1.0`
4. 填写发布说明
5. 点击 "Publish release"

#### 🛠️ 手动发布（备选方案）
```bash
# 使用项目提供的发布脚本
chmod +x release.sh
./release.sh 0.1.0

# 或者手动执行
python -m build
python -m twine upload dist/*
```

### 3. 用户安装验证

#### 测试安装链接
发布后，测试以下安装方式：

```bash
# 一键安装
curl -sSL https://raw.githubusercontent.com/kangvcar/ais/main/install.sh | bash

# 从 PyPI 安装
pipx install ais-terminal

# 从源码安装
git clone https://github.com/kangvcar/ais.git
cd ais && pipx install -e .
```

#### 功能验证
```bash
# 基本功能测试
ais --version
ais config
ais ask "hello"

# 错误分析测试  
mkdirr /tmp/test  # 故意输错

# 学习功能测试
ais learn git
```

### 4. 文档和推广

#### 📚 文档完善
- [x] README.md - 用户安装和使用指南
- [x] CHANGELOG.md - 版本更新记录
- [ ] CONTRIBUTING.md - 贡献指南（可选）
- [ ] GitHub Wiki - 详细文档（可选）

#### 🌟 推广建议
1. **在 README 中添加徽章**：
   ```markdown
   ![PyPI version](https://img.shields.io/pypi/v/ais-terminal.svg)
   ![Downloads](https://img.shields.io/pypi/dm/ais-terminal.svg)
   ![GitHub stars](https://img.shields.io/github/stars/kangvcar/ais.svg)
   ```

2. **社区分享**：
   - 发布到相关技术社区
   - 编写使用教程和技术博客
   - 参与开源项目推广活动

3. **功能演示**：
   - 录制演示视频或 GIF
   - 准备使用案例和最佳实践

### 5. 监控和维护

#### 📊 监控指标
- PyPI 下载量
- GitHub Stars 和 Issues
- 用户反馈和问题报告

#### 🔄 持续更新
- 定期更新依赖包
- 修复用户报告的问题
- 添加新功能和改进

#### 🐛 问题处理
监控以下渠道的用户反馈：
- GitHub Issues: https://github.com/kangvcar/ais/issues
- 邮件反馈（如果提供）
- 社区讨论

## 🎯 下一步行动

1. **立即执行**：
   - [ ] 设置 GitHub Secrets (PYPI_API_TOKEN)
   - [ ] 创建第一个 Release (v0.1.0)
   - [ ] 验证自动发布流程

2. **短期目标**：
   - [ ] 测试用户安装流程
   - [ ] 收集初期用户反馈
   - [ ] 修复发现的问题

3. **长期规划**：
   - [ ] 扩展功能特性
   - [ ] 支持更多平台
   - [ ] 建立用户社区

## 📞 技术支持

如果在部署过程中遇到问题，可以：
1. 查看 GitHub Actions 日志
2. 检查 PyPI 发布状态
3. 运行本地测试脚本：`./test_installation.sh`

---

**🚀 现在你的 AIS 项目已经准备好面向用户发布了！**