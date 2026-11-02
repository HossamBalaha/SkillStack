---
name: journal-manuscript-writer
description: 'Draft publication-ready journal sections in LaTeX with strict structural style: only \section and \subsection (no \subsubsection), separator comments around floats, IEEE citation style, and mandatory back-matter sections. Use when the user asks to write, format, or polish a journal article draft for IEEE, Elsevier, or comparable venues.'
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: academic-research
tags: [latex, manuscript, journal, imrad, writing]
related: [style-integrity/latex-style-guard, academic-research/related-work-surveyor, academic-research/supplementary-materials-organizer]
prerequisites: [style-integrity/latex-style-guard]
outputs: [latex]
difficulty: advanced
estimated_tokens: 2200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: ar
---

# كاتب مخطوطة المجلة

## متى تستخدم

- يطلب المستخدم "كتابة المخطوطة" أو "صياغة القسم 3" أو "تنسيق ورقتي بـ LaTeX".
- الهدف مجلّة (IEEE TPAMI، Medical Image Analysis، Nature Scientific Reports، Elsevier).
- يحتاج المستخدم متناً خلفيّاً إلزاميّاً (CRediT، التمويل، IRB، توفّر البيانات، تعارضات، اختصارات).
- كلمات مفتاحيّة مُحفِّزة: مخطوطة، مسوّدة LaTeX، IEEEtran، elsevier، المتن الخلفيّ، كلمات مفتاحيّة، استشهادات.

## سير العمل

1. أكّد المكان المستهدف وفئة المستند (مثل `IEEEtran`، `elsarticle`) ونمط المراجع (مثل `IEEEtran`، `elsarticle-num`).
2. صُغ الملخّص (150-250 كلمة). ألحق 4-6 كلمات مفتاحيّة بعد الملخّص بالتنسيق الذي يطلبه المكان.
3. ضع مخطّطاً للمقدمة، الأعمال ذات الصلة، المنهجيّة، التجارب، المناقشة، الخاتمة.
4. اكتب كلّ قسم باستخدام `\section{}` و`\subsection{}` فقط. لا تستخدم `\subsubsection` أبداً.
5. أدخل سطراً فارغاً بعد كلّ أمر `\section` و`\subsection`.
6. لُفّ كلّ عنصر طافٍ أو معادلة أو جدول أو شكل أو خوارزميّة بأسطر فاصلة `% ====================== %`.
7. استخدم نمط اقتباس LaTeX: ``مزدوج'' و`مفرد'. لا تستخدم الاقتباسات المستقيمة أبداً.
8. قيِّد `\textbf{}` على التسلسل الهرميّ الهيكليّ (رؤوس الأقسام، رؤوس أعمدة الجداول). لا تستخدم `\textit{}` أبداً؛ تحوّل
   إلى `\emph{}` فقط عندما يتطلّب المعنى التوكيد.
9. استشهد باستخدام `\cite{}` (نمط IEEE المرقّم). جمّع الاستشهادات المتعدّدة كـ `\cite{a, b, c}` مرتّبة تصاعديّاً.
10. ألحق المتن الخلفيّ الإلزاميّ: مساهمات المؤلّفين وفق CRediT، التمويل، موافقة IRB/الأخلاقيّات، الموافقة المستنيرة،
    توفّر البيانات، تعارضات المصالح، الاختصارات.
11. تحقّق ذهنياً من الترجمة: كلّ `\label{}` له `\ref{}` أو `\eqref{}` مطابق.
12. نفّذ مروراً أخيراً للأقسام الفرعيّة اليتيمة (لا `\subsection` بدون `\section` محيط).

## المُدخلات

- المكان المستهدف وفئة المستند.
- خطة المشروع / الملخّص التنفيذيّ من خطوة التأمّل.
- الأشكال والجداول والمعادلات (كمصدر LaTeX أو أوصاف).
- ملفّ المراجع (`refs.bib`) أو قائمة DOI للتنسيق.
- قائمة المؤلّفين بالانتماءات وأدوار CRediT.

## المُخرجات

- `main.tex` — ملفّ جذر واحد أو تضمينات `\input{}` لكلّ قسم.
- `sections/01_intro.tex`، `02_related.tex`، `03_method.tex`، `04_experiments.tex`، `05_discussion.tex`،
  `06_conclusion.tex`.
- `backmatter.tex` — CRediT، التمويل، IRB، الموافقة المستنيرة، توفّر البيانات، التعارضات، الاختصارات.
- `refs.bib` — مدخلات مراجع بنمط IEEE.
- قائمة فحص الترجمة (العلامات، المراجع، العناصر الطافية، الاستشهادات).

## القواعد الأساسية

- فقط `\section` و`\subsection`. لا `\subsubsection` أبداً.
- سطر فارغ بعد كلّ أمر تقسيم.
- `% ====================== %` حول كلّ عنصر طافٍ أو معادلة أو جدول أو شكل أو خوارزميّة.
- استخدم ``...'' و`...' للاقتباس؛ لا اقتباسات مستقيمة.
- لا `\textit{}` في أيّ مكان؛ `\textbf{}` فقط للتسلسل الهرميّ الهيكليّ.
- استشهادات IEEE مرقّمة مجمّعة ومرتّبة.
- المتن الخلفيّ الإلزاميّ موجود حتّى إن قالت بعض الحقول "غير قابل للتطبيق".
- 4-6 كلمات مفتاحيّة مباشرةً بعد الملخّص.

## أمثلة

```latex
% ====================== %
\section{Methodology}
% ====================== %

\subsection{Problem Formulation}

Let $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{N}$ denote the training set. The objective
is to minimize the empirical risk

% ====================== %
\begin{equation}
\label{eq:empirical_risk}
\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^{N} \ell(f_\theta(x_i), y_i).
\end{equation}
% ====================== %

As shown in Fig.~\ref{fig:pipeline}, the proposed model ``FedTopo'' combines
topology regularization with batch-norm-aware aggregation.
```

```latex
% ====================== %
\section*{Data Availability}
% ====================== %
The multi-site MRI dataset used in this study is available from
\url{https://example.org/data} under the CC-BY-NC 4.0 license. Code
and trained weights are released at \url{https://github.com/...}.
```

## المراجع

- قالب ودليل مؤلّف IEEEtran: https://journals.ieeeauthorcenter.ieee.org/
- فئة Elsevier elsarticle: https://www.ctan.org/pkg/elsarticle
- تصنيف CRediT: https://credit.niso.org/
- دليل موضع العناصر الطافية في LaTeX (Overleaf): https://www.overleaf.com/learn/latex/Positioning_images_and_tables
