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
language: ar
---

# مُتحقِّق الواقعيّة

## متى تستخدم

- إجابة LLM طويلة أو موجز أو ملخّص مقال يحوي ادّعاءات واقعيّة ستُنشَر أو ستُستشهَد بها.
- يطالب مراجع بأدلّة على مستوى الادّعاء بدلاً من حكم "يبدو معقولاً" واحد.
- كلمات مفتاحيّة مُحفِّزة: "تحقّق واقعيّ"، "تحقّق من الادّعاءات"، "هل هذا صحيح"، "مدعوم بمصادر"، "ادّعاءات ذرّيّة"،
  "FActScore".
- إجابة RAG تمزج الحقائق المسترجعة بمعرفة النموذج الداخليّة وتحتاج لفصلهما.

## سير العمل

1. طبيع مخرجات الذكاء الاصطناعيّ: أزل زبد markdown، قسّم إلى جمل، أبقِ خريطة مدى للتظليل لاحقاً.
2. ذرِّر: قسّم كلّ جملة إلى ادّعاءات ذرّيّة (اقتراح واحد قابل للتحقّق لكلّ ادّعاء). استخدم قالب محفّز مثل "Decompose the
   following text into self-contained factual claims. One fact per line. No compound clauses."
3. لكلّ ادّعاء ذرّيّ، استرجع أدلّة. الترتيب الافتراضيّ: (أ) Wikipedia REST API (`https://en.wikipedia.org/w/api.php`
   action=query)، (ب) Wikidata لحقائق الكيانات، (ج) Crossref للاستشهادات، (د) بحث ويب عامّ عبر واجهة برمجة تطبيقات بحث
   مُتحقَّق منها. اقتبس المقطع المسترجع وسجّل URL.
4. قرّر لكلّ ادّعاء مع مرور مُتحقِّق: قارن الادّعاء مقابل الأدلّة باستخدام نموذج NLI (`microsoft/deberta-v3-large-mnli`)
   بالإضافة إلى محفّز حاكم LLM يُعيد تصنيفاً وتعليل جملة واحدة.
5. صنِّف كلّ ادّعاء: `SUPPORTED` (الأدلّة تستلزمه)، `REFUTED` (الأدلّة تناقضه)، أو `UNVERIFIABLE` (لا أدلّة حاسمة في
   أعلى k نتيجة).
6. احسب درجة واقعيّة = (#SUPPORTED) / (#SUPPORTED + #REFUTED + #UNVERIFIABLE) ودرجة FActScore صارمة = SUPPORTED /
   الإجمالي.
7. أصدِر جدولاً على مستوى الادّعاء مع المدى والتصنيف وURL الأدلّة والتعليل، بالإضافة إلى ملخّص عامّ.

## المُدخلات

- نصّ مخرجات الذكاء الاصطناعيّ (مطلوب).
- اختياريّ: قائمة بيضاء للمصادر الموثوقة (مثل PubMed، Statista، النطاقات الحكوميّة).
- اختياريّ: ادّعاءات ذهبيّة أو مجموعة بذور لتقصير الاسترجاع.
- اختياريّ: k لأعلى k أدلّة وعتبة استلزام NLI (افتراضيّ 0.7).

## المُخرجات

- `claims.jsonl` — صفّ واحد لكلّ ادّعاء ذرّيّ: `id`، `text`، `span`، `label`، `evidence_url`، `rationale`.
- `factuality_report.md` — جدول بالإضافة إلى FActScore ونسبة غير المدعوم وأعلى الادّعاءات المشكلة.
- HTML/markdown مظلّل من المخرجات بمدى SUPPORTED (أخضر)، REFUTED (أحمر)، UNVERIFIABLE (أصفر).

## القواعد الأساسية

- لا تصنِّف ادّعاءً SUPPORTED بدون URL أدلّة مسترجَع؛ "النموذج يعرفه" ليس تحقّقاً.
- الادّعاء يكون REFUTED فقط عندما تناقض الأدلّة المسترجَعة مباشرةً — غياب الأدلّة هو UNVERIFIABLE، لا REFUTED.
- يجب ألّا تحوي الادّعاءات الذرّيّة ضمائر؛ حلّ المراجع إلى الكيانات قبل الاسترجاع.
- استشهد بمنشأ الاسترجاع لكلّ تصنيف ليتمكّن البشر من تدقيق المسار.
- عندما تحمل جملة واحدة حقيقتين، قسّمها؛ لا تصنّف العبارات المركّبة.
- لا تكتب حقائق جديدة أثناء التذرير — أعد صياغة ما تقوله المخرجات فقط.

## أمثلة

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

## المزالق الشائعة

- معاملة "لا أدلّة موجودة" كـ REFUTED — يجب أن تكون UNVERIFIABLE؛ غياب الأدلّة ليس تناقضاً.
- استخدام المعرفة المعاملاتيّة للنموذج نفسها كأدلّة — المصادر المسترجَعة القابلة للاستشهاد فقط هي المعتمدة.
- الفشل في تذرير الادّعاءات المركّبة — الجمل المربوطة بـ"and" تخفي عادةً حقيقتين مستقلّتين.
- الوثوق بمصدر مسترجَع واحد للاّدّعاءات الحسّاسة — اطلب تأكيداً من مصدر ثانٍ مستقلّ.
- ترك حاكم LLM يكتب حقائق جديدة أثناء التذرير — أعد صياغة ما تقوله المخرجات فقط.
