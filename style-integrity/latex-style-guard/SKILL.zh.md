---
name: latex-style-guard
description: Enforce strict LaTeX typography and structural formatting rules on manuscripts before submission. Use when editing .tex files, reviewing equations, figures, tables, algorithms, or normalizing quote styles and float placements for camera-ready papers.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: style-integrity
tags: [latex, typography, manuscript, formatting, camera-ready]
related: [style-integrity/cross-reference-validator, style-integrity/notation-consistency-checker, academic-research/journal-manuscript-writer]
prerequisites: []
outputs: [latex, markdown]
difficulty: advanced
estimated_tokens: 880
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: zh
---

# LaTeX 风格守卫

## 何时使用
- 用户提交 `.tex` 文件并要求"格式清理"、"风格检查"或"camera-ready 准备"。
- 稿件在浮动体、公式或章节命令周围的空行不一致。
- 行内引号显示为直引号 `"text"` 或 `"text"`，而非 LaTeX 风格的 ``text''。
- 正文使用 `\subsubsection{}` 而非行内粗体标题。
- 公式或浮动体缺少分隔注释行。

## 工作流程
1. 在编辑前从头到尾通读整个 `.tex` 源文件。
2. 验证每个 `\section{}` 和 `\subsection{}` 命令之后恰有一行空行。
3. 确认每个浮动环境：`table`、`figure`、`algorithm` 及任何 `equation`/`align` 块前后各恰有一行空行。
4. 在每个公式、表格、图、算法块之前和之后立即在其自身行上插入 `% ====================== %` 分隔行。**不要**在 `\section{}` 命令周围添加分隔符。
5. 将所有双引号替换为 `` `` `` 开与 `''` 闭，单引号替换为 `` ` `` 开与 `'` 闭。
6. 审计 `\textbf{}` 的使用：仅保留用于结构层级（类似章节的强调）。删除行内正文中的装饰性加粗。
7. 删除每个 `\textit{}` 出现。若强调必不可少，则改写句子。
8. 将每个 `\subsubsection{Title}` 替换为在下一段开头行内呈现的 `\textbf{Title.}`。
9. 将标点移出 `\ref{}` 和 `\cite{}` 的右花括号：写 `Figure~\ref{fig:x}.` 而非 `Figure~\ref{fig:x.}`。
10. 在导言区重新定义默认浮动体位置：
    ```latex
    \makeatletter
    \renewcommand{\fps@figure}{!htb}
    \renewcommand{\fps@table}{!htb}
    \makeatother
    ```
11. 重新阅读修补后的文件以确认所有规则一致成立。
12. 报告应用的每种变换的数量。

## 输入
- 一个或多个 `.tex` 文件的路径（通过 `\input{}`/`\include{}` 的单文件或多文件项目）。
- 若有目标期刊风格指南（在冲突时覆盖默认值）。
- 用户希望保留的任何现有导言宏。

## 输出
- 应用了所有规则的已修改 `.tex` 文件。
- 简短的汇总表：规则名称、找到的次数、修复的次数。

## 核心规则
- 每个 `\section{}` 和 `\subsection{}` 之后恰有一行空行。
- 每个浮动体/公式环境前后各恰有一行空行。
- `% ====================== %` 分隔符**仅**包裹公式、表格、图、算法，从不包裹章节命令。
- 双引号用 `` ``text'' ``，单引号用 `` `text' ``。禁止直引号。
- `\textbf{}` 保留用于结构层级；`\textit{}` 完全禁止。
- 禁止 `\subsubsection{}`。改用行内 `\textbf{Inline Heading.}`。
- 标点位于 `\ref{}`、`\cite{}`、`\eqref{}` 的右花括号**之外**。
- 浮动体位置通过 `\fps@...` 重定义默认为 `[!htb]`，而非逐个浮动体覆盖。

## 示例

之前：
```latex
\subsection{Method}
We define the loss as:
\begin{equation}
L = (y - \hat{y})^2
\end{equation}
The "standard" approach is shown in Figure~\ref{fig:x.}.
```

之后：
```latex
\subsection{Method}

We define the loss as:

% ====================== %
\begin{equation}
L = (y - \hat{y})^2
\end{equation}
% ====================== %

The ``standard'' approach is shown in Figure~\ref{fig:x}.
```

## 参考资料
- Leslie Lamport，《LaTeX: A Document Preparation System》（第 2 版）。
- TeX FAQ 关于浮动体位置：https://texfaq.org/FAQ-floats
- `amsmath` 用户指南（AMS）关于公式环境。
