---
name: factuality-checker
description: Verify factual claims in AI outputs by atomizing the text, retrieving evidence from trusted sources (Wikipedia API, Crossref, web search), and labeling each claim SUPPORTED, REFUTED, or UNVERIFIABLE. Use when an LLM response, summary, or long-form answer makes factual assertions that must be checked before release.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: ai-output-judgement
tags: [factuality, llm, verification, factscore]
related: [ai-output-judgement/hallucination-detector, ai-output-judgement/reference-accuracy-checker, ai-output-judgement/numeric-accuracy-verifier, style-integrity/zero-fabrication-guard]
prerequisites: []
outputs: [markdown, json]
difficulty: advanced
estimated_tokens: 2200
cost_warning: "Optional: web search API calls may incur costs."
permissions:
  read_files: true
  write_files: false
  network: true
  execute_code: false
language: zh
---

# 事实性检查器

## 何时使用
- 一段长篇 LLM 回答、简报或文章摘要包含将被发布或引用的事实性断言。
- 评审者要求声明级别的证据，而非一句"看起来合理"的判断。
- 触发关键词："事实核查"、"验证声明"、"这是真的吗"、"有来源支持"、"原子化声明"、"FActScore"。
- 一个 RAG 答案将检索到的事实与模型内部知识混合，你需要将两者分离。

## 工作流程
1. 归一化 AI 输出：去除 markdown 杂质，按句切分，保留 span 映射供后续高亮。
2. 原子化：将每个句子拆分为原子声明（每条一个可验证命题）。使用提示词模板如 "Decompose the following text into self-contained factual claims. One fact per line. No compound clauses."
3. 对每个原子声明检索证据。默认顺序：(a) Wikipedia REST API（`https://en.wikipedia.org/w/api.php` action=query），(b) Wikidata 查询实体事实，(c) Crossref 查询引用，(d) 经审核的搜索 API 进行通用网络搜索。引用检索到的段落并记录其 URL。
4. 用一次验证器判别每条声明：使用 NLI 模型（`microsoft/deberta-v3-large-mnli`）加上返回标签与一句理由的 LLM 裁判提示，将声明与证据进行比对。
5. 为每条声明打标签：`SUPPORTED`（证据蕴含它）、`REFUTED`（证据与之矛盾）或 `UNVERIFIABLE`（top-k 结果中未找到决定性证据）。
6. 计算事实性得分 = (#SUPPORTED) / (#SUPPORTED + #REFUTED + #UNVERIFIABLE)，以及严格的 FActScore = SUPPORTED / 总数。
7. 输出声明级别的表格，包含 span、标签、证据 URL 和理由，外加一份全局摘要。

## 输入
- AI 输出文本（必需）。
- 可选：可信来源白名单（如 PubMed、Statista、政府域名）。
- 可选：黄金声明或种子语料库以短路检索。
- 可选：top-k 证据的 k 值与 NLI 蕴含阈值（默认 0.7）。

## 输出
- `claims.jsonl` —— 每个原子声明一行：`id`、`text`、`span`、`label`、`evidence_url`、`rationale`。
- `factuality_report.md` —— 表格加 FActScore、未支持百分比以及最成问题的声明。
- 带高亮的 HTML/markdown 输出，SUPPORTED（绿色）、REFUTED（红色）、UNVERIFIABLE（黄色）。

## 核心规则
- 绝不在没有检索到的证据 URL 的情况下将声明标为 SUPPORTED；"模型知道它"不算验证。
- 仅当检索到的证据直接与之矛盾时，声明才为 REFUTED —— 缺少证据是 UNVERIFIABLE，而非 REFUTED。
- 原子声明不得包含代词；在检索前将引用解析为实体。
- 为每条标签记录检索来源，以便人工审计追溯链路。
- 当一个句子包含两条事实时，将其拆分；不要为复合陈述打标签。
- 在原子化过程中不要撰写新事实 —— 只重述输出所述内容。

## 示例

```text
AI output: "Marie Curie won the Nobel Prize in Physics in 1903 and again in Chemistry in 1911.
She was the first person to win two Nobel Prizes."

Atomized claims:
  C1: Marie Curie won the Nobel Prize in Physics in 1903.
  C2: Marie Curie won the Nobel Prize in Chemistry in 1911.
  C3: Marie Curie was the first person to win two Nobel Prizes.

Verdicts:
  C1 SUPPORTED — https://en.wikipedia.org/wiki/Marie_Curie (NLI entailment 0.96)
  C2 SUPPORTED — https://www.nobelprize.org/prizes/chemistry/1911/marie-curie/
  C3 SUPPORTED — Nobel Prize official biography confirms she was first.

FActScore: 1.00 (3/3 supported)
```

```text
AI output: "The Eiffel Tower was completed in 1889 for the World's Fair in London."
C1: The Eiffel Tower was completed in 1889.            -> SUPPORTED
C2: The Eiffel Tower was built for a World's Fair.      -> SUPPORTED (1889 Exposition Universelle)
C3: That World's Fair was held in London.               -> REFUTED (it was in Paris)
FActScore: 0.67; the London claim is refuted by evidence.
```

## 常见陷阱
- 将"未找到证据"当作 REFUTED —— 应为 UNVERIFIABLE；缺少证据不等于矛盾。
- 使用模型自身的参数化知识作为证据 —— 只有可引用的检索来源才算。
- 未能对复合声明进行原子化 —— 用"and"连接的句子通常隐藏了两条独立事实。
- 对敏感声明仅依赖单一检索来源 —— 要求来自第二个独立来源的佐证。
- 让验证器 LLM 在原子化过程中撰写新事实 —— 只重述输出所述内容。

## 参考资料
- Min, S. et al. (2023). "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation." EMNLP. https://arxiv.org/abs/2305.14251
- Wei, J. et al. (2024). "Long-form factuality in large language models." Google DeepMind — SAFE (Search Augmented Factuality Evaluator). https://arxiv.org/abs/2403.18802
- Wikipedia REST API: https://en.wikipedia.org/api/rest_v1/
- Crossref REST API: https://api.crossref.org/works
- 伴随技能：`hallucination-detector`、`groundedness-verifier`、`reference-accuracy-checker`。
