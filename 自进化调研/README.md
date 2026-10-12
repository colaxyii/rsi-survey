# 自进化调研

> 公开分享范围：仅本文件夹。只做论文 / 学习类知识分享，不含工作内容。

## 主线

三篇论文构成一条清晰的技术演进线，主题是**「不更新权重，靠改上下文让模型自己变强」**。

```
TextGrad (2024/2025 Nature)     把 text 当梯度反向传播  →  优化"组件"
        ↓  从"传播"改为"进化"
GEPA (2025/2026 ICLR Oral)      反思式提示词进化 + Pareto  →  优化"提示词"
        ↓  从"优化提示词"改为"优化整个上下文"
ACE (2025/2026 ICLR)            上下文当 playbook 增量生长  →  优化"上下文"
```

一句话概括三者关系：

- **TextGrad** 回答「怎么把自然语言反馈变成可优化的信号」→ 提出 textual gradient
- **GEPA** 回答「反馈怎么用得更省样本」→ 反思 + 进化搜索取代梯度传播
- **ACE** 回答「优化的对象除了提示词还能是什么」→ 把上下文本身当可进化对象，且**拒绝压缩**

## 核心对照：各自"自进化"了什么

| | TextGrad | GEPA | ACE |
|---|---|---|---|
| **年份 / 出处** | 2024 arXiv / 2025 Nature | 2025 arXiv / 2026 ICLR Oral | 2025 arXiv / 2026 ICLR |
| **优化对象** | 计算图中的任意变量（prompt、代码、分子结构） | 复合系统的提示词集合 | 上下文 / playbook（system prompt + memory） |
| **反馈形式** | textual gradient（文本梯度） | natural language reflection | insight + delta 条目 |
| **更新机制** | 反向传播（沿计算图） | 反思式变异 + 交叉 + Pareto 选择 | Generator-Reflector-Curator 三角色 + 增量 delta |
| **类比** | 反向传播 / 自动微分 | 遗传算法 + 自然选择 | 人类学习：试错-反思-固化 |
| **关键词** | metaphor of gradients | sample efficiency | anti-compression |
| **一句话** | 把 text 当梯度传播 | 把传播换成进化 | 把进化对象换成整个上下文 |

## 为什么这个顺序适合入门

用户给的判断是对的，补几点理由：

**1. TextGrad 是概念地基。** 它提出的核心洞见是——自然语言批评可以像梯度一样"指明参数该往哪调"。理解了这一点，后面两篇都是在换实现方式。

**2. GEPA 是范式转折点。** 它明确反对 RL 的样本低效（GRPO 要上万次 rollout），主张语言本身是更丰富的学习媒介。而且它的框架概括力很强：**大部分 self-evolution 论文都能抽象成 "GEPA-like 反思式文本优化 + 某个具体优化目标"**。

**3. ACE 是当代前沿，且明确与 GEPA 对话。** ACE 论文里直接点名 GEPA 的"简洁偏好"（brevity bias）是缺陷，并用"上下文坍缩"（context collapse）作为反面案例——一个真实的失败数据：上下文 18282 tokens 时准确率 66.7，下一步被 LLM 重写压到 122 tokens，准确率掉到 57.1，**比不做适配的 63.7 还差**。

这个数据点是整条线里最有分享价值的素材：**"让 AI 总结自己的经验，结果越总结越笨"**。

## 文件

- [papers/TextGrad-2025-Nature.pdf](papers/TextGrad-2025-Nature.pdf) — Optimizing generative AI by backpropagating language model feedback, Nature 2025-03-19, DOI [10.1038/s41586-025-08661-4](https://doi.org/10.1038/s41586-025-08661-4)
- [papers/GEPA-2026-ICLR.pdf](papers/GEPA-2026-ICLR.pdf) — GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning, ICLR 2026 Oral, [arXiv:2507.19457](https://arxiv.org/abs/2507.19457)
- [papers/ACE-2026-ICLR.pdf](papers/ACE-2026-ICLR.pdf) — Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models, ICLR 2026, [arXiv:2510.04618](https://arxiv.org/abs/2510.04618)

## 待办

- [ ] 逐篇精读，按 `90-templates/paper.md` 格式补笔记
- [ ] 三篇读完，写主题综述：文本优化路线的三次转向
- [ ] 挑小红书选题（建议从"上下文坍缩"这个反直觉点切入）
