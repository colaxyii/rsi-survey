# RSI合成数据

> 主题：让系统自己生产训练信号。产出物有三类——**训练数据、任务与环境、验证信号**。

## 一句话

RSI 合成数据的判据不是"像不像人写的"，而是**闭环性**：生成数据的东西和被改进的东西必须是同一个系统。2026 年这一支两条主线——**从"依赖验证器"转向"没有验证器怎么办"**，以及**从造样本转向造环境**。

## 口径与规模

- 16 组合成数据专项检索式，arXiv 2026 年命中 1328 篇
- 与 RSI 语义（self-improve / self-evolve / self-play / zero-data / data-centric）交叉后 **87 篇**
- 关键词分布：`synthetic data` 240 ｜ `zero-data / data-free` 209 ｜ `data synthesis` 143 ｜ `model collapse` 91 ｜ `verifier` 87 ｜ `self-play` 81
- 与 ICLR 2026 RSI Workshop 的接收论文高度重叠（Agent0、Language Self-Play、Escaping Model Collapse via Synthetic Data Verification、Your Self-Play Algorithm is Secretly an Adversarial Imitator、ESDAE、Verifying the Verifiers 等）

## 六条主线

### 1. 零数据自博弈（今年最活跃）

**要解决的问题**：没有人类数据时怎么起步；开放域里没有验证器，自博弈会退化成奖励欺骗。

```
有验证器（代码/数学）          已有成熟闭环
        ↓  去掉验证器是 2026 年的关键一跃
内在奖励（G-Zero 的 Hint-δ）   用"看到提示 vs 没看到提示"的预测位移当奖励
        ↓  结构补齐
三方自演化（J-Zero）           Challenger–Solver–Judge 统一框架
        ↓  推到最前端
预训练自博弈（Self-Play Pretraining）  训练数据由模型生成，上限从人类知识变成算力
```

- [Self-Play Pretraining with Zero Data](https://arxiv.org/abs/2609.30063)（2609.30063）— 让模型学会生成"最有利于自己改进"的数据，训练数据从"被人精选"变为"被模型生成"
- [G-Zero](https://arxiv.org/abs/2605.09959)（2605.09959）— **免验证器**，Hint-δ 内在奖励量化生成器在有/无提示下的预测分布位移，绕开 LLM judge 的能力瓶颈与 reward hacking
- [J-Zero](https://arxiv.org/abs/2608.26582)（2608.26582）— Challenger–Solver–Judge 三方统一自演化，专攻不可验证域
- [π-Play](https://arxiv.org/abs/2604.14054)（2604.14054）— 特权自蒸馏，解决自博弈稀疏奖励与弱信用分配
- 同族：[Tool-R0](https://arxiv.org/abs/2602.21320)（工具学习从零起步）、[MM-Zero](https://arxiv.org/abs/2603.09206)（推到视觉语言模型）、[SCOPE](https://arxiv.org/abs/2605.31433)、[CPMobius](https://arxiv.org/abs/2602.02979)、[Self-Generative Adversarial Fine-Tuning](https://arxiv.org/abs/2602.01137)

**关键点**：这一步决定 RSI 能不能走出代码和数学。

### 2. 任务与环境合成：从"造样本"到"造环境"

**要解决的问题**：固定的 mutation / bug injection 造出来的合成任务分布僵化、与被训模型能力脱节、难度不随能力增长，很快被训穿。

- [Learning to Build the Environment](https://arxiv.org/abs/2605.14392)（2605.14392）— 最清晰的一次范式重述：模型不是生成问题或轨迹去模仿，而是**构建训练自己的环境**，产物是可复用的可执行对象
- [SynCo](https://arxiv.org/abs/2610.11345)（2610.11345，10-08 最新）— 静态数据集和"单独更新的合成模型"都会让任务随能力变化而过时，主张数据合成与被训模型**协同训练**
- [Recursive Harness Self-Improvement for Frontier Reasoning Data Synthesis](https://arxiv.org/abs/2610.03548)（2610.03548）— 提出**任务–harness 共演化**，把 solver 失败在线转成对 harness 的修改
- [VISA](https://arxiv.org/abs/2608.26013)（2608.26013）— 批评一次性 generate-and-filter 丢弃失败样本与 verifier 结果
- [Socratic-SWE](https://arxiv.org/abs/2606.07412)（2606.07412）— 从真实 agent 轨迹反推 SWE 任务，让合成分布来源于真实失败
- [QUEST](https://arxiv.org/abs/2605.24218)（全合成任务训 deep research agent）、[GSAR](https://arxiv.org/abs/2608.22847)（GUI agent 自演化数据合成）、[Question Begets Question](https://arxiv.org/abs/2608.01522)（自演化课程）

**关键点**：环境难度必须与被训练者一起演化，这也是合成数据与课程学习合流之处。

### 3. 造数据的流程自己递归改进

最贴近 RSI 原义的一支，今年才明确出现：既有的"任务级递归"只是把生成的问题当种子，**构造 harness 本身不变**；新工作把失败信号直接用于修改 harness。代表作见上方 2610.03548。

### 4. 数据为中心的 RSI 基准

回答"怎么知道数据策略真的有效"。

- [RSIBench-Data](https://arxiv.org/abs/2607.25886)（2607.25886）— 把数据为中心的后训练研究拆成"诊断能力缺口 → 设计并验证数据策略 → 从 checkpoint 反馈学习"，并刻意把这些研究决策与训练/服务/评测解耦
- [AutoDataBench](https://arxiv.org/abs/2609.35025)（2609.35025）— 直接问：**agent 能不能写出喂给自我改进循环的数据**？现有产线仍依赖专家人力，自动化才能让数据生产随算力扩张
- [Gödel Forest](https://arxiv.org/abs/2609.36675)（2609.36675）— 点出根本两难：验证数据策略需要昂贵的模型训练，所以只能在搜索深度与广度之间取舍
- workshop 侧：PostTrainBench（agent 能否自动化 LLM 后训练）、ESDAE（给 agent 评测用的合成数据本身也要被评估）

### 5. 验证信号合成（真正的瓶颈）

几乎所有摘要最后都指向同一件事：**瓶颈不是生成，是验证**。

- [Self-Trained Verification](https://arxiv.org/abs/2605.30290)（2605.30290）— 明确点出训练时自训练、测试时"验证–精炼"循环都卡在 verifier 上，且 V-R 循环会**验证器分数膨胀、准确率停滞**
- [Self-Play Search Distillation](https://arxiv.org/abs/2609.30936)（2609.30936）— 生成"超人类合成数据"以暴露困难决策点与竞争性选项
- 形式化路线最成熟：[Formal Disco](https://arxiv.org/abs/2607.04631)（大规模生成形式验证程序）、[Semantic Equivalence Self-Play](https://arxiv.org/abs/2604.17010)（用 Liquid Haskell 证明引导对抗训练）
- workshop：《Your Self-Play Algorithm is Secretly an Adversarial Imitator》（把自博弈翻译成模仿学习）、《Verifying the Verifiers》（验证器本身的失败归因）

### 6. 风险：崩塌、污染与"数据不属于你"

- [Better, Faster](https://arxiv.org/abs/2605.24998)（2605.24998）— 自生成推理轨迹在复杂推理上会**导致 model collapse**
- [Learning from Synthetic Data without Model Collapse](https://arxiv.org/abs/2607.17043)（2607.17043）— 目标转换：不是"限制退化"，而是"保证每一代都比上一代强"
- [Model Collapse as Cultural Evolution](https://arxiv.org/abs/2605.23054)（2605.23054）— 用文化演化的迭代学习理论解释**哪些语言结构先退化、按什么顺序、为什么**，给出五个可证伪预测
- [Not All Synthetic Data Is Yours to Learn From](https://arxiv.org/abs/2605.31126)（2605.31126）— **最值得记的结论**：能否从自身采样文本中获益，是 source–student 配对的**关系属性**，不是数据的固有属性（latent capability resurfacing）
- [SynthSentry](https://arxiv.org/abs/2609.12353)（2609.12353）— 训练前的语料级污染筛查，因为事后诊断崩塌没有意义

## 四条共识

1. **可验证域与不可验证域是真正的分水岭。** 代码/数学/形式证明的闭环已跑通，开放域刚起步，且必须靠内在奖励或 judge。
2. **质量判据是"与当前学生模型的匹配度"，不是"像不像人写的"。** 同一批合成数据对 A 模型是营养、对 B 模型是毒药。
3. **生成器必须与被改进者共同演化。** 静态数据、静态合成器、落后一代的 judge 都会被训穿。
4. **验证才是瓶颈。** 生成端已便宜到可以无限产，缺的是可信筛选信号，于是要么 verifier 分数膨胀，要么退回可机检域。

## 五个未解问题

1. **无验证器的内在奖励缺理论保证。** Hint-δ 这类"预测位移"奖励很聪明，但没人证明它不会把人往错误方向推——只是把 reward hacking 转移了形式。
2. **崩塌的机制刚有假设，没有可操作处方。** 文化演化解释、分布尾部退化都是诊断；"每代都进步"还是目标而非方法。
3. **合成数据的溯源与产权。** 语料混没混、混了多少、来自哪个模型，目前只能靠判别器，而判别器会被下一代生成器绕过。
4. **数据策略的验证成本。** Gödel Forest 的两难是真问题：验证数据策略就要训练模型，而训练正是要省掉的东西。
5. **评测自身的合法性。** 用合成任务评 agent，考的是能力还是合成器的偏置？

## 只读 8 篇

| 顺序 | 论文 | 为什么读 |
|---|---|---|
| 1 | [G-Zero 2605.09959](https://arxiv.org/abs/2605.09959) | 免验证器自博弈的关键一跃 |
| 2 | [Self-Play Pretraining 2609.30063](https://arxiv.org/abs/2609.30063) | 把自博弈推到预训练 |
| 3 | [Learning to Build the Environment 2605.14392](https://arxiv.org/abs/2605.14392) | 从造样本到造环境的范式转向 |
| 4 | [Recursive Harness Self-Improvement 2610.03548](https://arxiv.org/abs/2610.03548) | 生成流程自身的 RSI |
| 5 | [AutoDataBench 2609.35025](https://arxiv.org/abs/2609.35025) | 数据自动化基准 |
| 6 | [Not All Synthetic Data Is Yours 2605.31126](https://arxiv.org/abs/2605.31126) | 合成数据的价值是关系属性 |
| 7 | [Model Collapse as Cultural Evolution 2605.23054](https://arxiv.org/abs/2605.23054) | 崩塌的机制解释 |
| 8 | [Self-Trained Verification 2605.30290](https://arxiv.org/abs/2605.30290) | 瓶颈定位在 verifier |

## 文件

- [论文索引.md](论文索引.md) — 87 篇按主线分组的清单
- [data/rsi_synthetic_data_2026.csv](data/rsi_synthetic_data_2026.csv) — 原始数据（日期、arXiv ID、主分类、标题、一作、子方向、链接）

## 相关

- [[自进化调研/README|自进化调研]] — RSI 全景与八个方向
- [[推荐记忆机制/推荐记忆机制调研|推荐记忆机制]]

合成数据与记忆本质上是同一个写入决策的两个场景：**"这条自己产出的东西，该不该被固化进系统"**。合成数据侧卡在验证信号，记忆侧卡在写入门控与信任标定，根子是同一个——缺少一个不依赖人工、又不容易被自己欺骗的判据。

## 待办

- [ ] 精读八篇入口，按 `90-templates/paper.md` 格式补卡片
- [ ] 深挖一支：零数据自博弈（G-Zero / J-Zero / Self-Play Pretraining）或 model collapse
- [ ] 把「验证信号」这一支与记忆侧的写入门控（GRASP / ORC / Prediction Is Not Memory）对齐成一张机制表
- [ ] 小红书选题：从「模型自己出题自己学，为什么越学越笨」切入
