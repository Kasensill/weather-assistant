# Agent（智能体）

这是现在招聘核心。
Agent本质：就是不断构造新的Context，然后循环。
Agent工程 ≈ Context工程 + Tool调用 + Loop（循环）

# 与普通LLM的区别：
## 普通LLM：

      用户
      |
      LLM
      |
      答案

## Agent：

           用户
            |
           Agent
            |
      ----------------
       |    |      |
      LLM  工具    记忆
       |
      规划
       |
      执行
       |
      反馈

# 举个例子：
## 用户：

帮我分析XXX情况

## 普通模型：

回答一段文字。

## Agent：

可能：

查询数据库
调接口
获取统计数据
运行Python分析
生成报告

# Agent核心：
四个能力：

## 1. Planning（规划）

拆任务。

## 2. Tool Use（工具调用）

调用：

搜索
数据库
API
Python

## 3. Memory（记忆）

记住：

用户偏好
历史任务

## 4. Reflection（反思）

检查自己结果。


# Agent框架

如LangGraph、AutoGen、OpenManus、OpenClaw等，都是帮助你搭Agent的软件框架。

## 1.LangChain

最早的框架

### 定位：

LLM应用开发框架。

### 提供：

       LLM
        |
      Prompt
        |
      Retriever
        |
      Memory
        |
      Tool

组合。


## 2.LangGraph ⭐⭐⭐

重点关注

它可以解决复杂Agent流程。

LangChain 推出的 Agent 编排框架，解决 LangChain 原版难以实现循环、分支、多步骤复杂 Agent。
基于**图、DAG**，可以画带循环、状态持久化的工作流，现在工业界 Agent 首选框架之一。

## 名字含义：

Graph，图，字如其人，就是图的形式

### 例如：

          开始
            |
        判断问题
        /      \
     查资料    直接回答
       |
    总结
       |
      输出

这就是一个Graph。

## 实际它会用节点表示步骤：

Node1:
分析问题

Node2:
搜索

Node3:
总结

Edge:
决定下一步


## 3.AutoGen

微软出品，重点在于多Agent能力。

### 例如：

          老板Agent

              |
        ---------------
        |             |
      程序员Agent   测试Agent

不同Agent互相聊天。

## 4.OpenManus

开源 Agent 项目。

目标类似复刻 Manus AI。

强调自动执行任务。

## 5.OpenClaw（龙虾）

也是开源 Agent 框架。

方向重点是Agent的运行环境。

可以让Agent：调工具、执行动作、管理任务。

## 6.LlamaIndex

对标 LangChain，但是**最初定位优先做检索 (RAG)**。
LangChain：偏工作流、Agent；
LlamaIndex：擅长文档解析、索引构建、向量检索、RAG 流程；现在两者功能大量重叠，经常一起搭配使用。

## 7.DSPy

斯坦福开源框架。**Prompt 工程的升级版，不用手写提示词**。
传统：人手动写 Prompt；
DSPy：用代码定义任务目标，框架自动生成、优化提示词，也可以自动选择 Few‑shot 示例。适合复杂 LLM 任务，硅谷热门。

## 8.DeerFlow

国内开源 AI Agent 工作流编排框架，对标 LangGraph，国产方案。




# AgentHarness ⭐⭐⭐

这个词比较新。

Harness，字面意思是"安全带、框架"，在AI里面指：包裹Agent运行的控制层。

## 举个例子：

### 裸Agent：

LLM
 |
执行任务

问题：容易失控。

## Harness示意图：
        Agent Harness

      --------------------
              |
            Agent
              |
        ----------------
        |      |       |
        工具   记忆   日志
        控制   评估   重试

### 负责：

生命周期管理
权限控制
状态保存
错误恢复
评估

**企业级Agent一定需要**


# Agent Loop / ReAct ⭐⭐⭐

即Agent循环，也叫ReAct（Reason + Act），是经典Agent模式。
ReAct 就是一种最常见的 AgentLoop 范式。
循环：LLM 先思考需要做什么 → 调用工具行动 → 获取结果 → 继续思考。绝大多数 Agent 底层都是 ReAct。
它交替输出“思考（Reason）”和“行动（Act）”的文本，让AI的推理过程“可视化”，大大提高了复杂任务的成功率和可解释性。
每循环一次，Context 都在变化。

## 继续举个经典的例子：

      Observe
      观察
      ↓
      Think
      思考
      ↓
      Act
      行动
      ↓
      Observe
      观察结果
      ↓
      Think
      继续


# MCP（Model Context Protocol）⭐⭐⭐⭐

MCP，Model Context Protocol，即模型上下文协议

这个非常重要，2025开始大量出现，简单理解就是：AI时代的USB接口。

## 以前每个AI接工具（非常乱）：

      GPT
      |
      自己写数据库接口

      GPT
      |
      自己写搜索接口

      GPT
      |
      自己写文件接口

## MCP：

统一标准后：

                   LLM
                    |
                   MCP
        -------------------------
          |         |          |
        数据库    文件系统     搜索

MCP类似USB接口的出现，以前手机有苹果接口、安卓接口，各种不同，无法通用。
出现USB-C后，接口统一了，而MCP就是做到了让AI连接工具统一。
例如Claude通过MCP访问：本地文件/GitHub/数据库


# Tool Calling / Function Calling(工具调用)

Function Calling是OpenAI叫法，Tool Calling更广。与Tool Use含义解决。

## 以前：

AI：我不会计算

## 现在：

用户：
北京天气？

LLM：

      我要调用天气API
        ↓
      API返回
        ↓
      回答天气情况

## 流程：

     用户
      ↓
    LLM判断需要工具
      ↓
    生成函数参数
      ↓
    调用工具
      ↓
    结果返回LLM
      ↓
    生成答案


# Multi-Agent / Subagent(多智能体)

## Multi-Agent

即多个Agent合作，一般是系统预先设计多个Agent。

例如写论文的时候：

                总Agent
                  |
      ------------------------------
          |         |           |
      资料Agent  写作Agent   审稿Agent

## Subagent

即子Agent。
通常由主Agent动态创建。

例如：

主Agent：
帮我完成旅游规划

拆：
天气子Agent
酒店子Agent
路线子Agent


# Reflection workflow
反思工作流

是Agent 高级能力，完成一步任务之后，**回头复盘刚才输出有没有错，自我修正**，大幅降低幻觉。

属于 Agent 高级工作流。

举个例子：

      Agent生成代码

           ↓

      测试Agent检查

           ↓

       发现Bug

         ↓

        修改

         ↓

      重新测试

## Graph RAG

微软推出的 RAG 高级方案：**知识图谱 + 检索增强生成**
普通 RAG：文档切分→向量检索；
Graph‑RAG：先从文档抽取实体、关系构建知识图谱；查询的时候沿着图谱路径推理。适合需要多跳推理、复杂关联分析的场景。

## Workflow 编排 / 任务编排 / Graph/DAG 编排机制

- Workflow：一系列 LLM 步骤、工具调用组成的流水线工作流程
- DAG(Directed Acyclic Graph)：有向无环图。用来定义任务先后顺序、分支；LangGraph 底层就是 DAG。

例如：
某个毕业设计流程：

         数据采集
            |
         数据处理
            |
         模型预测
            |
         可视化

> DAG**不能循环**；Agent 循环任务则需要 DAG 之外额外加循环状态。
 

# AI Agent 产品

Manus AI：自动完成任务的Agent。
OpenManus：是Manus AI的开源复刻版本，来自MetaGPT团队，也是框架。

CoddingAgent（编码智能体），专门写代码的 AI Agent；例如 Devin















