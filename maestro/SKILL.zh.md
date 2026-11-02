---
name: maestro
description: Top-level orchestrator for the SkillStack 168-skill composable toolkit. When a task arrives, classify it into one of 9 themes (academic-research, style-integrity, ml-engineering, data-engineering, visualization, writing-citation, ai-text, ai-output-judgement, project-tooling) and point the agent at the correct skill folder and skill name. Themes are non-numbered so any can be dropped, swapped, or renamed without renumbering — removing a theme never breaks routing for the others. Use this FIRST whenever the agent needs to find a skill, before loading any individual skill.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  role: orchestrator
  skill_count: 168
  theme_count: 9
  repo_name: SkillStack
  language: zh
---

# Maestro — 技能编排器

## 目的

本技能是一个由 168 个可组合技能构成的库的前门，组织成 9 个独立的主题文件夹。各主题是独立模块——任意一个都可以被删除、替换或重命名，而堆栈的其余部分仍能正常工作。当收到一个任务时，不要猜测加载哪个技能，而是：

1. 阅读任务描述。
2. 将其匹配到下方 9 个主题中的**一个**。
3. 在该主题文件夹中，找到名称和描述最匹配的技能。
4. 加载该技能的 `SKILL.md` 并遵循它。

## 仓库布局

```
skillstack/
├── maestro/SKILL.md                          ← 你在这里
├── README.md                                 ← 主索引（全部 168 个技能）
├── academic-research/    (20 个技能)         ← 研究规划与写作
├── style-integrity/      (18 个技能)         ← LaTeX、正文、编码规范
├── ml-engineering/        (22 个技能)         ← PyTorch、训练、验证
├── data-engineering/      (18 个技能)         ← ETL、模式、血缘
├── visualization/         (18 个技能)         ← 图表、TikZ、海报
├── writing-citation/      (18 个技能)         ← BibTeX、引用、编辑
├── ai-text/               (15 个技能)         ← 检测并拟人化 AI 文本
├── ai-output-judgement/   (18 个技能)         ← 评判并验证 AI 输出
└── project-tooling/       (20 个技能)         ← 打包、Docker、CI/CD
```

每个主题子文件夹为每个技能包含一个文件夹，每个技能文件夹内有一个 `SKILL.md`（部分还包含一个 `references/` 子文件夹，带有更深的规则）。

## 主题路由表

| 主题文件夹 | 当任务涉及...时使用 | # 技能数 |
|---|---|---|
| `academic-research/` | 规划研究、起草稿件、撰写学位论文、设计资助申请、评审论文、准备演讲 | 20 |
| `style-integrity/` | 执行 LaTeX/正文/编码风格规则、零捏造检查、标记一致性、以纪律执行任何多步骤任务 | 18 |
| `ml-engineering/` | 在 PyTorch/Lightning/HuggingFace 中构建、训练、调优、解释或验证 ML 模型 | 22 |
| `data-engineering/` | ETL、数据质量、模式执行、特征存储、数据集卡片、转换器 | 18 |
| `visualization/` | 出版级图表、TikZ 图、海报、表格、仪表盘、绘图 | 18 |
| `writing-citation/` | BibTeX、引用、摘要、IMRaD、方法学、英文编辑、改写 | 18 |
| `ai-text/` | 检测 AI 生成的文本、拟人化 AI 文本、困惑度/突发性、水印检测 | 15 |
| `ai-output-judgement/` | 评判 AI 输出的事实性、幻觉、偏差、安全性、扎根度、忠实度、对齐、代码正确性，构建评估框架 | 18 |
| `project-tooling/` | 打包、Docker、CI/CD、pytest、文档、README、pyproject.toml、Makefile | 20 |

## 如何路由

### 第 1 步 — 分类任务

阅读用户请求并选择恰好一个主主题。如果任务跨两个主题（例如"写一篇论文并生成其图表"），先路由到**主**主题，再链到第二个。

### 第 2 步 — 选择技能

在主题文件夹内，扫描技能名称。每个 `SKILL.md` 以 YAML `description` 字段开头，说明何时使用它。将任务匹配到最接近的描述。

### 第 3 步 — 加载并遵循

打开选定的 `SKILL.md`，完整阅读并遵循其工作流程。如果它引用 `references/` 子文件，则在行动前也阅读该文件。

### 第 4 步 — 必要时链式调用

如果任务自然链式调用（例如 `research-ideation-planner` → `research-repo-builder` → `modular-ml-architect`），则在加载下一个前先完成第一个技能的输出。

## 常见路由示例

| 用户说 | 主题 | 技能 |
|---|---|---|
| "为一本医学影像期刊提出 3 个研究想法" | academic-research | research-ideation-planner |
| "用 src/、configs、手册搭建一个研究仓库" | academic-research | research-repo-builder |
| "用 LaTeX 起草方法章节" | academic-research | journal-manuscript-writer |
| "在我的 Python 中执行 2 空格缩进、CamelCase、句末注释" | style-integrity | coding-conventions-enforcer |
| "检查我的 LaTeX 是否缺少 `% ====== %` 分隔符" | style-integrity | latex-style-guard |
| "验证我参考文献中的每个 DOI 都是真实的" | style-integrity | zero-fabrication-guard |
| "运行多随机种子的训练循环并在每个 nn.Module 上调用 .to(device)" | ml-engineering | reproducible-experiment-runner |
| "用 Optuna TPE 进行贝叶斯超参搜索" | ml-engineering | hyperparameter-tuner |
| "生成 SHAP 摘要 + 依赖图" | ml-engineering | model-explainer |
| "构建一个幂等转换并带审计追踪的 ETL" | data-engineering | etl-pipeline-builder |
| "用 pandera 模式验证我的 CSV" | data-engineering | data-quality-validator |
| "制作期刊级 300 DPI matplotlib 图表" | visualization | publication-figure-maker |
| "绘制带有实心分组线的 TikZ 流水线图" | visualization | tikz-framework-diagrammer |
| "把我的 .bib 转为 IEEE 引用风格" | writing-citation | citation-style-converter |
| "检查每个 bibitem 至少被 \cite 一次" | writing-citation | bibtex-citation-manager |
| "检测这篇文章是否为 AI 生成" | ai-text | ai-text-detector |
| "拟人化这段 AI 文本但保留所有事实" | ai-text | ai-text-humanizer |
| "检查此 LLM 响应是否含有幻觉事实" | ai-output-judgement | hallucination-detector |
| "验证这段 AI 生成段落中的事实声明" | ai-output-judgement | factuality-checker |
| "检查我的 RAG 输出是否扎根于检索到的文档" | ai-output-judgement | groundedness-verifier |
| "审计我的 LLM 输出的性别/种族偏差" | ai-output-judgement | bias-auditor |
| "构建带 MMLU + GSM8K 的 LLM 评估框架" | ai-output-judgement | evaluation-harness-builder |
| "用 LLM-as-judge 给这些聊天机器人响应打分" | ai-output-judgement | llm-as-judge-evaluator |
| "在检索到的网页中检测提示注入" | ai-output-judgement | prompt-injection-detector |
| "验证这段 AI 生成的 Python 代码能运行并通过测试" | ai-output-judgement | code-output-validator |
| "把我的仓库打包成 zip，排除 results/ 和 .git/" | project-tooling | project-zip-packager |
| "为可复现研究编写 Dockerfile" | project-tooling | docker-research-container |
| "为我的 Python 包生成 README.md" | project-tooling | readme-generator |

## 编码规范技能（特别说明）

用户仓库执行严格的非标准 Python 风格。每当在本仓库中编写或编辑 Python 代码时，**首先**加载 `style-integrity/coding-conventions-enforcer/SKILL.md`。五条规则：

1. **变量**使用 `camelCase`（例如 `dataSourceUrl`）。
2. **函数、类、文件名、字典键**使用 `CamelCase`（例如 `ProcessData`、`DataProcessor`、`VisualizationUtils.py`、`"ValidationStatus"`）。
3. **`if` 语句**始终将条件用括号包裹：`if (condition):`。
4. **注释**位于每条语句上方并以句点结尾：`# Initialize the data source URL.`。
5. **字符串**在 docstring 之外的所有地方使用双引号 `""`。

框架强制的小写方法名（`forward`、`backward`、`training_step`、`validation_step`、`configure_optimizers`、`setUp`、`tearDown`）豁免。

## 冲突解决

如果似乎有两个技能都适用：
- 优先选择**更具体**的技能。
- 优先选择与任务**主要输出**（用户最终想要的文件或产物）所属主题匹配的技能。
- 当仍不确定时，请用户确认其想要产生哪种产物。

## 何时不使用 Maestro

- 简单问答或单文件读取（直接回答）。
- 已由本仓库之外的技能覆盖的任务（例如内置的 `docx`、`pdf`、`xlsx`、`charts` 技能）。
- 仅需网络研究而无需调用技能的任务。

## 更新本文件

如果你向任何主题添加新技能，请更新上述路由表中该主题的计数以及 `README.md`。保持两个文件同步。

主题故意不编号——你可以删除或重命名任何主题文件夹而无需对其余重新编号。maestro 按文件夹名称而非序数路由。
