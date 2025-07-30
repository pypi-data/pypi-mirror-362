# AI 问答

AIS 的 AI 问答功能让您能够快速获取技术问题的答案，结合上下文感知能力，提供更准确和个性化的回答。

## 🤖 功能概览

### 核心特性
- **即时问答**：快速获取技术问题的答案
- **上下文感知**：结合当前环境信息提供更准确的答案
- **多模型支持**：支持 OpenAI、Claude、Ollama 等多种 AI 模型
- **流式输出**：实时显示 AI 处理进度
- **历史记录**：保存问答历史，便于回顾

## 🚀 基本使用

### 简单问答
```bash
# 基本问答
ais ask "如何使用 Docker 创建容器？"

# 询问编程问题
ais ask "Python 中如何处理异常？"

# 询问系统问题
ais ask "如何查看 Linux 系统的内存使用情况？"
```

### 带上下文的问答
```bash
# 在项目目录中询问相关问题
cd /path/to/python-project
ais ask "如何优化这个项目的性能？"

# 询问当前环境相关问题
ais ask "为什么我的 Docker 容器无法启动？"
```

## 🎯 高级功能

### 多轮对话
```bash
# 开始对话
ais ask "什么是 Kubernetes？"

# 继续对话
ais ask "如何部署应用到 Kubernetes？"

# 深入探讨
ais ask "Kubernetes 和 Docker 有什么区别？"
```

### 技术领域问答
```bash
# 前端开发
ais ask "React 中如何实现状态管理？"

# 后端开发
ais ask "如何设计 RESTful API？"

# 数据库
ais ask "MySQL 和 PostgreSQL 有什么区别？"

# 运维
ais ask "如何监控服务器性能？"
```

## 📊 上下文感知

### 环境信息整合
AIS 会自动收集以下环境信息来提供更准确的回答：

```bash
# 系统信息
- 操作系统类型和版本
- 当前工作目录
- 项目类型（Git 仓库、Python 项目等）

# 开发环境
- 编程语言版本
- 已安装的包和工具
- 配置文件信息

# 运行状态
- 当前进程
- 网络状态
- 资源使用情况
```

### 个性化回答
```bash
# 基于您的技能水平调整回答深度
ais ask "如何学习 Docker？"
# 回答会根据您的历史问题和错误分析调整复杂度

# 基于您的项目环境提供针对性建议
ais ask "如何优化这个应用？"
# 回答会考虑您的项目类型、技术栈和配置
```

## 🔧 配置选项

### 基本配置
```bash
# 设置默认 AI 提供商
ais config set ai-provider openai

# 设置回答语言
ais config set language zh-CN

# 设置回答详细程度
ais config set answer-detail-level standard
```

### 高级配置
```bash
# 启用上下文感知
ais config set context-aware true

# 设置上下文收集级别
ais config set context-level standard

# 启用历史记录
ais config set save-history true
```

## 🎨 输出格式

### Rich 格式输出
```bash
# 默认使用 Rich 格式，包含：
- 彩色语法高亮
- 代码块美化
- 表格和列表格式化
- 进度条和状态提示
```

### 流式输出
```bash
# 启用流式输出
ais config set enable-streaming true

# 设置流式输出模式
ais config set stream-mode progressive  # 步骤化显示
ais config set stream-mode realtime     # 实时进度条
ais config set stream-mode spinner      # 简单转圈
```

## 📚 使用场景

### 开发者
```bash
# 调试帮助
ais ask "这个错误是什么意思：ImportError: No module named 'requests'"

# 代码优化
ais ask "如何优化这段 Python 代码的性能？"

# 架构设计
ais ask "如何设计一个高并发的 Web 服务？"
```

### 系统管理员
```bash
# 系统诊断
ais ask "服务器 CPU 使用率过高怎么办？"

# 配置管理
ais ask "如何配置 Nginx 反向代理？"

# 安全问题
ais ask "如何加强 Linux 服务器的安全性？"
```

### 学习者
```bash
# 概念理解
ais ask "什么是微服务架构？"

# 技术选型
ais ask "Python 和 Java 哪个更适合后端开发？"

# 最佳实践
ais ask "Web 开发有哪些最佳实践？"
```

## 🔍 问答历史

### 查看历史
```bash
# 查看最近的问答
ais history --type ask --limit 10

# 搜索历史问答
ais history --search "Docker"

# 查看特定时间的问答
ais history --date 2024-01-01 --type ask
```

### 历史管理
```bash
# 清空问答历史
ais history clear --type ask

# 导出问答历史
ais history export --type ask questions.json

# 导入问答历史
ais history import questions.json
```

## 🤝 多 AI 提供商支持

### OpenAI
```bash
# 配置 OpenAI
ais provider-add openai \
  --url https://api.openai.com/v1/chat/completions \
  --model gpt-3.5-turbo \
  --api-key YOUR_API_KEY

# 使用 OpenAI
ais provider-use openai
ais ask "测试 OpenAI 连接"
```

### Claude
```bash
# 配置 Claude
ais provider-add claude \
  --url https://api.anthropic.com/v1/messages \
  --model claude-3-sonnet-20240229 \
  --api-key YOUR_API_KEY

# 使用 Claude
ais provider-use claude
ais ask "测试 Claude 连接"
```

### Ollama（本地）
```bash
# 配置 Ollama
ais provider-add ollama \
  --url http://localhost:11434/v1/chat/completions \
  --model llama2

# 使用 Ollama
ais provider-use ollama
ais ask "测试本地 AI 连接"
```

## 🔒 隐私保护

### 敏感信息过滤
```bash
# 自动过滤敏感信息
ais ask "如何配置数据库连接？"
# 您的实际数据库密码不会被发送给 AI

# 查看过滤规则
ais config show privacy-filters
```

### 本地 AI 使用
```bash
# 使用本地 AI 模型保护隐私
ais provider-use ollama
ais ask "这样就不会向外部服务发送数据"
```

## 📊 性能优化

### 缓存机制
```bash
# 启用答案缓存
ais config set enable-cache true

# 设置缓存过期时间
ais config set cache-ttl 3600

# 清空缓存
ais config clear-cache
```

### 异步处理
```bash
# 启用异步处理
ais config set async-processing true

# 设置并发数
ais config set max-concurrent 3
```

## 🎓 学习集成

### 与学习系统结合
```bash
# 基于问答生成学习内容
ais ask "什么是 Docker？"
# 然后运行: ais learn docker

# 将问答转换为学习笔记
ais ask "如何使用 Git 分支？" --save-as-learning
```

### 知识图谱
```bash
# 查看相关知识点
ais ask "什么是 Kubernetes？" --show-related

# 构建知识图谱
ais knowledge-graph --topic "容器化技术"
```

---

## 下一步

- [学习系统](./learning-system) - 系统化学习技术知识
- [错误分析](./error-analysis) - 智能错误分析功能
- [提供商管理](./provider-management) - 管理 AI 提供商

---

::: tip 提示
AI 问答功能会随着使用变得更加智能，建议开启历史记录以获得更好的体验。
:::

::: info 上下文感知
AIS 会自动收集环境信息来提供更准确的回答，您可以在隐私设置中调整收集级别。
:::

::: warning 注意
使用外部 AI 服务时，请注意数据隐私。推荐使用本地 AI 模型处理敏感信息。
:::