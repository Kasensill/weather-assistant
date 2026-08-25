# 🌦️ Weather Assistant

一个基于 **RAG（Retrieval-Augmented Generation，检索增强生成）** 的气象知识库助手。

本项目尝试将大气科学领域的知识进行结构化整理，并结合 **Embedding、向量数据库、语义检索和大语言模型**，构建一个能够理解用户自然语言问题、从气象知识库中检索相关内容并生成回答的智能助手。

项目目前处于开发阶段，主要用于探索 **RAG 知识库构建、向量检索、知识组织以及大语言模型应用**。

---

## 📌 项目简介

传统的大语言模型虽然具备较强的自然语言理解和生成能力，但对于特定领域的专业知识，仍然可能存在：

- 知识缺失
- 知识更新不及时
- 回答出现事实错误
- 无法准确引用指定知识来源
- 专业领域知识之间缺乏明确关联

因此，本项目尝试使用 RAG 架构，将大语言模型与一个专门构建的**气象知识库**结合起来。

基本工作流程为：

```text
用户问题
   ↓
问题理解
   ↓
知识检索
   ↓
从气象知识库中找到相关内容
   ↓
将检索结果提供给大语言模型
   ↓
生成最终回答
````

项目的最终目标并不仅仅是实现一个简单的聊天机器人，而是探索如何构建一个**面向大气科学领域的专业知识库助手**。

---

## 🎯 项目目标

目前项目主要围绕以下几个方向进行开发：

* [√] 建立基础气象知识库
* [√] 使用 Markdown 管理知识内容
* [√] 对气象知识进行分类整理
* [√] 建立基础的 Python 项目环境
* [√] 使用 Git / GitHub 进行项目版本管理
* [√] 对 Chroma 向量数据库进行实验
* [🚧] 完成完整的 RAG Pipeline
* [🚧] 优化文本 Chunk 切分策略
* [🚧] 优化 Embedding 策略
* [🚧] 设计知识库 Metadata
* [🚧] 优化向量检索策略
* [🚧] 增加 Query Rewrite
* [🚧] 增加 Reranker
* [🚧] 建立完整的问答流程
* [🚧] 增加对话上下文能力
* [🚧] 增加 Web UI
* [🚧] 完善气象知识体系

---

# 📚 知识库

目前知识库采用 **Markdown 文件**进行组织。

知识按照不同的主题进行分类，便于后续进行：

* 文档管理
* 文本切分
* Embedding
* 向量化存储
* 语义检索
* 知识更新

当前知识库结构如下：

```text
knowledge_base/
│
├── 01_基础概念/
│   ├── 大气环流.md
│   ├── 对流.md
│   ├── 锋面.md
│   ├── 科里奥利力.md
│   ├── 气团.md
│   ├── 气压.md
│   └── 湿度.md
│
└── 02_天气现象/
    ├── 雾和霾.md
    └── 彩虹.md
```

知识库目前仍处于持续扩充阶段。

后续计划增加更多大气科学相关内容，包括但不限于：

* 大气环流
* 天气系统
* 云与降水
* 热带气旋
* 温带气旋
* 高压与低压系统
* 季风
* ENSO（厄尔尼诺与拉尼娜）
* 温室效应
* 大气稳定度
* 边界层
* 水汽
* 辐射
* 数值天气预报
* 气候系统

---

# 🧠 RAG 架构

项目核心方向为构建一个面向气象领域的 RAG 系统。

基本架构计划为：

```text
                    ┌─────────────────┐
                    │     用户问题     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    Query处理     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Embedding模型   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   向量数据库     │
                    │    ChromaDB     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   相关知识检索   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   Context构建   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   大语言模型     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     最终回答     │
                    └─────────────────┘
```

目前该架构仍处于开发阶段。

---

# 🔎 检索系统

项目计划使用向量语义检索作为基础检索方式。

目前主要研究：

### Embedding

将知识库中的文本转换为向量表示，使语义相近的文本在向量空间中具有更高的相似度。

当前状态：

> 🚧 开发中

---

### ChromaDB

使用 Chroma 作为项目的向量数据库，用于保存知识库文本对应的向量以及相关 Metadata。

当前状态：

> 🚧 开发中

---

### Chunk

知识库中的 Markdown 文档不会直接作为一个整体进行向量化，而是需要根据内容结构进行合理切分。

当前主要研究：

* Chunk 大小
* Chunk 重叠
* Markdown 标题结构
* 语义完整性
* Chunk 与检索效果之间的关系

当前状态：

> 🚧 开发中

---

### Metadata

计划为知识库中的文本块增加 Metadata，例如：

```text
category
title
source
section
document
```

从而使后续检索不仅依赖向量相似度，还能够结合知识类别等信息进行过滤和优化。

当前状态：

> 🚧 开发中

---

# 🤖 Query Processing

用户提出的问题并不一定适合直接进行向量检索。

例如：

```text
为什么夏天会有雷暴？
```

可能需要进一步分析问题中的：

* 核心概念
* 因果关系
* 领域实体
* 查询意图

因此后续计划增加 Query Processing 模块。

计划包括：

* Query Rewrite
* Query Expansion
* 查询意图识别
* 多查询检索

当前状态：

> 🚧 开发中

---

# 🎯 Reranker

单纯依靠向量相似度进行 Top-K 检索并不一定能够得到最相关的知识。

因此后续计划增加 Reranker，对初步检索结果进行二次排序。

计划流程：

```text
用户问题
   ↓
向量检索
   ↓
Top-K候选文档
   ↓
Reranker
   ↓
重新排序
   ↓
选择最相关内容
```

当前状态：

> 🚧 开发中

---

# 📖 学习笔记

项目根目录下的 `md/` 文件夹用于保存开发过程中产生的学习笔记、技术研究以及设计思考。

目前主要涉及：

* Python
* RAG
* Embedding
* ChromaDB
* 向量距离
* Chunk
* Metadata
* 检索策略
* 大语言模型
* 项目架构设计
* Git / GitHub

这些内容不仅用于记录学习过程，也用于记录项目在设计和开发过程中产生的思考。

```text
md/
├── ...
├── ...
└── ...
```

笔记内容会随着项目开发持续更新。

---

# 🛠️ 技术栈

目前项目主要使用或计划使用以下技术：

| 技术            | 用途       | 状态     |
| ------------- | -------- | ------ |
| Python        | 项目主要开发语言 | ✅ 使用中  |
| Markdown      | 知识库内容管理  | ✅ 使用中  |
| Git           | 版本控制     | ✅ 使用中  |
| GitHub        | 项目托管     | ✅ 使用中  |
| ChromaDB      | 向量数据库    | 🚧 开发中 |
| Embedding     | 文本向量化    | 🚧 开发中 |
| RAG           | 知识增强问答   | 🚧 开发中 |
| LLM           | 自然语言生成   | 🚧 开发中 |
| Reranker      | 检索结果重排序  | 🚧 计划中 |
| Query Rewrite | 查询优化     | 🚧 计划中 |
| Web UI        | 用户交互界面   | 🚧 计划中 |

---

# 📂 项目结构

当前项目整体结构：

```text
weather-assistant/
│
├── knowledge_base/           # 气象知识库
│   │
│   ├── 01_基础概念/
│   │   ├── 大气环流.md
│   │   ├── 对流.md
│   │   ├── 锋面.md
│   │   ├── 科里奥利力.md
│   │   ├── 气团.md
│   │   ├── 气压.md
│   │   └── 湿度.md
│   │
│   └── 02_天气现象/
│       ├── 雾和霾.md
│       └── 彩虹.md
│
├── md/                       # 学习笔记与项目设计记录
│
├── src/                      # 项目源代码
│
├── .env                      # 本地环境变量，不提交到 Git
├── .env.example              # 环境变量模板
├── .gitignore
├── README.md
└── requirements.txt
```

> 项目结构目前仍在调整中，随着功能增加可能发生变化。

---

# ⚙️ 环境要求

目前项目主要开发环境：

* Python 3.10+
* Git
* GitHub
* ChromaDB
* 可用的大语言模型 API

具体 Python 依赖请参考：

```text
requirements.txt
```

---

# 🚀 快速开始

## 1. 克隆项目

```bash
git clone https://github.com/Kasensill/weather-assistant.git
```

进入项目目录：

```bash
cd weather-assistant
```

---

## 2. 创建 Python 虚拟环境

Windows：

```powershell
python -m venv venv
```

激活虚拟环境：

```powershell
venv\Scripts\activate
```

---

## 3. 安装依赖

```powershell
pip install -r requirements.txt
```

---

## 4. 配置环境变量

项目使用 `.env` 保存本地环境变量。

首先复制：

```text
.env.example
```

创建：

```text
.env
```

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

然后根据自己的模型服务配置 `.env`。

例如：

```env
OPENAI_API_KEY=your_api_key_here
```

> `.env` 文件包含敏感信息，不应提交到 GitHub。

---

# 🔐 环境变量

项目使用 `.env.example` 作为环境变量配置模板。

示例：

```env
# LLM API
OPENAI_API_KEY=

# Optional
# OPENAI_BASE_URL=

# ChromaDB
# CHROMA_HOST=
# CHROMA_PORT=
```

实际使用时请复制 `.env.example` 为 `.env`，并填写自己的配置。

**不要将真实 API Key、Token 或其他敏感信息提交到 GitHub。**

---

# ▶️ 运行项目

当前项目启动方式仍在开发中。

> 🚧 开发中

后续将在项目完成基础 RAG Pipeline 后补充完整的启动方式。

预计使用类似：

```bash
python main.py
```

或：

```bash
python -m src
```

具体启动方式以项目最终结构为准。

---

# 🧪 当前开发阶段

目前项目主要处于 **RAG 基础设施和知识库建设阶段**。

当前重点并不是立即构建一个复杂的聊天界面，而是首先解决：

1. 如何组织气象知识
2. 如何合理切分 Markdown 文档
3. 如何生成 Embedding
4. 如何使用 Chroma 存储向量
5. 如何进行语义检索
6. 如何评价检索结果
7. 如何将检索结果提供给 LLM
8. 如何减少 RAG 中的错误回答

因此，项目当前更偏向于：

> **知识库构建 + RAG 技术研究 + 实验性项目**

而不是一个已经完成的生产级应用。

---

# 🗺️ Roadmap

## Phase 1：知识库建设

* [√] 建立知识库目录
* [√] 建立基础概念分类
* [√] 建立天气现象分类
* [√] 使用 Markdown 编写知识
* [ ] 扩充气象知识内容
* [ ] 建立更加完整的知识分类体系
* [ ] 建立知识之间的关联关系

---

## Phase 2：向量数据库

* [√] 学习向量数据库基本概念
* [√] 学习 Chroma
* [ ] Markdown 文档读取
* [ ] 文档 Chunk
* [ ] Embedding
* [ ] 写入 Chroma
* [ ] Metadata 设计
* [ ] 向量检索
* [ ] 检索效果测试

---

## Phase 3：RAG Pipeline

* [ ] 用户 Query
* [ ] Query Processing
* [ ] Retriever
* [ ] Context 构建
* [ ] Prompt 构建
* [ ] LLM Generation
* [ ] 最终回答

---

## Phase 4：检索优化

* [ ] Chunk 优化
* [ ] Embedding 对比
* [ ] Top-K 调整
* [ ] Metadata Filtering
* [ ] Query Rewrite
* [ ] Query Expansion
* [ ] Reranker
* [ ] Hybrid Search

---

## Phase 5：问答系统

* [ ] 多轮对话
* [ ] Conversation Memory
* [ ] 对话上下文管理
* [ ] 来源引用
* [ ] 检索结果展示
* [ ] 回答可信度优化

---

## Phase 6：用户界面

* [ ] Web UI
* [ ] Chat Interface
* [ ] 知识库浏览
* [ ] 检索结果展示
* [ ] 来源文档展示
* [ ] 知识库管理

---

# 🔬 项目研究方向

本项目除了实现一个气象知识库助手，也用于探索以下问题：

### 1. 知识应该如何组织？

气象知识并不是简单的独立文档。

例如：

```text
气压
 ↓
气压梯度力
 ↓
风
 ↓
大气环流
```

以及：

```text
水汽
 ↓
凝结
 ↓
云
 ↓
降水
```

因此后续需要探索如何表达知识之间的关联。

---

### 2. Chunk 应该如何切？

如果一个知识文档过长，直接进行向量化可能导致：

* 语义范围过大
* 检索结果不够精确
* Context 中包含大量无关内容

但如果切得过小，又可能导致：

* 上下文丢失
* 知识不完整
* 语义关系被破坏

因此 Chunk 策略是本项目重点研究的问题之一。

---

### 3. 向量距离究竟意味着什么？

项目在学习 Chroma 和 Embedding 的过程中，也会研究：

* Cosine Similarity
* Euclidean Distance
* L2 Distance
* Inner Product
* Embedding 空间
* 向量相似度

并尝试理解：

> 一个“语义相似度”数字到底代表什么？

---

### 4. RAG 是否真的能够减少错误？

项目后续会尝试通过实验比较：

```text
LLM
vs
LLM + RAG
```

在气象领域问题上的回答差异。

重点关注：

* 正确率
* 相关性
* 知识覆盖率
* 幻觉
* 来源可靠性
* 检索准确率

---

# 📊 Evaluation

目前尚未建立完整的 RAG 评测体系。

> 🚧 开发中

未来计划建立气象领域测试集，对以下指标进行评估：

* Retrieval Accuracy
* Context Relevance
* Answer Relevance
* Faithfulness
* Recall
* Precision

并比较不同：

* Chunk 策略
* Embedding 模型
* Top-K
* Retriever
* Reranker

对最终回答效果的影响。

---

# 📝 开发记录

项目开发过程中产生的学习笔记和技术思考保存在：

```text
md/
```

其中会记录：

* 技术原理
* 实验过程
* 问题分析
* Debug 记录
* RAG 设计
* Chroma 实验
* 向量检索理解
* 项目架构调整
* 开发过程中的思考

这些记录会随着项目持续开发不断更新。

---

# 🚧 项目状态

**Current Status: Early Development**

目前项目仍处于早期开发阶段。

当前主要完成：

* 基础项目创建
* Git / GitHub 项目管理
* 气象知识库初步建立
* Markdown 知识管理
* RAG 与 Chroma 技术学习
* 基础架构探索

RAG Pipeline、检索优化以及最终用户界面仍在开发中。

---

# 🤝 Contributing

目前项目主要用于个人学习与研究，因此暂未建立正式的 Contribution 流程。

如果未来项目开放贡献，将在这里补充：

* Issue
* Pull Request
* Contribution Guide
* Code Style
* Knowledge Base Contribution Rules

---

# 📄 License

This project is licensed under the MIT License.

---

# 🌦️ About

**Weather Assistant** 是一个面向气象领域的 RAG 知识库助手实验项目。

项目希望探索一个问题：

> **如果把大气科学知识进行合理组织，并交给 RAG 系统进行检索，大语言模型能否成为一个真正理解气象知识的专业助手？**

项目仍在持续开发中。

```
```
